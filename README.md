#Deeplodocus

##Introduction:
Initially created by both Alix Leroy and Samuel Westlake, Deeplodocus is a high-level framework with the objective to help to create, train, analyze and test deep networks.
Initially based on Keras, the framework was rewritten from scratch in a modular, flexible and config file based fashion. 
The current supported backed is PyTorch but you are more than welcome to contribute to  integrate another library.

Deeplodocus embeds functionalities such as : 

- Smart and automatic data loading
- Data augmentation / transformation 
- Metrics and losses display during training, validation and test stages
- Save of the results (model, weights and metrics)
- Custom loss and metrics
- Explicit logs system
- Training configuration from config files
- And more !

All the Deeplodocus parameters are available in the config files.

Deeplodocus is designed to be cross-platform (Windows, Linux and Mac OS). It uses Python 3.5.3+.


## Installation

The current version of Deeplodocus relies on PyTorch as backend. Please install the adequate version of PyTorch available [HERE](https://pytorch.org/).

### PIP

Once PyTorch is installed, you can install Deeplodocus using a PIP command :

`pip install deeplodocus`


### Required packages

* PyTorch (v1.0.0+)

#### Automatically installed
* numpy (v1.15.1+)
* pyyaml (3.13+)
* pandas (0.23.1+)
* matplotlib (2.2.2+)
* aiohttp (3.4.0+)
* psutil (5-4.8+)

### Recommended packages
* cv2 (3.1.4+) (For fast image transformation)


## Functionalities : 

* User friendly notifications [✓]
* User interface on browser [Under construction]
* Logs [✓]
* Automatic trainer [✓]
* Automatic tester/validator [✓]
* Callbacks [✓]
* History [✓]
* Saving the model [✓]
* Smart saving [✓]
* Dataset Loader [✓]
* Data checker [Under construction]
* Data Augmentation
* Transformations [✓]
* Filters
* Augmentation modes [Under construction]
* Instruction List [✓]

## Check version

There are two solutions to check Deeplodocus version:


1. Look at the version displayed into Deeplodocus logo when starting the `Brain` of your project

2. Run the following command in the terminal :
`deeplodocus version`

## Create a Deeplodocus project

Open a terminal / command line and enter :


`deeplodocus startproject "project-name"`

replacing "project-name" by the name of your project


This command will generate the following structure in the current folder :
- Main.py (Main file)
- Config folder
- Logs folder
- Results folder
- Model folder
- Losses folder
- Metrics folder
- Possible other folders to be defined




# Structure :

The current structure of Deeplodocus is as described by this schema :

INSERT FIGURE

## Entries

Deeplodocus is composed of 3 entries:
- Deeplodocus Admin : A terminal / command line entry to create a Deeplodocus project 
- Deeplodocus Brain : A main script file entry to train / test a deep network
- Deeplodocus UI : A browser access to an interface to configure and use Deeplodocus

### Deeplodocus Admin

The command line entry permits to access functions in the Deeplodocus admin system such as creating a Deeplodocus project

To access the admin commands just enter `deeplodocus` in the terminal followed by the required command.


### Deeplodocus Brain

Deeplodocus Brain is available through the Brain class.
A brain instance gives access to all the functionalities of Deeplodocus such as training or testing the network. It is also possible to access the brain using the main file generated by Deeplodocus Admin.

#### Instruction List
It is possible to interact with the Brain by giving a list of instructions to complete when waking up Deeplodocus. To do so just add commands into the `project.yaml` file

```yaml
# INSIDE config/project.yaml
on_wake: ["clear_history(force=True)",
          "load()",
          "train()"]
```
          
The commands available are exactly the one available through the terminal through Deeplodocus. See the documentation for more information on a specific command.

### Deeplodocus UI :

Using the terminal and modifying the config files may lead to errors that will cost time in the development of a network.
The Deeplodocus team develops a web interface permitting to :

- Define and generate dynamically config files
- Visualise the metrics in real time
- Visualise the generate network (graph)
- Previsualize data augmentation/transforms on the dataset
- ...


## Notifications :

Deeplodocus comes with a notification system. The current system is composed of 5 different notification categories :

- Info (blue) : Display a generic information to the user (default)
- Debug (Cyan) : Debug message (not visible for the end user)
- Success (green) : Display a successful action result
- Warning (yellow) : Display a warning
- Error (red) : Display a no-blocking error to the user
- Fatal error (white with red background) : Display a blocking error to the user. Stops the brain
- Result (white) : Display a training result
- Input (Blanking white) : Ask the user for an keyboard input
- Love<3 (Pink) : Exit message
- 

All notifications are saved into a log file in `logs/notification-datetime.logs`


## Data

The data in Deeplodocus is splitted into 3 different entries:

- Inputs (input given to your Machine Learning algorithm)
- Labels (Expected Output, optional)
- Additional Data (Additional data given to the loss function if required, optional)


In order to load the data you have to feed Deeplodocus using the `config/data.yaml` file:

```yaml

data.yaml

# _____________________________
#
# ---- DATA CONFIG EXAMPLE ----
# _____________________________
#

dataloader:
  batch_size: 4
  num_workers: 4
enabled:
  train: True
  validation: True
  test: True
dataset:
  train:
    name: "Train set"
    number: 100
    inputs:
      - source: ['../../data/input1.txt']
        join: ["../../data/"] # Null, auto, "some/path"      # (Optional) Null, auto, "some/path"
        type: "image"                             # (Optional) image, video, integer, label,
        load_method: "default" #default (online), offline, online
      - source: ['../../data/input2.txt']
        join: ["../../data/"]                                # (Optional) Null, auto, "some/path"
        type: "image"                             # (Optional) image, video, integer, label,
        load_method: "default" #default (online), offline, online
    labels:
      - source: ['../../data/label1.txt']
        join: Null
        type: "integer"
        load_method: "default" #default (online), offline, online
    additional_data:
      - Null
  validation:
    name: "Validation set"
    number : 7
    inputs:
      - source: ['../../data/input1.txt']
        join: Null # Null, auto, "some/path"      # (Optional) Null, auto, "some/path"
        type: "image"                             # (Optional) image, video, integer, label,
        load_method: "default" #default (online), offline, online
      - source: ['../../data/input2.txt']
        join: Null                                # (Optional) Null, auto, "some/path"
        type: "image"                             # (Optional) image, video, integer, label,
        load_method: "default" #default (online), offline, online
    labels:
      - source: ['../../data/label1.txt']
        type: "integer"
        load_method: "default" #default (online), offline, online
    additional_data:
      - Null
  test:
    name: "Test set"
    number : 7
    inputs:
      - source: ['../../data/input1.txt']
        join: Null # Null, auto, "some/path"      # (Optional) Null, auto, "some/path"
        type: "image"                             # (Optional) image, video, integer, label,
        load_method: "default" #default (online), offline, online
      - source: ['../../data/input2.txt']
        join: Null                                # (Optional) Null, auto, "some/path"
        type: "image"                             # (Optional) image, video, integer, label,
        load_method: "default" #default (online), offline, online
    labels:
      - source: ['../../data/label1.txt']
        type: "integer"
        load_method: "default" #default (online), offline, online
    additional_data:
      - Null

```

Deeplodocus accepts to load data referenced in text files (images path, video path, numbers, text, numpy array path, etc...) and also files inside folder.
Therefore you can directly give a file path or a folder path.

NOTE: Relative paths are relative to the main file

```yaml

# Example

train:
    inputs:
      - source: "input1.txt"            # Works

train:
    inputs:
      - source: "./path_to_folder/"     # Works as well
```


If you have multiple entries, please add the item below:

```yaml

# Example

train:
    inputs:
      - source: "input1.txt"  # Input 1
      - source: "input2.txt"  # Input 2 

```

If one entry is split in to different location, you can merge these to sources in one using brackets:
```yaml

# Example

train:
    inputs:
      - source: ["input1-1.txt", "input1-2.txt"]            # Input 1 = input1-1 + input1-2
      - source: "input2.txt"                                # Input 2
```

 
 
 Data are loaded by Deeplodocus through two interfaces :
 - Dataset
 - Dataloader

### Dataset

The `Dataset` has two main objectives :
- Automatically read, check the completeness and format the data given in the config files in folders and files
- Open, augment/transform the data before being transmitted to the network


### Dataloader

The `Dataloader` can call the `Dataset` in parallel of the training using the CPU.
The data are assembled into batches and then sent to the `Trainer` or the `Tester`

NOTE : Currently the Dataloader is provided by the PyTorch's Dataloader.




### Data Transformation

Data transformation is made using four different `Transformer` classes managed by a `TransformManager`. The following `Transformer` classes are available:
- Sequential
- One Of
- Some Of
- Pointer


#### TransformManager 

Here is an example of config file to generate the `TransformManager` for the training, validation and test.
Make sure the three are given in one file.


```yaml

# transform_config.yaml

# ___________________________________
#
# ---- TRANSFORM MANAGER EXAMPLE ----
# ___________________________________
#
train:                                                                              # Training entries
    name: "Train Transform Manager"
    inputs :
      - ".config/transforms/transform_input_train_left.yaml"
      - "*input:0"                                                                  # Example of pointer which points to first transformer of input
    labels :
      - Null                                                                        
      - Null
    additional_data:
      - Null

validation:                                                                        # Validation entries
    name: "Validation Transform Manager"
    inputs :
      - ".config/transforms/transform_input_validation_left.yaml"
      - "*input:0"                                                                  # Example of pointer which points to first transformer of input
    labels :
      - Null
      - Null
    additional_data:
      - Null

test:                                                                               # Test entries
    name: "Validation Transform Manager"
    inputs:
      - Null
      - Null
    labels :
      - Null
      - Null
    additional_data:
      - Null
```

Each entry has to be given a `Transformer`. If none is desired, please enter `Null`.

#### Sequential

The `Sequential` transformer applies transformation operations sequentially on the given input.

Here is an example of config file for a `Sequential` transformer:

```yaml

# sequential_example.yaml

# ______________________________________
#
# ---- TRANSFORM SEQUENTIAL EXAMPLE ----
# ______________________________________
#

method: "sequential"
name: "Sequential example"

transforms:
  - blur :
      kernel_size : 3
  - random_blur:
      kernel_size_min: 15
      kernel_size_max : 21
```

For more details on each transform please check the corresponding documentation


#### One Of

The `Oneof` transformer applies on the given input one transformation operation among the ones available in the given list.

Here is an example of config file for a `OneOf` transformer:

```yaml
# oneof_example.yaml

# _________________________________
#
# ---- TRANSFORM ONEOF EXAMPLE ----
# _________________________________
#

method: "oneof"
name: "OneOf example"

mandatory_transforms_start:
    - name: "resize"
      # module : "deeplodocus.app.transforms.image"
      kwargs:
          shape : [512, 512, 3]
          keep_aspect : True
          padding : 0


transforms:
  - blur :
      kernel_size : 3
  - random_blur:
      kernel_size_min: 15
      kernel_size_max : 21
      
    
mandatory_transforms_end:
      - name: "normalize_image"
        #module:
        kwargs:
          mean: [127.5, 127.5, 127.5]
          standard_deviation: 255
```

For more details on each transform please check the corresponding documentation


#### Some Of

The `Someof` transformer applies multiple transformation operations to the given input.
The number of operations applied can be fixed if the user specifies `num_transformations`.
The number of transformation can also be a random number between `num_transformations_min` and `num_transformations_max`.

Here is an example of config file for a `SomeOf` transformer:

```yaml
# someof_example.yaml
# _________________________________
#
# ---- TRANSFORM SOME OF EXAMPLE ----
# _________________________________
#

method: "someof"
name: "Some Of example"

num_transformations : 3             #If used, comment "num_transformations_min" and  "num_transformations_max"
#num_transformations_min : 1        #If used, comment "num_transformations"
#num_transformations_max : 5        #If used, comment "num_transformations"

mandatory_transforms_start:
    - name: "resize"
      # module : "deeplodocus.app.transforms.image"
      kwargs:
          shape : [512, 512, 3]
          keep_aspect : True
          padding : 0


transforms:
    - # module: "" #optional
      name: "blur"
      kwargs:
        kernel_size : 3
    - # module :"" # optional
      name : "random_blur"
      kwargs:
        kernel_size_min: 15
        kernel_size_max : 21
    - # module : "" # optional
      name : "example_function"
      kwargs :
        parameters : 1


mandatory_transforms_end:
      - name: "normalize_image"
        #module:
        kwargs:
          mean: [127.5, 127.5, 127.5]
          standard_deviation: 255

```

For more details on each transform please check the corresponding documentation

#### Pointer

The Pointer consists in redirecting the transformation process to another transformer.
Using a pointer has two major advantages :

- It avoids creating another transformer config file
- It allows multiple entries system to have exactly the same transformation operations applied to all its entries. [1]

[1] - e.g. : Working on a stereo vision system. The input of the network consists in two images (left and right).
If we create to transformers (one for the left image and one for the right image) then the left and right image will not have the same transformations applied (if random operations are used).
Using a pointer for the right image to the left transformer will allow to have exactly the same transformations applied to both the right and left image (even if random operations and done (e.g. random blur)

To define a Pointer, instead of the path to the transformer config file, enter 

```yaml
*category:index
```

```yaml
# * Is necessary so that Deeplodocus understands it is a pointer
# category: "input", "label", "additional_data"
# index: The index of the transformer in the selected category (indexed at 0)

#e.g. : "*input:0" points to the first transformer of the input
```

Note : A `Pointer` cannot point to another `Pointer`

#### Offline

Offline data augmentation is not available

#### Custom transforms

Not only Deeplodocus provides a rich list of standard builtin transformation operations, it also allows you to define your own transforms !

The transforms can either be fixed operations or random operations. The following example illustrates two different transforms (blurs).
The first blur method directly uses the given kernel size whereas the second one computes a blur whose the kernel size is picked between its min and max parameters.


```python
import random
import numpy as np
import cv2

def blur(image: np.array, kernel_size: int) -> Tuple[Any, None]:
    """
    AUTHORS:
    --------

    :author: Alix Leroy

    DESCRIPTION:
    ------------

    Apply a blur to the image

    PARAMETERS:
    -----------

    :param image: np.array: The image to transform
    :param kernel_size: int: Kernel size

    RETURN:
    -------

    :return: The blurred image
    :return: None
    """
    return cv2.blur(image, (int(kernel_size), int(kernel_size))), None


def random_blur(image: np.array, kernel_size_min: int, kernel_size_max: int) -> Tuple[Any, dict]:
    """
    AUTHORS:
    --------

    :author: Alix Leroy

    DESCRIPTION:
    ------------

    Apply a random blur to the image


    PARAMETERS:
    -----------

    :param image: np.array: The image to transform
    :param kernel_size_min: int: Min size of the kernel
    :param kernel_size_max: int: Max size of the kernel


    RETURN:
    -------

    :return: The blurred image
    :return: The last transform data
    """
    kernel_size = (random.randint(kernel_size_min // 2, kernel_size_max // 2)) * 2 + 1
    image, _ = blur(image, kernel_size)
    transform = {"name": "blur",
                 "method": blur,
                 "module_path": __name__,
                 "kwargs": {"kernel_size": kernel_size}}
    return image, transform
```


The custom transforms can be saved inside the `config/modules/transforms` folder in any python file. This architecture allows your to structure your files as you wish.


## Model

### Pytorch Model

### Custom Model

Deeplodocus is compatible with any PyTorch custom model with the following structure.

```python

import torch.nn as nn

class CustomModel(nn.Module):

    def __init__(self, resize_method):
        super(CustomModel, self).__init__()
        
        # DEFINE THE DIFFERENT MODULES OF YOUR MODEL
        
    def forward(self, input):
        
        # DEFINE THE FORWARD PASS OF YOUR MODEL
        
        return output
```

If your Deeplodocus project contains multiple input entries, they will be available in the forward function as follow:


```python
    def forward(self, input1, input2, input3):
        
        # DEFINE THE FORWARD PASS OF YOUR MODEL
        
        return output
```

If your input entry contains a sequence of data, the sequence will be available in a list as follow:

```python
    def forward(self, sequence):
        
        # Method1
        item1, item2, item3 = sequence
        
        #Method2
        for item in sequence:
            # DO SOMETHING
        
        # DEFINE THE FORWARD PASS OF YOUR MODEL
        
        return output
```