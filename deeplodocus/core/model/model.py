import torch
import torch.nn as nn
import numpy as np
from collections import OrderedDict

from deeplodocus.utils.flags.module import DEEP_MODULE_MODELS
from deeplodocus.utils.generic_utils import get_module
from deeplodocus.utils.notification import Notification
from deeplodocus.utils.flags.notif import *
from deeplodocus.utils.flags.msg import DEEP_MSG_MODEL_CHECK_CHANNELS


def load_model(
        name, module, kwargs, device,
        model_state_dict=None,
        device_ids=None,
        input_size=None,
        batch_size=None
):
    # Get the model, should be nn.Module
    module, origin = get_module(name=name, module=module, browse=DEEP_MODULE_MODELS)
    if module is None:
        return None

    # Define our model that inherits from the nn.Module
    class Model(module):

        def __init__(self, name, origin, device,
                     device_ids=None,
                     input_size=None,
                     batch_size=None,
                     model_dict=None,
                     **kwargs):
            super(Model, self).__init__(**kwargs)
            self.name = name
            self.origin = origin
            self.device_ids = device_ids
            self.input_size = input_size
            self.batch_size = batch_size
            self.model_dict = {} if model_dict is None else model_dict
            self.device = device

        def summary(self):
            """
            AUTHORS:
            --------
            :author: Alix Leroy
            :author: Samuel Westlake
            DESCRIPTION:
            ------------
            Summarise the model
            PARAMETERS:
            -----------
            None
            RETURN:
            -------
            :return: None
            """

            if self.input_size is not None:
                self.__summary()
            else:
                Notification(DEEP_NOTIF_ERROR, "Model's input size not given, the summary cannot be displayed.")

        def __summary(self):
            """
            AUTHORS:
            --------
            :author:  https://github.com/sksq96/pytorch-summary
            :author: Alix Leroy
            DESCRIPTION:
            ------------
            Print a summary of the current model
            PARAMETERS:
            -----------
            None
            RETURN:
            -------
            :return: None
            """

            def register_hook(module):

                def hook(module, input, output):
                    class_name = str(module.__class__).split(".")[-1].split("'")[0]
                    module_idx = len(summary)
                    m_key = "%s-%i" % (class_name, module_idx + 1)
                    summary[m_key] = OrderedDict()
                    summary[m_key]["input_shape"] = list(input[0].size())
                    summary[m_key]["input_shape"][0] = self.batch_size
                    if isinstance(output, (list, tuple)):
                        summary[m_key]["output_shape"] = [[-1] + list(o.size())[1:] for o in output]
                    else:
                        summary[m_key]["output_shape"] = list(output.size())
                        summary[m_key]["output_shape"][0] = self.batch_size
                    params = 0
                    if hasattr(module, "weight") and hasattr(module.weight, "size"):
                        params += torch.prod(torch.LongTensor(list(module.weight.size())))
                        summary[m_key]["trainable"] = module.weight.requires_grad
                    if hasattr(module, "bias") and hasattr(module.bias, "size"):
                        params += torch.prod(torch.LongTensor(list(module.bias.size())))
                    summary[m_key]["nb_params"] = params

                if (
                        not isinstance(module, nn.Sequential)
                        and not isinstance(module, nn.ModuleList)
                        and not (module == model)
                ):
                    hooks.append(module.register_forward_hook(hook))

            # Batch_size of 2 for batchnorm
            x = [torch.rand(2, *in_size) for in_size in input_size]

            # Move the batch to the same device as the model
            x = [i.to(self.device) for i in x]

            # Create properties
            summary = OrderedDict()
            hooks = []

            # Register hook
            self.apply(register_hook)

            # Make a forward pass
            try:
                self.forward(*x)
            except RuntimeError as e:
                if "channels" in str(e):
                    Notification(
                        DEEP_NOTIF_FATAL,
                        str(e),
                        solutions=[
                            DEEP_MSG_MODEL_CHECK_CHANNELS
                        ]
                    )
                else:
                    Notification(DeprecationWarning, str(e))

            # Remove these hooks
            for h in hooks:
                h.remove()

            Notification(DEEP_NOTIF_INFO, '================================================================')
            Notification(DEEP_NOTIF_INFO, "MODEL : %s from %s" % (self.name, self.origin))
            Notification(DEEP_NOTIF_INFO, '================================================================')
            line_new = '{:>20}  {:>25} {:>15}'.format('Layer (type)', 'Output Shape', 'Param #')
            Notification(DEEP_NOTIF_INFO, line_new)
            Notification(DEEP_NOTIF_INFO, '----------------------------------------------------------------')
            total_params = 0
            total_output = 0
            trainable_params = 0
            for layer in summary:
                # Input_shape, output_shape, trainable, nb_params
                line_new = '{:>20}  {:>25} {:>15}'.format(layer, str(summary[layer]['output_shape']),
                                                          '{0:,}'.format(summary[layer]['nb_params']))
                total_params += summary[layer]['nb_params']
                total_output += np.prod(summary[layer]["output_shape"])
                if 'trainable' in summary[layer]:
                    if summary[layer]['trainable'] == True:
                        trainable_params += summary[layer]['nb_params']
                Notification(DEEP_NOTIF_INFO, line_new)

            # Assume 4 bytes/number (float on cuda).
            total_input_size = abs(np.prod(input_size) * self.batch_size * 4. / (1024 ** 2.))
            total_output_size = abs(2. * total_output * 4. / (1024 ** 2.))  # x2 for gradients
            total_params_size = abs(total_params.numpy() * 4. / (1024 ** 2.))
            total_size = total_params_size + total_output_size + total_input_size
            Notification(DEEP_NOTIF_INFO, '----------------------------------------------------------------')
            Notification(DEEP_NOTIF_INFO, "Input size : %s" % self.input_size)
            Notification(DEEP_NOTIF_INFO, "Batch size : %s" % self.batch_size)
            for key, item in self.model_dict.items():
                Notification(DEEP_NOTIF_INFO, "%s : %s" % (key, item))
            Notification(DEEP_NOTIF_INFO, '----------------------------------------------------------------')
            Notification(DEEP_NOTIF_INFO, 'Total params: {0:,}'.format(total_params))
            Notification(DEEP_NOTIF_INFO, 'Trainable params: {0:,}'.format(trainable_params))
            Notification(DEEP_NOTIF_INFO, 'Non-trainable params: {0:,}'.format(total_params - trainable_params))
            Notification(DEEP_NOTIF_INFO, '----------------------------------------------------------------')
            Notification(DEEP_NOTIF_INFO, "Input size (MB): %0.2f" % total_input_size)
            Notification(DEEP_NOTIF_INFO, "Forward/backward pass size (MB): %0.2f" % total_output_size)
            Notification(DEEP_NOTIF_INFO, "Params size (MB): %0.2f" % total_params_size)
            Notification(DEEP_NOTIF_INFO, "Estimated Total Size (MB): %0.2f" % total_size)
            Notification(DEEP_NOTIF_INFO, '----------------------------------------------------------------')

    # Initialise the model
    model = Model(
        name=name,
        origin=origin,
        device=device,
        device_ids=device_ids,
        input_size=input_size,
        batch_size=batch_size,
        model_dict=kwargs,
        **kwargs
    )

    if model_state_dict is not None:
        model_state_dict = {k[7:]: v for k, v in model_state_dict.items() if k.startswith("module.")}

        model.load_state_dict(model_state_dict)

    n_devices = torch.cuda.device_count() if device_ids is None else len(device_ids)
    if n_devices > 1:
        model = DataParallelModel(module=model)

    # Send to the appropriate device
    model.to(device)

    # inp = torch.zeros((2, 3, 416, 416)).to(model.device)
    # output = model(inp)
    # print(output.shape)
    return model


class DataParallelModel(nn.DataParallel):

    def __init__(self, module):
        super(DataParallelModel, self).__init__(module, device_ids=module.device_ids)
        self.name = module.name
        self.origin = module.origin,
        self.device = module.device

    def summary(self):
        self.module.summary()
