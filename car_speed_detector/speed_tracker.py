# This class servers as a common place to store all the centroids, timestamp, position and speed computed for a
# identified object.
import numpy as np
from car_speed_detector.constants import MILES_PER_ONE_KILOMETER, SPIKE_THRESHOLD
from car_speed_detector.car_speed_logging import logger


class SpeedTracker:
    """
    This class is used to store all those variables used to compute speed for a trackable object.
    """
    def __init__(self, object_id, centroid):
        # store the object ID, then initialize a list of centroids
        # using the current centroid
        self.object_id = object_id

        # Store the first centroid object into the centroids list.
        # Subsequent centroids SHALL be appended to the centroids list.
        self.centroids = [centroid]

        self.estimated_speed_list = []

        # initialize a lists to store the timestamp and
        # position of the object at various points
        self.timestamp_list = []

        # Used to record the timestamp for inactivity of the centroid object.
        self.empty_recorded_timestamp = None

        # initialize the object speeds in MPH and KMPH
        self.speedMPH = None
        self.speedMPH_list = []
        # initialize two booleans, (1) used to indicate if the
        # object's speed has already been estimated or not, and (2)
        # used to indicate if the object's speed has been logged or
        # not
        self.estimated = False
        self.logged = False

        # initialize the direction of the object
        self.direction = None

        # Tracked object frame.
        self.tracked_object_frame_list = []

    def compute_average_speed(self):
        """
        This method calculates speed by averaging the list of estimated speeds.
        """
        # calculate the speed in MPH
        self.speedMPH_list = list(map(lambda x: x*MILES_PER_ONE_KILOMETER, self.estimated_speed_list))
        logger().info("self.speedMPH_list = {}".format(self.speedMPH_list))
        if len(self.speedMPH_list) <=1:
            return
        # Filter out skewed up values.
        # Filter out values which are greater than its predecessor by a large value. Example: If the speedMPH_list = [1,2,1,100,2] remove 100 from this list bec ause 100 is skewed up than its predecessor by a large spike.
        temp_speedMPH_list = []
        for index in range(len(self.speedMPH_list)):
            if index == 0 and abs(self.speedMPH_list[index] - self.speedMPH_list[index+1]) < SPIKE_THRESHOLD:
                temp_speedMPH_list.append(self.speedMPH_list[index])
            elif index == len(self.speedMPH_list)-1 and abs(self.speedMPH_list[index] - self.speedMPH_list[index-1]) < SPIKE_THRESHOLD :
                temp_speedMPH_list.append(self.speedMPH_list[index])
            elif abs(self.speedMPH_list[index]-self.speedMPH_list[index+1]) < SPIKE_THRESHOLD and abs(self.speedMPH_list[index] - self.speedMPH_list[index-1]) < SPIKE_THRESHOLD:
                temp_speedMPH_list.append(self.speedMPH_list[index])
        self.speedMPH_list = temp_speedMPH_list
        logger().info("spike corrected self.speedMPH_list = {}".format(self.speedMPH_list))
        self.speedMPH = np.average(self.speedMPH_list)

