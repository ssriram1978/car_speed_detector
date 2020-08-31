from enum import Enum

PACKAGE_NAME = "speed_detector"

# object detection model
MODEL_NAME = "MobileNetSSD_deploy.caffemodel"

# Log file name
LOG_FILE_NAME = "speed_detector.csv"

# proto text file of the object detection model
PROTO_TEXT_FILE = "MobileNetSSD_deploy.prototxt"

# Max threshold for Speed in miles/hour
MAX_THRESHOLD_SPEED = 5

VIDEO_DEV_ID = 0
# Distance of the camera from the road.
DISTANCE_OF_CAMERA_FROM_ROAD = 20

# Frame width.
FRAME_WIDTH_IN_PIXELS = 400

# Maximum consecutive frames a given object is allowed to be
# marked as "disappeared" until we need to deregister the object from tracking.
MAX_NUM_OF_CONSECUTIVE_FRAMES_FOR_ACTION = 10

# Maximum distance between centroids to associate an object --
# if the distance is larger than this maximum distance we'll
# start to mark the object as "disappeared".
MAX_DISTANCE_FROM_THE_OBJECT = 175

# list holding the different speed estimation column index.
# For example, first timestamp is stored at column index 60 and so on...
SPEED_ESTIMATION_LIST = [60, 120, 180, 240]

# number of frames to perform object tracking instead of object detection.
MAX_NUM_OF_FRAMES_FOR_OBJECT_TRACKER = 4

# minimum confidence (set at 40% now)
MIN_CONFIDENCE = 0.4

MILES_PER_ONE_KILOMETER = 0.621371

# initialize the list of class labels MobileNet SSD was trained to
# detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

OPEN_DISPLAY = True

SEND_EMAIL = True

TIMEOUT_FOR_TRACKER = 10


class Direction(Enum):
    LEFT_TO_RIGHT = 1
    RIGHT_TO_LEFT = 2


MIN_COLUMN_MOVEMENT_TO_DETERMINE_DIRECTION = 1
