# This class is used to compute the speed for a centroid object.

from datetime import datetime

import cv2
import numpy as np
from car_speed_detector.car_speed_logging import logger
from car_speed_detector.constants import (DISCARD_SPEED_VALUE,
                                          MILES_PER_ONE_KILOMETER, TIMEOUT_FOR_TRACKER, MID_POINT_IN_THE_FRAME,
                                          Direction, MIN_COLUMN_MOVEMENT_TO_DETERMINE_DIRECTION)
from car_speed_detector.speed_tracker import SpeedTracker
from car_speed_detector.speed_validator import SpeedValidator


class SpeedTrackerHandler:
    speed_tracking_dict = {}

    @classmethod
    def yield_a_speed_tracker_object(cls, centroid_tracker_dict):
        """
        Yields a speed tracker object.
        :param centroid_tracker_dict: dict
        :return:
        """
        for (object_id, centroid) in centroid_tracker_dict.items():
            # check to see if a trackable object exists for the current
            # object ID
            speed_tracker_object = cls.speed_tracking_dict.get(object_id, None)

            # if there is no existing trackable object, create one
            if not speed_tracker_object:
                speed_tracker_object = SpeedTracker(object_id, centroid)
            else:
                speed_tracker_object.centroids.append(centroid)
            speed_tracker_object.timestamp_list.append(datetime.now())
            yield speed_tracker_object
        yield []

    @classmethod
    def __clear_object_from_speed_tracking_dict(cls, object_id):
        del (cls.speed_tracking_dict[object_id])

    @classmethod
    def __handle_zero_time_stamp_list(cls, speed_tracker_object):
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
                logger().debug("Deleting object_id {} for empty timestamp "
                               "from the speed_tracking_dict.".format(
                                speed_tracker_object.object_id))
                cls.__clear_object_from_speed_tracking_dict(speed_tracker_object.object_id)
        else:
            speed_tracker_object.empty_recorded_timestamp = datetime.now()

    @classmethod
    def __handle_the_case_where_grace_time_for_tracking_is_over(cls, now, speed_tracker_object):
        """
        This method handles the case where the grace time (TIMEOUT_FOR_TRACKER) for the tracker object is over.
        :param now: timestamp
        :param speed_tracker_object: Instance of type SpeedTracker.
        :return:
        """
        if speed_tracker_object.logged:
            # Delete this object from speed tracking dict.
            logger().info("Deleting object_id {} from the human_tracking_dict.".format(
                speed_tracker_object.object_id))
            cls.__clear_object_from_speed_tracking_dict(speed_tracker_object.object_id)

    @classmethod
    def compute_speed_for_dangling_object_ids(cls, keep_dict_items=False):
        """
        This method computes speed for dangling objects found in speed_tracking_dict.
        This can happen when the car was tracked only at a few sampling points (column traversal).
        :return:
        """
        for object_id, car_tracker_object in cls.speed_tracking_dict.copy().items():
            if len(car_tracker_object.timestamp_list) == 0:
                cls.__handle_zero_time_stamp_list(car_tracker_object)
                return
            now = datetime.now()
            duration = now - car_tracker_object.timestamp_list[-1]
            if duration.total_seconds() > TIMEOUT_FOR_TRACKER:
                if not car_tracker_object.estimated:
                    # set the object as estimated
                    car_tracker_object.estimated = True
                    if car_tracker_object.speedMPH <= DISCARD_SPEED_VALUE:
                        # set the object has logged
                        car_tracker_object.logged = True
                        #cls.__handle_the_case_where_grace_time_for_tracking_is_over(now, car_tracker_object)
                        continue
                    else:
                        logger().info(
                        "Speed of the vehicle {} that just passed is: {:.2f} MPH".format(car_tracker_object.object_id,
                                                                                         car_tracker_object.speedMPH))
                SpeedValidator.validate_speed(car_tracker_object)
                if not keep_dict_items:
                    cls.__handle_the_case_where_grace_time_for_tracking_is_over(now, car_tracker_object)

    @classmethod
    def get_direction_for_first_centroid_object(cls):
        """
        Used for unit testing purpose.
        :return:
        """
        return repr(cls.speed_tracking_dict[0].direction)

    @classmethod
    def get_direction_for_this_centroid_object(cls, object_id):
        """
        Used for unit testing purpose.
        :return:
        """
        return repr(cls.speed_tracking_dict[object_id].direction)

    @classmethod
    def get_computed_speed_for_the_first_centroid_object(cls):
        """
        Fetches speed computed for the first centroid object.
        :return:
        """
        return cls.speed_tracking_dict[0].speedMPH

    @classmethod
    def get_computed_speed_for_the_this_centroid_object(cls, centroid_object_id):
        """
        Fetches speed computed for the first centroid object.
        :return:
        """
        return cls.speed_tracking_dict[centroid_object_id].speedMPH

    @classmethod
    def estimate_object_speed(cls, frame, trackable_object, meter_per_pixel):
        """
        Estimate speed for the trackable object.
        1. It first records important parameters from the trackable object.
        2. It computes the speed if we have sufficient sampled data.
        :param frame: frame
        :param trackable_object: Instance of type Speed Tracker.
        :param meter_per_pixel: meter per pixel
        :return:
        """
        if trackable_object:
            cls.__compute_direction(trackable_object)
            # check to see if the vehicle is past the last point and
            # the vehicle's speed has not yet been estimated, if yes,
            # then calculate the vehicle speed and log it if it's
            # over the limit
            cls.__compute_speed(trackable_object, frame, meter_per_pixel)
            cls.speed_tracking_dict[trackable_object.object_id] = trackable_object

    @classmethod
    def __compute_direction(cls, trackable_object):
        # check if the direction of the object has been set, if
        # not, calculate it, and set it
        if trackable_object.direction is None:
            pass
        if len(trackable_object.centroids) > 1:
            tracker_column_movement = abs(trackable_object.centroids[-1][0] - trackable_object.centroids[-2][0])
            if trackable_object.centroids[-1][0] >= trackable_object.centroids[-2][0]:
                if trackable_object.direction != Direction.LEFT_TO_RIGHT and \
                        tracker_column_movement > MIN_COLUMN_MOVEMENT_TO_DETERMINE_DIRECTION:

                    logger().error("Correcting the Computed direction of trackable object id {} to be {}".format(
                                   trackable_object.object_id, repr(Direction.LEFT_TO_RIGHT)))
                    trackable_object.direction = Direction.LEFT_TO_RIGHT
            else:
                if trackable_object.direction != Direction.RIGHT_TO_LEFT and \
                        tracker_column_movement > MIN_COLUMN_MOVEMENT_TO_DETERMINE_DIRECTION:
                    logger().error("Correcting the Computed direction of trackable object id {} to be {}".format(
                                   trackable_object.object_id, repr(Direction.RIGHT_TO_LEFT)))
                    trackable_object.direction = Direction.RIGHT_TO_LEFT
        else:
            if trackable_object.centroids[-1][0] <= MID_POINT_IN_THE_FRAME:
                trackable_object.direction = Direction.LEFT_TO_RIGHT
            else:
                trackable_object.direction = Direction.RIGHT_TO_LEFT
            logger().info("Computed direction of trackable object id {} to be {}".format(
                trackable_object.object_id, repr(trackable_object.direction)))

    @classmethod
    def __compute_speed(cls, trackable_object, frame, meter_per_pixel):
        """
        This method measures speed.
        :param trackable_object: Instance of type Speed Tracker.
        :param meter_per_pixel: meter per pixel
        :return:
        """
        cls.__calculate_distance_in_pixels(trackable_object, meter_per_pixel)
        trackable_object.compute_average_speed()
        cls.__draw_id_centroid_on_output_frame(frame, trackable_object.centroids, trackable_object.object_id)
        trackable_object.tracked_object_frame_list.append(frame)

    @classmethod
    def __draw_id_centroid_on_output_frame(cls, frame, centroids, object_id):
        # draw both the ID of the object and the centroid of the
        # object on the output frame
        if len(centroids) <= 1:
            return
        text = "ID {}".format(object_id)
        cv2.putText(frame, text, (centroids[-1][0] - 10, centroids[-1][1] - 10)
                    , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(frame, (centroids[-1][0], centroids[-1][1]), 4,
                   (0, 255, 0), -1)

    @classmethod
    def __calculate_distance_in_pixels(cls, trackable_object, meter_per_pixel):
        if len(trackable_object.centroids) <= 1:
            return
        d = trackable_object.centroids[-1][0] - trackable_object.centroids[-2][0]
        distance_in_pixels = abs(d)
        # check if the distance in pixels is zero, if so,
        # skip this iteration
        if distance_in_pixels == 0:
            return
        t = trackable_object.timestamp_list[-1] - trackable_object.timestamp_list[-2]
        time_in_seconds = abs(t.total_seconds())
        time_in_hours = time_in_seconds / (60 * 60)
        # calculate distance in kilometers and append the
        # calculated speed to the list
        distance_in_meters = distance_in_pixels * meter_per_pixel
        distance_in_km = distance_in_meters / 1000
        trackable_object.estimated_speed_list.append(distance_in_km / time_in_hours)
