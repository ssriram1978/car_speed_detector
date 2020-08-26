# import the necessary packages
import numpy as np
from car_speed_detector.constants import MILES_PER_ONE_KILOMETER

class SpeedTracker:
	def __init__(self, objectID, centroid):
		# store the object ID, then initialize a list of centroids
		# using the current centroid
		self.objectID = objectID
		self.centroids = [centroid]

		# initialize a lists to store the timestamp and
		# position of the object at various points
		self.timestamp_list = []
		self.position_list = []
		self.current_index = -1
		self.empty_recorded_timestamp = None
		
		# initialize the object speeds in MPH and KMPH
		self.speedMPH = None
		self.speedKMPH = None

		# initialize two booleans, (1) used to indicate if the
		# object's speed has already been estimated or not, and (2)
		# used to indidicate if the object's speed has been logged or
		# not
		self.estimated = False
		self.logged = False

		# initialize the direction of the object
		self.direction = None

	def calculate_speed(self, estimatedSpeeds):
		# calculate the speed in KMPH and MPH
                for index, value in enumerate(estimatedSpeeds[:]):
                    if value == 0:
                        del estimatedSpeeds[index]
                self.speedKMPH = np.average(estimatedSpeeds)
                self.speedMPH = self.speedKMPH * MILES_PER_ONE_KILOMETER
