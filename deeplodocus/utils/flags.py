#
# ENTRIES
#

DEEP_ENTRY_INPUT = 0
DEEP_ENTRY_LABEL = 1
DEEP_ENTRY_OUTPUT = 2
DEEP_ENTRY_ADDITIONAL_DATA = 3

#
# TYPE FLAGS
#

DEEP_TYPE_FILE = 0
DEEP_TYPE_FOLDER = 1
DEEP_TYPE_IMAGE = 2
DEEP_TYPE_VIDEO = 3
DEEP_TYPE_INTEGER = 4
DEEP_TYPE_FLOAT = 5
DEEP_TYPE_BOOLEAN = 6
DEEP_TYPE_SOUND = 7
DEEP_TYPE_SEQUENCE = 8
DEEP_TYPE_NP_ARRAY = 9

#
# NOTIFICATION FLAGS
#

DEEP_NOTIF_INFO = 0
DEEP_NOTIF_DEBUG = 1
DEEP_NOTIF_SUCCESS = 2
DEEP_NOTIF_WARNING = 3
DEEP_NOTIF_ERROR = 4
DEEP_NOTIF_FATAL = 5
DEEP_NOTIF_INPUT = 6
DEEP_NOTIF_RESULT = 7

#
# COMPUTER VISION LIBRARY
#

DEEP_LIB_OPENCV = 0
DEEP_LIB_PIL = 1

#
# HISTORY SAVING CONDITION
#

DEEP_SAVE_CONDITION_END_BATCH = 0         # Highly not recommended
DEEP_SAVE_CONDITION_END_EPOCH = 1
DEEP_SAVE_CONDITION_END_TRAINING = 2
DEEP_SAVE_CONDITION_AUTO = 3                # Highly recommended

#
# DATA MEMORIZATION CONDITION
#

DEEP_MEMORIZE_BATCHES = 0
DEEP_MEMORIZE_EPOCHS = 1


#
# VERBOSE
#

DEEP_VERBOSE_BATCH = 2
DEEP_VERBOSE_EPOCH = 1
DEEP_VERBOSE_TRAINING = 0

#
# SHUFFLE
#

DEEP_SHUFFLE_NONE = 0
DEEP_SHUFFLE_ALL = 1
DEEP_SHUFFLE_BATCHES = 2

#
# SAVE NETWORK FORMAT
#

DEEP_SAVE_NET_FORMAT_ONNX = 0
DEEP_SAVE_NET_FORMAT_PYTORCH = 1

#
# NOTIFICATION STATEMENTS
#

FINISHED_TRAINING = "Finished training"
SUMMARY = "Summary"
TOTAL_LOSS = "Total Loss"
WALL_TIME = "Wall Time"
RELATIVE_TIME = "Relative Time"
EPOCH = "Epoch"
BATCH = "Batch"
TRAINING = "Training"
VALIDATION = "Validation"
TIME_FORMAT = "%Y:%m:%d:%H:%M:%S"
EPOCH_END = "End of Epoch [%i/%i]"
EPOCH_START = "Start of Epoch [%i/%i]"
HISTORY_SAVED = "History saved to %s"
