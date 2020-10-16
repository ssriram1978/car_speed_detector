#!/usr/bin/env python3
import argparse
import os
import time
from datetime import datetime
import sys, traceback
import cv2
import imutils
from car_speed_detector.exception_handler import NoFrameFromVideoStreamException
from car_speed_detector.car_speed_logging import logger
from car_speed_detector.centroid_object_creator import CentroidObjectCreator
# import the necessary packages
from car_speed_detector.constants import PROTO_TEXT_FILE, MODEL_NAME, FRAME_WIDTH_IN_PIXELS, \
    DISTANCE_OF_CAMERA_FROM_ROAD, TIMEOUT_FOR_TRACKER, VIDEO_DEV_ID
from car_speed_detector.speed_tracker_handler import SpeedTrackerHandler
from car_speed_detector.speed_validator import SpeedValidator
from car_speed_detector.speed_tracker import SpeedTracker
from imutils.video import FPS
from imutils.video import VideoStream


class SpeedDetector:
    def __init__(self, estimate_speed_from_video_file_name=None, use_pi_camera=True, open_display=True):
        # initialize the frame dimensions (we'll set them as soon as we read
        # the first frame from the video)
        self.height_of_frame = None
        self.width_of_frame = None
        self.video_stream = None
        self.net = None
        self.current_time_stamp = None
        self.frame = None
        self.rgb = None
        self.meter_per_pixel = None
        self.args = None
        self.estimate_speed_from_video_file_name = estimate_speed_from_video_file_name
        self.__perform_speed_detection = True
        self.open_display = open_display

        # Parse input arguments
        self.parse_input_arguments()

        # Load Model
        self.load_model(use_pi_camera)
        # Initialize the camera.
        self.initialize_camera(use_pi_camera)

        # start the frames per second throughput estimator
        self.frames_per_second = 0
        self.fps_instance = FPS()
        self.fps_instance.start()
        self.fps_instance.stop()
        self.centroid_object_creator = CentroidObjectCreator()

    def parse_input_arguments(self):
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--input", required=False, default="",
                        help="Path to the input video file")
        self.args = vars(ap.parse_args())
        if len(self.args["input"]):
            self.estimate_speed_from_video_file_name = self.args["input"]

    def load_model(self, use_pi_camera):
        """
        Load our serialized model from disk
        """
        logger().info("Loading model name:{}, proto_text:{}.".format(MODEL_NAME, PROTO_TEXT_FILE))
        self.net = cv2.dnn.readNetFromCaffe(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            PROTO_TEXT_FILE),
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                MODEL_NAME))

        if use_pi_camera:
            # Set the target to the MOVIDIUS NCS stick connected via USB
            # Prerequisite: https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_raspbian.html
            logger().info("Setting MOVIDIUS NCS stick connected via USB as the target to run the model.")
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
        else:
            logger().info("Setting target to CPU.")
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def initialize_camera(self, use_pi_camera):
        """
        Initialize the video stream and allow the camera sensor to warmup.
        """
        if self.estimate_speed_from_video_file_name:
            self.estimate_speed_from_video_file_name = \
                os.path.join(os.path.dirname(__file__),
                             self.estimate_speed_from_video_file_name)
            logger().info("Reading the input video file {}.".format(self.estimate_speed_from_video_file_name))

            self.video_stream = cv2.VideoCapture(self.estimate_speed_from_video_file_name)
            if not self.video_stream:
                logger().error("cv2.VideoCapture() returned None.")
                raise ValueError
            # self.video_stream.set(cv2.CAP_PROP_FPS, int(10))
        elif use_pi_camera:
            logger().info("Warming up Raspberry PI camera connected via the PCB slot.")
            self.video_stream = VideoStream(usePiCamera=True).start()
        else:
            logger().debug("Setting video capture device to {}.".format(VIDEO_DEV_ID))
            self.video_stream = VideoStream(src=VIDEO_DEV_ID).start()
        time.sleep(2.0)
        # vs = VideoStream(src=0).start()

    def grab_next_frame(self):
        """
        1. Grab the next frame from the stream.
        2. store the current timestamp, and store the new date.
        """
        if self.estimate_speed_from_video_file_name:
            if self.video_stream.isOpened():
                ret, self.frame = self.video_stream.read()
            else:
                logger().info("Unable to open video stream...")
                raise ValueError
        else:
            self.frame = self.video_stream.read()
        if self.frame is None:
            if self.estimate_speed_from_video_file_name:
                for _ in range(TIMEOUT_FOR_TRACKER + 1):
                    SpeedTrackerHandler.compute_speed_for_dangling_object_ids(keep_dict_items=True)
                    time.sleep(1)
                self.__perform_speed_detection = False
            else:
                logger().error("No frames from video stream.")
                raise NoFrameFromVideoStreamException("No frames from video stream.")
            return
        if self.fps_instance.elapsed() >= 1:
            self.frames_per_second = self.fps_instance.fps()
            self.fps_instance.start()
        self.fps_instance.update()
        self.fps_instance.stop()

        self.current_time_stamp = datetime.now()
        # resize the frame
        self.frame = imutils.resize(self.frame, width=FRAME_WIDTH_IN_PIXELS)
        # width = FRAME_WIDTH_IN_PIXELS
        # height = self.frame.shape[0] # keep original height
        # dim = (width, height)
        # self.frame = cv2.resize(self.frame, dim, interpolation = cv2.INTER_AREA)
        self.rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

    def set_frame_dimensions(self):
        """
        If the frame dimensions are empty, set them.
        """
        # if the frame dimensions are empty, set them
        if not self.width_of_frame or not self.height_of_frame:
            (self.height_of_frame, self.width_of_frame) = self.frame.shape[:2]
            self.meter_per_pixel = DISTANCE_OF_CAMERA_FROM_ROAD / self.width_of_frame

    def get_direction(self):
        """
        Used in unit testing.
        Returns the computed direction for the first found centroid tracker from the dictionary.
        :return:
        """
        return SpeedTrackerHandler.get_direction_for_first_centroid_object()

    def get_speed_dict(self):
        """
        Get the speed dict.
        :return:
        """
        return SpeedTrackerHandler.speed_tracking_dict

    def get_computed_speed(self):
        """
        Used in unit testing.
        Returns the computed speed.
        :return:
        """
        return SpeedTrackerHandler.get_computed_speed_for_the_first_centroid_object()

    def loop_over_streams(self):
        while self.__perform_speed_detection:
            self.grab_next_frame()
            # check if the frame is None, if so, break out of the loop
            if self.frame is None:
                if self.estimate_speed_from_video_file_name:
                    self.__perform_speed_detection = False
                break
            self.set_frame_dimensions()
            centroid_object_dict = self.centroid_object_creator.create_centroid_tracker_object(self.height_of_frame,
                                                                                  self.width_of_frame, self.rgb,
                                                                                  self.net,
                                                                                  self.frame)
            for speed_tracked_object in SpeedTrackerHandler.yield_a_speed_tracker_object(
                    centroid_object_dict):
                if not isinstance(speed_tracked_object, SpeedTracker):
                    continue
                SpeedTrackerHandler.estimate_object_speed(self.frame, speed_tracked_object, self.meter_per_pixel)

            SpeedTrackerHandler.compute_speed_for_dangling_object_ids()

            # if the *display* flag is set, then display the current frame
            # to the screen and record if a user presses a key
            if self.open_display:
                cv2.imshow("FPS={:.2f}".format(self.frames_per_second), self.frame)
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key is pressed, break from the loop
                if key == ord("q"):
                    break

    def clean_up(self):
        self.__perform_speed_detection = False
        # stop the timer and display FPS information
        self.fps_instance.stop()
        logger().info("elapsed time: {:.2f}".format(self.fps_instance.elapsed()))
        logger().info("approx. FPS: {:.2f}".format(self.fps_instance.fps()))

        # Close the log file.
        SpeedValidator.close_log_file()

        # close any open windows
        cv2.destroyAllWindows()

        # clean up
        logger().info("cleaning up...")
        if self.estimate_speed_from_video_file_name:
            self.video_stream.release()
        else:
            self.video_stream.stop()

    def perform_speed_detection(self):
        """
        This method computes speed detection by looping over the video stream.
        :return: True or False.
        """
        return_value = True
        while self.__perform_speed_detection:
            try:
                self.loop_over_streams()
            except Exception as e:
                logger().error("Caught an exception while looping over streams {}, rebooting....".format(
                    type(e).__name__ + ': ' + str(e)))
                print("Exception in user code:")
                print("-" * 60)
                traceback.print_exc(file=sys.stdout)
                print("-" * 60)
                return_value = False
                os.system("sudo reboot")
        return  return_value


if __name__ == "__main__":
    # time.sleep(60)
    SpeedDetector().perform_speed_detection()
