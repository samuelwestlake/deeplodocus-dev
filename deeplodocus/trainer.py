from typing import Union
from typing import List

from torch import tensor
from torch.utils.data import  DataLoader
from torch.nn import Module

from deeplodocus.data.dataset import Dataset
from deeplodocus.callback import Callback
from deeplodocus.tester import Tester
from deeplodocus.utils.notification import Notification
from deeplodocus.utils.dict_utils import apply_weight
from deeplodocus.utils.flags import *
from deeplodocus.utils.generic_utils import is_string_an_integer



class Trainer(object):

    def __init__(self,
                 model:Module,
                 dataset:Dataset,
                 metrics:dict,
                 losses:dict,
                 optimizer,
                 num_epochs:int,
                 initial_epoch:int = 1,
                 batch_size:int = 4,
                 shuffle:bool = DEEP_SHUFFLE_ALL,
                 num_workers:int = 4,
                 verbose:int=2,
                 data_to_memorize:int = DEEP_MEMORIZE_BATCHES,
                 save_condition:int=DEEP_SAVE_CONDITION_AUTO,
                 stopping_parameters=None,
                 tester=None,
                 write_logs=True):

        self.model = model
        self.write_logs = write_logs
        self.metrics = metrics
        self.losses = losses
        self.shuffle = shuffle
        self.optimizer = optimizer
        self.initial_epoch = initial_epoch
        self.callbacks = Callback(metrics=metrics,
                                  losses=losses,
                                  working_directory="",
                                  model_name="test",
                                  verbose=verbose,
                                  data_to_memorize=data_to_memorize,
                                  save_condition=save_condition,
                                  stopping_parameters=stopping_parameters,
                                  write_logs=write_logs)
        self.num_epochs = num_epochs
        self.train_dataset = dataset
        self.dataloader_train =  DataLoader(dataset=dataset,
                                            batch_size=batch_size,
                                            shuffle=False,
                                            num_workers=num_workers)
        self.num_minibatches = self.__compute_num_minibatches(length_dataset=dataset.__len__(), batch_size=batch_size)

        if isinstance(tester, Tester):
            self.tester = tester          # Tester for validation
        else:
            self.tester = None

    def fit(self, first_training:bool = True)->None:
        """
        :param method:
        :return:
        """


        self.__train(first_training=first_training)

        Notification(DEEP_NOTIF_SUCCESS, "\n", write_logs=self.write_logs)
        Notification(DEEP_NOTIF_SUCCESS,"=============================================================", write_logs=self.write_logs)
        Notification(DEEP_NOTIF_SUCCESS,'Finished Training', write_logs=self.write_logs)
        Notification(DEEP_NOTIF_SUCCESS,"=============================================================", write_logs=self.write_logs)
        Notification(DEEP_NOTIF_SUCCESS,"\n", write_logs=self.write_logs)

        # Prompt if the user want to continue the training
        self.__continue_training()


    def __train(self, first_training = True)->None:
        """
        AUTHORS:
        --------

        :author: Alix Leroy

        DESCRIPTION:
        ------------

        Loop over the dataset to train the network

        PARAMETERS:
        -----------

        :param first_training->bool: Whether more epochs have been required after initial training or not

        RETURN:
        -------

        :return: None
        """


        if first_training is True :

            self.callbacks.on_train_begin()

        for epoch in range(self.initial_epoch, self.num_epochs+1):  # loop over the dataset multiple times

            for minibatch_index, minibatch in enumerate(self.dataloader_train):

                # Clean the given data
                inputs, labels, additional_data = self.__clean_single_element_list(minibatch)

                # zero the parameter gradients
                self.optimizer.zero_grad()

                # Infer the output of the batch
                outputs = self.model(inputs)

                # Compute losses and metrics
                result_losses = self.__compute_metrics(self.losses, inputs, outputs, labels, additional_data)
                result_metrics = self.__compute_metrics(self.metrics, inputs, outputs, labels, additional_data)

                # Add weights to losses
                for name, value in result_losses.items():
                    result_losses[name] = value * self.losses[name].get_weight()
                # TRY THIS FROM DICT_UTILS INSTEAD...
                # result_losses = apply_weight(result_losses, self.losses)


                # Sum all the result of the losses
                total_loss = sum(list(result_losses.values()))

                # Accumulates the gradient (by addition) for each parameter
                total_loss.backward()

                # performs a parameter update based on the current gradient (stored in .grad attribute of a parameter) and the update rule
                self.optimizer.step()

                # Minibatch callback
                self.callbacks.on_batch_end(minibatch_index=minibatch_index+1,
                                            num_minibatches=self.num_minibatches,
                                            epoch_index=epoch,
                                            total_loss=total_loss.item(),
                                            result_losses=result_losses,
                                            result_metrics=result_metrics)

            # Shuffle the data if required
            if self.shuffle is not None:
                self.train_dataset.shuffle(self.shuffle)

            # Reset the dataset (transforms cache)
            self.train_dataset.reset()

            total_validation_loss, result_validation_losses, result_validation_metrics = self.__evaluate_epoch()

            #Epoch callback
            self.callbacks.on_epoch_end(epoch_index=epoch,
                                        num_epochs=self.num_epochs,
                                        model=self.model,
                                        num_minibatches=self.num_minibatches,
                                        total_validation_loss=total_validation_loss,
                                        result_validation_losses=result_validation_losses,
                                        result_validation_metrics=result_validation_metrics)


        # End of training callback
        self.callbacks.on_training_end(model=self.model)

        # Pause callbacks which compute time
        self.callbacks.pause()

    def __compute_num_minibatches(self, batch_size:int, length_dataset:int):

        num_minibatches = length_dataset//batch_size

        if num_minibatches != length_dataset*batch_size:
            num_minibatches += 1
        return num_minibatches


    def __clean_single_element_list(self, minibatch:list)->list:
        """
        AUTHORS:
        --------

        :author: Alix Leroy

        DESCRIPTION:
        ------------

        Convert single element lists from the batch into an element

        PARAMETERS:
        -----------

        :param batch->list: The batch to clean

        RETURN:
        -------

        :return cleaned_batch->list: The cleaned batch
        """
        cleaned_minibatch = []

        # For each entry in the minibatch:
        # If it is a single element list -> Make it the single element
        # If it is an empty list -> Make it None
        # Else -> Do not change

        for entry in minibatch:

            if isinstance(entry, list) and len(entry) == 1:
                cleaned_minibatch.append(entry[0])

            elif isinstance(entry, list) and len(entry) == 0:
                cleaned_minibatch.append(None)

            else:
                cleaned_minibatch.append(entry)

        return cleaned_minibatch


    def __compute_metrics(self, metrics:dict, inputs:Union[tensor, list], outputs:Union[tensor, list], labels:Union[tensor, list], additional_data:Union[tensor, list])->dict:
        """
        AUTHORS;
        --------

        :author: Alix Leroy

        DESCRIPTION:
        ------------

        Compute the metrics using the corresponding method arguments

        PARAMETERS:
        -----------

        :param metrics->dict: The metrics to compute
        :param inputs->Union[tensor, list]: The inputs
        :param outputs->Union[tensor, list]: Outputs of the network
        :param labels->Union[tensor, list]: Labels
        :param additional_data->Union[tensor, list]: Additional data

        RETURN:
        -------

        :return->dict: A dictionary containing the associations (key, output)
        """

        result_metrics = {}

        # Temporary variable for saving the output
        temp_metric_result = None

        for metric in list(metrics.values()):
            metric_args = metric.get_arguments()
            metric_method = metric.get_method()

            #
            # Select the good type of input
            #
            if DEEP_ENTRY_INPUT in metric_args:
                if DEEP_ENTRY_LABEL in metric_args:
                    if DEEP_ENTRY_ADDITIONAL_DATA in metric_args:
                        temp_metric_result = metric_method(inputs, outputs, labels, additional_data)
                    else:
                        temp_metric_result = metric_method(inputs, outputs, labels)
                else:
                    if DEEP_ENTRY_ADDITIONAL_DATA in metric_args:
                        temp_metric_result = metric_method(inputs, outputs, additional_data)
                    else:
                        temp_metric_result = metric_method(inputs, outputs)
            else:
                if DEEP_ENTRY_LABEL in metric_args:
                    if DEEP_ENTRY_ADDITIONAL_DATA in metric_args:
                        temp_metric_result = metric_method(outputs, labels, additional_data)
                    else:
                        temp_metric_result = metric_method(outputs, labels)
                else:
                    if DEEP_ENTRY_ADDITIONAL_DATA in metric_args:
                        temp_metric_result = metric_method(outputs, additional_data)
                    else:
                        temp_metric_result = metric_method(outputs)

            #
            # Add the metric to the dictionary
            #

            # Check if the the metric is a Metric instance or a Loss instance
            if metric.is_loss() is True:
                # Do not call ".item()" in order to be able to achieve back propagation on the total_loss
                result_metrics[metric.get_name()] = temp_metric_result
            else:
                result_metrics[metric.get_name()] = temp_metric_result.item()

        return result_metrics

    def __continue_training(self):

        continue_training = ""

        # Ask if the user want to continue the training
        while continue_training.lower() != ("y" or "n"):

            continue_training = Notification(DEEP_NOTIF_INPUT, 'Would you like to continue the training ? (Y/N) ', write_logs=self.write_logs).get()

        #If yes ask the number of epochs
        if continue_training.lower() == "y":
            epochs = ""

            while is_string_an_integer(epochs) is False:
                epochs =  Notification(DEEP_NOTIF_INPUT, 'Number of epochs ? ', write_logs=self.write_logs).get()

            epochs = int(epochs)
            # Reset the system to continue the training
            if epochs > 0:
                self.initial_epoch = self.num_epochs
                self.num_epochs += epochs

                # Resume the training
                self.fit(first_training = False)



        else:
            pass

    def __evaluate_epoch(self):

        total_validation_loss = None
        result_losses = None
        result_metrics = None

        if self.tester is not None:
            total_validation_loss, result_losses, result_metrics = self.tester.evaluate()

        return total_validation_loss, result_losses, result_metrics




