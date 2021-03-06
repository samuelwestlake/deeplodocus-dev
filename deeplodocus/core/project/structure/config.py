from deeplodocus.flags.ext import DEEP_EXT_YAML

# The divider to use when expressing paths to configs
DEEP_CONFIG_DIVIDER = "/"

# Keywords
DEEP_CONFIG_INIT = "INIT"
DEEP_CONFIG_DEFAULT = "DEFAULT"
DEEP_CONFIG_DTYPE = "DTYPE"
DEEP_CONFIG_WILDCARD = "*"

# Names of each section of the config fle
DEEP_CONFIG_PROJECT = "project"
DEEP_CONFIG_MODEL = "model"
DEEP_CONFIG_TRAINING = "training"
DEEP_CONFIG_DATA = "data"
DEEP_CONFIG_TRANSFORM = "transform"
DEEP_CONFIG_OPTIMIZER = "optimizer"
DEEP_CONFIG_METRICS = "metrics"
DEEP_CONFIG_LOSSES = "losses"
DEEP_CONFIG_HISTORY = "history"

# Wildcard place holders
DEEP_CONFIG_WILDCARD_DEFAULT = {
    DEEP_CONFIG_METRICS: "accuracy",
    DEEP_CONFIG_LOSSES: "loss",
    "datasets": "MNIST Train"
}

# List of all config sections
DEEP_CONFIG_SECTIONS = [
    DEEP_CONFIG_PROJECT,
    DEEP_CONFIG_MODEL,
    DEEP_CONFIG_TRAINING,
    DEEP_CONFIG_DATA,
    DEEP_CONFIG_TRANSFORM,
    DEEP_CONFIG_OPTIMIZER,
    DEEP_CONFIG_METRICS,
    DEEP_CONFIG_LOSSES,
    DEEP_CONFIG_HISTORY
]

DEF = {
    "SOURCE": '"./data/..."    # Path to data file/folder',
    "JOIN": "Null              # Path to append to the start of each data item",
    "TYPE_IMG": '"image"           # One of: "integer", "image", "string", "float", "np-array", "bool", "video", "audio"',
    "TYPE_INT": '"int"             # One of: "integer", "image", "string", "float", "np-array", "bool", "video", "audio"',
    "LOAD_METHOD": '"default"  # One of: "online" / "default" or "offline"',
    "NUMBER": "Null                # The number of instances from the dataset to use (Null = all instances)",
    "LOAD_AS": '"float32"            # The Data type at the input of the network (int, float32, float64, etc...)',
    "MOVE_AXES": '"[0, 1, 2]"      # Move axes if necessary'
}

# A dict of names for each config file
DEEP_CONFIG_FILES = {item: "%s%s" % (item, DEEP_EXT_YAML) for item in DEEP_CONFIG_SECTIONS}

