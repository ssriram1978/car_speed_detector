from speed_tracker import SpeedTracker
from constants import SPEED_ESTIMATION_DICT, POINTS, MILES_PER_ONE_KILOMETER, LIST_OF_SPEED_ZONES
import numpy as np
from car_speed_logging import logger
import cv2


class SpeedTrackerHandler:
    speed_tracking_dict = {}
    
    @classmethod
    def calculate_speed(cls, estimatedSpeeds):
	    # calculate the speed in KMPH and MPH
	    return np.average(estimatedSpeeds) * MILES_PER_ONE_KILOMETER
 
    @classmethod
    def draw_id_centroid_on_output_frame(cls, frame, centroid, objectID):
        # draw both the ID of the object and the centroid of the
        # object on the output frame
        text = "ID {}".format(objectID)
        cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10)
                    , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(frame, (centroid[0], centroid[1]), 4,
                   (0, 255, 0), -1)
    
    @classmethod
    def yield_a_speed_tracker_object(cls, objects):

        for (objectID, centroid) in objects.items():
            # check to see if a trackable object exists for the current
            # object ID
            speed_tracker_object = cls.speed_tracking_dict.get(objectID, None)

            # if there is no existing trackable object, create one
            if not speed_tracker_object:
                speed_tracker_object = SpeedTracker(objectID, centroid)
                if len(cls.speed_tracking_dict) > 100:
                    cls.speed_tracking_dict.clear()
            yield speed_tracker_object, objectID, centroid
        
    @classmethod
    def compute_speed(cls, frame, speed_tracked_object, objectID, centroid, ts, meter_per_pixel):
        #If a trackable object speed has not yet been estimated then estimate it
        cls.estimate_object_speed(speed_tracked_object, centroid, ts, meter_per_pixel)
        # store the trackable object in our dictionary
        cls.speed_tracking_dict[objectID] = speed_tracked_object
        cls.draw_id_centroid_on_output_frame(frame, centroid, objectID)

    @classmethod
    def fetch_speed_zones(cls, trackable_object, centroid):
        # check if the direction of the object has been set, if
        # not, calculate it, and set it
        if trackable_object.direction is None:
            y = [c[0] for c in trackable_object.centroids]
            trackable_object.direction = centroid[0] - np.mean(y)
        # if the direction is positive (indicating the object
        # is moving from left to right)
        if trackable_object.direction > 0:
            list_of_speed_zones = LIST_OF_SPEED_ZONES
        else:
            list_of_speed_zones = LIST_OF_SPEED_ZONES[::-1]
        return list_of_speed_zones
    
    @classmethod
    def estimate_trackable_object(cls, trackable_object, centroid, ts):
        empty_slot = -1
        current_index = -1
        for index, speed_zone in enumerate(cls.fetch_speed_zones(trackable_object, centroid)):
            if speed_zone not in trackable_object.timestamp:
                empty_slot = speed_zone
                current_index = index
                break
        if empty_slot == -1:
            logger().error("Unable to find an empty slot in the trackable_object timestamp.")
            return
        if centroid[0] > SPEED_ESTIMATION_DICT[empty_slot]:
            trackable_object.timestamp[empty_slot] = ts
            trackable_object.position[empty_slot] = centroid[0]
            if current_index == len(LIST_OF_SPEED_ZONES)-1:
                trackable_object.lastPoint = True
    
    @classmethod
    def calculate_distance_in_pixels(cls, start, end, trackable_object, meter_per_pixel, estimated_speeds):
        # calculate the distance in pixels
        d = trackable_object.position[end] - trackable_object.position[start]
        distance_in_pixels = abs(d)
        # check if the distance in pixels is zero, if so,
        # skip this iteration
        if distance_in_pixels == 0:
           return
        # calculate the time in hours
        t = trackable_object.timestamp[end] - trackable_object.timestamp[start]
        time_in_seconds = abs(t.total_seconds())
        time_in_hours = time_in_seconds / (60 * 60)
        # calculate distance in kilometers and append the
        # calculated speed to the list
        distance_in_meters = distance_in_pixels * meter_per_pixel
        distance_in_km = distance_in_meters / 1000
        estimated_speeds.append(distance_in_km / time_in_hours)
    
    @classmethod
    def estimate_object_speed(cls, trackable_object, centroid, ts, meter_per_pixel):
        if not trackable_object.estimated:
            cls.estimate_trackable_object(trackable_object, centroid, ts)
            # check to see if the vehicle is past the last point and
            # the vehicle's speed has not yet been estimated, if yes,
            # then calculate the vehicle speed and log it if it's
            # over the limit
            if trackable_object.lastPoint:
                # initialize the list of estimated speeds
                estimated_speeds = []
                # loop over all the pairs of points and estimate the
                # vehicle speed
                for (start, end) in POINTS:
                    cls.calculate_distance_in_pixels(start, end, trackable_object, meter_per_pixel, estimated_speeds)
                # calculate the average speed
                trackable_object.calculate_speed(estimated_speeds)
                # set the object as estimated
                trackable_object.estimated = True
                logger().info("Speed of the vehicle that just passed" \
                      " is: {:.2f} MPH".format(trackable_object.speedMPH))
