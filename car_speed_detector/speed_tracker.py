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
        self.objectID = object_id

        # Store the first centroid object into the centroids list.
        # Subsequent centroids SHALL be appended to the centroids list.
        self.centroids = [centroid]

        # initialize a lists to store the timestamp and
        # position of the object at various points
        self.timestamp_list = []

        # Store the position list corresponding to each centroid found in centroids list.
        self.position_list = []

        # Used to find the current index from the position list.
        self.current_index = -1

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


def calculate_speed(self, estimated_speeds):
    # calculate the speed in KMPH and MPH
    for index, value in enumerate(estimated_speeds[:]):
        if value == 0:
            del estimated_speeds[index]
    self.speedKMPH = np.average(estimated_speeds)
    self.speedMPH = self.speedKMPH * MILES_PER_ONE_KILOMETER