# Define the expected structure of the project configuration space
# First level keys define the name of config .yaml files
# Second level keys and below should be found in each file
# Default values and  data types must be given for each configuration
# NB: if a list of floats is expected, use [float] instead of float
DEEP_CONFIG = {
    DEEP_CONFIG_PROJECT: {
        "session": {
            DEEP_CONFIG_DTYPE: str,
            DEEP_CONFIG_DEFAULT: "version01"
        },
        "enable_log": {
            DEEP_CONFIG_DTYPE: bool,
            DEEP_CONFIG_DEFAULT: True
        },
        "cv_library": {
            DEEP_CONFIG_DTYPE: str,
            DEEP_CONFIG_DEFAULT: "opencv"
        },
        "device": {
            DEEP_CONFIG_DTYPE: str,
            DEEP_CONFIG_DEFAULT: "auto"
        },
        "device_ids": {
            DEEP_CONFIG_DTYPE: [int],
            DEEP_CONFIG_DEFAULT: "auto"
        },
        "on_wake": {
            DEEP_CONFIG_DTYPE: [str],
            DEEP_CONFIG_DEFAULT: None,
            DEEP_CONFIG_INIT: [
                'config.data.datasets[0].entries[0].sources[0].kwargs.__dict__["transform"] = np.array',
                'config.data.datasets[1].entries[0].sources[0].kwargs.__dict__["transform"] = np.array'
            ]
        },
        "imports": {
            DEEP_CONFIG_DTYPE: [str],
            DEEP_CONFIG_DEFAULT: None,
            DEEP_CONFIG_INIT: "numpy as np"
        }
    },
    DEEP_CONFIG_MODEL: {
        "name": {
            DEEP_CONFIG_DTYPE: str,
            DEEP_CONFIG_DEFAULT: "LeNet"
        },
        "module": {
            DEEP_CONFIG_DTYPE: str,
            DEEP_CONFIG_DEFAULT: None,
            DEEP_CONFIG_INIT: "deeplodocus.app.models.lenet"
        },
        "epoch": {
            DEEP_CONFIG_DTYPE: int,
            DEEP_CONFIG_DEFAULT: None
        },
        "from_file": {
            DEEP_CONFIG_DTYPE: bool,
            DEEP_CONFIG_DEFAULT: False
        },
        "file": {
            DEEP_CONFIG_DTYPE: str,
            DEEP_CONFIG_DEFAULT: None
        },
        "input_size": {
            DEEP_CONFIG_DTYPE: [[int]],
            DEEP_CONFIG_DEFAULT: None,
            DEEP_CONFIG_INIT: [[1, 28, 28]]
        },
        "kwargs": {
            DEEP_CONFIG_DTYPE: dict,
            DEEP_CONFIG_DEFAULT: {},
        }
    },
    DEEP_CONFIG_OPTIMIZER: {
        "name": {
            DEEP_CONFIG_DTYPE: str,
            DEEP_CONFIG_DEFAULT: "Adam"
        },
        "module": {
            DEEP_CONFIG_DTYPE: str,
            DEEP_CONFIG_DEFAULT: None,
            DEEP_CONFIG_INIT: "torch.optim"
        },
        "kwargs": {
            DEEP_CONFIG_DTYPE: dict,
            DEEP_CONFIG_DEFAULT: {}
        },
        "param_groups": {
            DEEP_CONFIG_DTYPE: None,
            DEEP_CONFIG_DEFAULT: None
        }
    },
    DEEP_CONFIG_HISTORY: {
        "enabled": {
            "train_batches": {
                DEEP_CONFIG_DTYPE: bool,
                DEEP_CONFIG_DEFAULT: True
            },
            "train_epochs": {
                DEEP_CONFIG_DTYPE: bool,
                DEEP_CONFIG_DEFAULT: True
            },
            "validation": {
                DEEP_CONFIG_DTYPE: bool,
                DEEP_CONFIG_DEFAULT: True
            }
        },
    },
    DEEP_CONFIG_TRAINING: {
        "verbose": {
            DEEP_CONFIG_DTYPE: str,
            DEEP_CONFIG_DEFAULT: "epoch"
        },
        "num_epochs": {
            DEEP_CONFIG_DTYPE: int,
            DEEP_CONFIG_DEFAULT: 10
        },
        "shuffle": {
            DEEP_CONFIG_DTYPE: str,
            DEEP_CONFIG_DEFAULT: "default"
        },
        "accumulate": {
            DEEP_CONFIG_DTYPE: int,
            DEEP_CONFIG_DEFAULT: 1
        },
        "enable_metrics": {
            DEEP_CONFIG_DTYPE: bool,
            DEEP_CONFIG_DEFAULT: True
        },
        "scheduler": {
            "name": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: str,
                DEEP_CONFIG_INIT: "ExponentialLR"
            },
            "module": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: str,
                DEEP_CONFIG_INIT: "torch.optim.lr_scheduler"
            },
            "enabled": {
                DEEP_CONFIG_DEFAULT: False,
                DEEP_CONFIG_DTYPE: bool,
                DEEP_CONFIG_INIT: True
            },
            "kwargs": {
                DEEP_CONFIG_DEFAULT: {},
                DEEP_CONFIG_DTYPE: dict,
                DEEP_CONFIG_INIT: {"gamma": 0.95}
            }
        },
        "saver": {
            "method": {
                DEEP_CONFIG_DEFAULT: "pytorch",
                DEEP_CONFIG_DTYPE: str
            },
            "save_signal": {
                DEEP_CONFIG_DEFAULT: "auto",
                DEEP_CONFIG_DTYPE: str
            },
            "overwrite": {
                DEEP_CONFIG_DEFAULT: False,
                DEEP_CONFIG_DTYPE: bool
            }
        },
        "overwatch": {
            "metric": {
                DEEP_CONFIG_DEFAULT: "Total Loss",
                DEEP_CONFIG_DTYPE: str
            },
            "condition": {
                DEEP_CONFIG_DEFAULT: "less",
                DEEP_CONFIG_DTYPE: str
            },
            "dataset": {
                DEEP_CONFIG_DEFAULT: "validation",
                DEEP_CONFIG_DTYPE: str
            }
        },
    },
    DEEP_CONFIG_DATA: {
        "dataloader": {
            "num_workers": {
                DEEP_CONFIG_DTYPE: int,
                DEEP_CONFIG_DEFAULT: 1
            }
        },
        "enabled": {
            "train": {
                DEEP_CONFIG_DTYPE: bool,
                DEEP_CONFIG_DEFAULT: False,
                DEEP_CONFIG_INIT: True
            },
            "validation": {
                DEEP_CONFIG_DTYPE: bool,
                DEEP_CONFIG_DEFAULT: False
            },
            "test": {
                DEEP_CONFIG_DTYPE: bool,
                DEEP_CONFIG_DEFAULT: False
            },
            "prediction": {
                DEEP_CONFIG_DTYPE: bool,
                DEEP_CONFIG_DEFAULT: False
            }
        },
        "datasets": [
            {
                "name": {
                    DEEP_CONFIG_DTYPE: str,
                    DEEP_CONFIG_DEFAULT: "Dataset",
                    DEEP_CONFIG_INIT: "Train MNIST"
                },
                "type": {
                    DEEP_CONFIG_DTYPE: str,
                    DEEP_CONFIG_DEFAULT: "train",
                },
                "num_instances": {
                    DEEP_CONFIG_DTYPE: int,
                    DEEP_CONFIG_DEFAULT: None,
                },
                "batch_size": {
                    DEEP_CONFIG_DTYPE: int,
                    DEEP_CONFIG_DEFAULT: 1
                },
                "entries": [
                    {
                        "name": {
                            DEEP_CONFIG_DTYPE: str,
                            DEEP_CONFIG_DEFAULT: "Data Entry",
                            DEEP_CONFIG_INIT: "MNIST Image"
                        },
                        "type": {
                            DEEP_CONFIG_DTYPE: str,
                            DEEP_CONFIG_DEFAULT: "input",
                        },
                        "data_type": {
                            DEEP_CONFIG_DTYPE: str,
                            DEEP_CONFIG_DEFAULT: "image",
                        },
                        "load_as":
                        {
                            DEEP_CONFIG_DTYPE: str,
                            DEEP_CONFIG_DEFAULT: "float32",
                        },
                        "move_axis": {
                            DEEP_CONFIG_DTYPE: [int],
                            DEEP_CONFIG_DEFAULT: None,
                        },
                        "enable_cache": {
                            DEEP_CONFIG_DTYPE: bool,
                            DEEP_CONFIG_DEFAULT: False,
                        },
                        "sources": [
                            {
                                "name": {
                                    DEEP_CONFIG_DTYPE: str,
                                    DEEP_CONFIG_DEFAULT: "MNIST",
                                },
                                "module": {
                                    DEEP_CONFIG_DTYPE: str,
                                    DEEP_CONFIG_DEFAULT: None,
                                    DEEP_CONFIG_INIT: "torchvision.datasets"
                                },
                                "kwargs": {
                                    DEEP_CONFIG_DTYPE: dict,
                                    DEEP_CONFIG_DEFAULT: {},
                                    DEEP_CONFIG_INIT: {
                                        "root": "./MNIST",
                                        "train": True,
                                        "download": True
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        ],
    },
    DEEP_CONFIG_LOSSES: {
        DEEP_CONFIG_WILDCARD: {
            "name": {
                DEEP_CONFIG_DTYPE: str,
                DEEP_CONFIG_DEFAULT: "CrossEntropyLoss"
            },
            "module": {
                DEEP_CONFIG_DTYPE: str,
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_INIT: "torch.nn.modules.loss"
            },
            "weight": {
                DEEP_CONFIG_DTYPE: float,
                DEEP_CONFIG_DEFAULT: 1
            },
            "kwargs": {
                DEEP_CONFIG_DTYPE: dict,
                DEEP_CONFIG_DEFAULT: {}
            }
        }
    },
    DEEP_CONFIG_TRANSFORM: {
        "train": {
            "name": {
                DEEP_CONFIG_DEFAULT: "Train Transform Manager",
                DEEP_CONFIG_DTYPE: str
            },
            "inputs": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str],
                DEEP_CONFIG_INIT: ["config/transformers/input.yaml"]
            },
            "labels": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str],
            },
            "additional_data": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str]
            },
            "outputs": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str]
            }
        },
        "validation": {
            "name": {
                DEEP_CONFIG_DEFAULT: "Validation Transform Manager",
                DEEP_CONFIG_DTYPE: str
            },
            "inputs": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str],
                DEEP_CONFIG_INIT: ["config/transformers/input.yaml"]
            },
            "labels": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str],
            },
            "additional_data": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str]
            },
            "outputs": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str]
            }
        },
        "test": {
            "name": {
                DEEP_CONFIG_DEFAULT: "Test Transform Manager",
                DEEP_CONFIG_DTYPE: str
            },
            "inputs": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str],
            },
            "labels": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str],
            },
            "additional_data": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str]
            },
            "outputs": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str]
            }
        },
        "prediction": {
            "name": {
                DEEP_CONFIG_DTYPE: str,
                DEEP_CONFIG_DEFAULT: "Predict Transform Manager",
            },
            "inputs": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str]
            },
            "additional_data": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str]
            },
            "outputs": {
                DEEP_CONFIG_DEFAULT: None,
                DEEP_CONFIG_DTYPE: [str]
                }
            }
        },
    DEEP_CONFIG_METRICS: {
        DEEP_CONFIG_WILDCARD: {
            "name": {
                DEEP_CONFIG_DTYPE: str,
                DEEP_CONFIG_DEFAULT: "accuracy"
            },
            "module": {
                DEEP_CONFIG_DTYPE: str,
                DEEP_CONFIG_DEFAULT: None
            },
            "reduce": {
                DEEP_CONFIG_DTYPE: str,
                DEEP_CONFIG_DEFAULT: "mean"
            },
            "ignore_value": {
                DEEP_CONFIG_DTYPE: float,
                DEEP_CONFIG_DEFAULT: None
            },
            "kwargs": {
                DEEP_CONFIG_DTYPE: dict,
                DEEP_CONFIG_DEFAULT: {}
            }
        }
    }
}
