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

# Discard value for speed.
DISCARD_SPEED_VALUE = 5

VIDEO_DEV_ID = 0
# Distance of the camera from the road. This is measured in meters (not feet).
DISTANCE_OF_CAMERA_FROM_ROAD = 10

# Frame width.
FRAME_WIDTH_IN_PIXELS = 400

# Mid point in the frame.
MID_POINT_IN_THE_FRAME = 200

# Maximum consecutive frames a given object is allowed to be
# marked as "disappeared" until we need to deregister the object from tracking.
MAX_NUM_OF_CONSECUTIVE_FRAMES_FOR_ACTION = 10

# Maximum distance between centroids to associate an object --
# if the distance is larger than this maximum distance we'll
# start to mark the object as "disappeared".
MAX_DISTANCE_FROM_THE_OBJECT = 175

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

OPEN_DISPLAY = False

SPIKE_THRESHOLD = 50 

SEND_EMAIL = True

SEND_WHATS_APP = True

TIMEOUT_FOR_TRACKER = 3

TEMP_FILE = 'temp_file'
IMAGE_NAME = 'image_name'
LOG_FILE = 'log_file'
CAR_SPEED = 'speed'
SPEEDING_CAR_IMAGE = 'image_path'

USERNAME = 'username'
PASSWORD = 'password'


class Direction(Enum):
    LEFT_TO_RIGHT = 1
    RIGHT_TO_LEFT = 2


MIN_COLUMN_MOVEMENT_TO_DETERMINE_DIRECTION = 1

WHATSAPP_CHAT_GROUP_NAME = "ML for kids"

BROWSER_LOCATION = "/usr/bin/google-chrome"

BROWSER_EXECUTABLE_PATH = "/home/sriramsridhar/Downloads/chromedriver"
