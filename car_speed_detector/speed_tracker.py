# This class servers as a common place to store all the centroids, timestamp, position and speed computed for a
# identified object.
import numpy as np
from car_speed_detector.constants import MILES_PER_ONE_KILOMETER


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
        self.speedKMPH = None

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
        # calculate the speed in KMPH and MPH
        self.speedKMPH = np.average(self.estimated_speed_list)
        self.speedMPH = self.speedKMPH * MILES_PER_ONE_KILOMETER
