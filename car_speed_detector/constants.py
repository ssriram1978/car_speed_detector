PACKAGE_NAME = "speed_detector"

# object detection model
MODEL_NAME = "MobileNetSSD_deploy.caffemodel"

# Log file name
LOG_FILE_NAME = "speed_detector.csv"

# proto text file of the object detection model
PROTO_TEXT_FILE = "MobileNetSSD_deploy.prototxt"

# Max threshold for Speed in miles/hour
MAX_THRESHOLD_SPEED = 15

# Distance of the camera from the road.
DISTANCE_OF_CAMERA_FROM_ROAD = 16

# Frame width.
FRAME_WIDTH_IN_PIXELS = 400

# Maximum consecutive frames a given object is allowed to be
# marked as "disappeared" until we need to deregister the object from tracking.
MAX_NUM_OF_CONSECUTIVE_FRAMES_FOR_ACTION = 10

# Maximum distance between centroids to associate an object --
# if the distance is larger than this maximum distance we'll
# start to mark the object as "disappeared".
MAX_DISTANCE_FROM_THE_OBJECT = 175

# dictionary holding the different speed estimation columns
SPEED_ESTIMATION_DICT = {"1st Zone": 120,
                        "2nd Zone": 160,
                        "3rd Zone": 200,
                        "4th Zone": 240}

LIST_OF_SPEED_ZONES = ["1st Zone", "2nd Zone", "3rd Zone", "4th Zone"]

# number of frames to perform object tracking instead of object detection.
MAX_NUM_OF_FRAMES_FOR_OBJECT_TRACKER = 4

# minimum confidence
MIN_CONFIDENCE = 0.4

# initialize the list of various points used to calculate the avg of
# the vehicle speed
POINTS = [("1st Zone", "2nd Zone"),
         ("2nd Zone", "3rd Zone"),
         ("3rd Zone", "4th Zone")]

MILES_PER_ONE_KILOMETER = 0.621371

# initialize the list of class labels MobileNet SSD was trained to
# detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
          "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
          "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
          "sofa", "train", "tvmonitor"]

OPEN_DISPLAY = True

SEND_EMAIL = True
