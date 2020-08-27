from datetime import datetime

import cv2
import numpy as np
from car_speed_detector.car_speed_logging import logger
from car_speed_detector.constants import SPEED_ESTIMATION_LIST, MILES_PER_ONE_KILOMETER, TIMEOUT_FOR_TRACKER
from car_speed_detector.speed_tracker import SpeedTracker


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
            else:
                speed_tracker_object.centroids.append(centroid)
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
            list_of_speed_zones = SPEED_ESTIMATION_LIST
        else:
            list_of_speed_zones = SPEED_ESTIMATION_LIST[::-1]
        return list_of_speed_zones
    
    @classmethod
    def estimate_trackable_object(cls, trackable_object, centroid, ts):
        if trackable_object.current_index == -1:
            #initialize it for the first time to 0.
            trackable_object.current_index = 0
        elif trackable_object.current_index == len(SPEED_ESTIMATION_LIST):
            error_str = "Unable to find an empty slot in the trackable_object timestamp."
            logger().error(error_str)
            raise ValueError
        
        if centroid[0] > SPEED_ESTIMATION_LIST[trackable_object.current_index]:
            logger().debug("Recording timestamp and centroid at column {}".format(SPEED_ESTIMATION_LIST[trackable_object.current_index]))
            trackable_object.timestamp_list.append(ts)
            trackable_object.position_list.append(centroid[0])
            trackable_object.current_index += 1

    @classmethod
    def clear_object_from_speed_tracking_dict(cls, object_id):
        del (cls.speed_tracking_dict[object_id])

    @classmethod
    def handle_zero_time_stamp_list(cls, speed_tracker_object):
        """
        This method is invoked when there is no timestamp recorded for this tracker.
        In this case, this method initially computes the current time and stores it in empty_recorded_timestamp.
        Since the grace period (TIMEOUT_FOR_TRACKER) is already over, this method deletes the tracker object
        from the speed_tracking_dict.
        :param speed_tracker_object: Instance of type SpeedTracker.
        :return:
        """
        if speed_tracker_object.empty_recorded_timestamp:
            now = datetime.now()
            duration = now - speed_tracker_object.empty_recorded_timestamp
            if duration.total_seconds() > TIMEOUT_FOR_TRACKER:
                logger().debug("Deleting objectId {} for empty timestamp "
                                     "from the speed_tracking_dict.".format(
                                     speed_tracker_object.objectID))
                cls.clear_object_from_speed_tracking_dict(speed_tracker_object.objectID)
        else:
            speed_tracker_object.empty_recorded_timestamp = datetime.now()

    @classmethod
    def handle_the_case_where_grace_time_for_tracking_is_over(cls, now, speed_tracker_object):
        """
        This method handles the case where the grace time (TIMEOUT_FOR_TRACKER) for the tracker object is over.
        :param now: timestamp
        :param speed_tracker_object: Instance of type SpeedTracker.
        :return:
        """
        if speed_tracker_object.estimated and speed_tracker_object.logged:
            # Delete this object from speed tracking dict.
            logger().info("Deleting objectId {} from the human_tracking_dict.".format(
                speed_tracker_object.objectID))
            cls.clear_object_from_speed_tracking_dict(speed_tracker_object.objectID)

    @classmethod
    def compute_speed_for_dangling_object_ids(cls):
        """
        This method computes speed for dangling objects found in speed_tracking_dict.
        This can happen when the car was tracked only at a few sampling points (column traversal).
        :return:
        """
        for object_id, car_tracker_object in cls.speed_tracking_dict.copy().items():
            if len(car_tracker_object.timestamp_list) == 0:
                cls.handle_zero_time_stamp_list(car_tracker_object)
                return
            now = datetime.now()
            duration = now - car_tracker_object.timestamp_list[-1]
            if duration.total_seconds() > TIMEOUT_FOR_TRACKER:
                cls.handle_the_case_where_grace_time_for_tracking_is_over(now, car_tracker_object)

    @classmethod
    def calculate_distance_in_pixels(cls, start, end, trackable_object, meter_per_pixel, estimated_speeds):
        # calculate the distance in pixels
        logger().debug("position_list={}".format(trackable_object.position_list))
        d = trackable_object.position_list[end] - trackable_object.position_list[start]
        distance_in_pixels = abs(d)
        # check if the distance in pixels is zero, if so,
        # skip this iteration
        if distance_in_pixels == 0:
            estimated_speeds.append(0)
            return
        # calculate the time in hours
        t = trackable_object.timestamp_list[end] - trackable_object.timestamp_list[start]
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
            if trackable_object.current_index == len(SPEED_ESTIMATION_LIST):
                # initialize the list of estimated speeds
                estimated_speeds = []
                # loop over all the pairs of points and estimate the
                # vehicle speed
                for index in range(len(SPEED_ESTIMATION_LIST)-1):
                    start = index
                    end = index + 1
                    logger().debug("start={},end={}".format(start, end))
                    cls.calculate_distance_in_pixels(start, end, trackable_object, meter_per_pixel, estimated_speeds)
                # calculate the average speed
                for index in range(len(SPEED_ESTIMATION_LIST)-1):
                    logger().info("Between column indices {} to {}, measured speed = {}".format(SPEED_ESTIMATION_LIST[index], SPEED_ESTIMATION_LIST[index+1],estimated_speeds[index] * MILES_PER_ONE_KILOMETER))
                trackable_object.calculate_speed(estimated_speeds)
                # set the object as estimated
                trackable_object.estimated = True
                logger().info("Speed of the vehicle that just passed" \
                      " is: {:.2f} MPH".format(trackable_object.speedMPH))
                
