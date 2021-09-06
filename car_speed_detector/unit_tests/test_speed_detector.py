# This file is used to test the car speed detector functionality.

import unittest
from car_speed_detector.constants import Direction
import os
from car_speed_detector.speed_detector import SpeedDetector


class TestSpeedDetector(unittest.TestCase):
    """
    This class unit tests SpeedDetector class.
    """
    def __cleanup(self):
        for file in os.listdir(os.getcwd()):
            if file.endswith('.jpg'):
                os.remove(file)

    def test_speed_detector(self):
        speed_detector_inst = SpeedDetector(estimate_speed_from_video_file_name='sample_data/cars.mp4',
                                            use_pi_camera=False, open_display=True)
        self.assertEqual(speed_detector_inst.perform_speed_detection(), True)
        speed_detector_inst.clean_up()
        self.__cleanup()

    def test_left_to_right_direction_1(self):
        """
        This method validates the direction of movement of the speeding car and validates the speed.
        :return:
        """
        speed_detector_inst = SpeedDetector(
            estimate_speed_from_video_file_name='sample_data/left_to_right_car_movement1.mp4',
            use_pi_camera=False, open_display=False)
        self.assertEqual(speed_detector_inst.perform_speed_detection(), True)
        speed_dict = speed_detector_inst.get_speed_dict()
        self.assertEqual(speed_detector_inst.get_direction(), repr(Direction.LEFT_TO_RIGHT))
        self.assertLessEqual(speed_detector_inst.get_computed_speed(), 20)

        speed_detector_inst.clean_up()
        self.__cleanup()

    def test_left_to_right_direction_2(self):
        """
        This method validates the direction of movement of the speeding car and validates the speed.
        :return:
        """

        speed_detector_inst = SpeedDetector(
            estimate_speed_from_video_file_name='sample_data/left_to_right_car_movement2.mp4',
            use_pi_camera=False, open_display=False)
        self.assertEqual(speed_detector_inst.perform_speed_detection(), True)
        self.assertEqual(speed_detector_inst.get_direction(), repr(Direction.LEFT_TO_RIGHT))
        self.assertLessEqual(speed_detector_inst.get_computed_speed(), 27)
        speed_detector_inst.clean_up()
        self.__cleanup()

    def test_left_to_right_direction_3(self):
        """
        This method validates the direction of movement of the speeding car and validates the speed.
        :return:
        """

        speed_detector_inst = SpeedDetector(
            estimate_speed_from_video_file_name='sample_data/left_to_right_car_movement3.mp4',
            use_pi_camera=False, open_display=False)
        self.assertEqual(speed_detector_inst.perform_speed_detection(), True)
        self.assertEqual(speed_detector_inst.get_direction(), repr(Direction.LEFT_TO_RIGHT))
        self.assertLessEqual(speed_detector_inst.get_computed_speed(), 25)
        speed_detector_inst.clean_up()
        self.__cleanup()

    def test_right_to_left_direction_1(self):
        """
        This method validates the direction of movement of the speeding car and validates the speed.
        :return:
        """

        speed_detector_inst = SpeedDetector(
            estimate_speed_from_video_file_name='sample_data/right_to_left_car_movement1.mp4',
            use_pi_camera=False, open_display=False)
        self.assertEqual(speed_detector_inst.perform_speed_detection(), True)
        self.assertEqual(speed_detector_inst.get_direction(), repr(Direction.RIGHT_TO_LEFT))
        self.assertLessEqual(speed_detector_inst.get_computed_speed(), 25)
        speed_detector_inst.clean_up()
        self.__cleanup()

    def test_right_to_left_direction_2(self):
        """
        This method validates the direction of movement of the speeding car and validates the speed.
        :return:
        """

        speed_detector_inst = SpeedDetector(
            estimate_speed_from_video_file_name='sample_data/right_to_left_car_movement2.mp4',
                                            use_pi_camera=False, open_display=False)
        self.assertEqual(speed_detector_inst.perform_speed_detection(), True)
        self.assertLessEqual(speed_detector_inst.get_computed_speed(), 30)
        speed_detector_inst.clean_up()
        self.__cleanup()

    def test_font_view_10mph(self):
        """
        This method validates the direction of movement of the speeding car and validates the speed.
        :return:
        """

        speed_detector_inst = SpeedDetector(
            estimate_speed_from_video_file_name='sample_data/front_view_10mph 2.mp4',
            use_pi_camera=False, open_display=False)
        self.assertEqual(speed_detector_inst.perform_speed_detection(), True)
        # The centroid tracker object id = 3
        self.assertEqual(speed_detector_inst.get_direction_for_a_centroid_id(3), repr(Direction.LEFT_TO_RIGHT))
        self.assertLessEqual(speed_detector_inst.get_computed_speed_for_the_this_centroid_object(3), 15)
        speed_detector_inst.clean_up()
        self.__cleanup()

    def test_rear_view_15mph(self):
        """
        This method validates the direction of movement of the speeding car and validates the speed.
        :return:
        """

        speed_detector_inst = SpeedDetector(
            estimate_speed_from_video_file_name='sample_data/back_view_15mph.mp4',
            use_pi_camera=False, open_display=False)
        self.assertEqual(speed_detector_inst.perform_speed_detection(), True)
        # The centroid tracker object id = 0
        self.assertEqual(speed_detector_inst.get_direction_for_a_centroid_id(1), repr(Direction.RIGHT_TO_LEFT))
        self.assertLessEqual(speed_detector_inst.get_computed_speed_for_the_this_centroid_object(1), 18)
        speed_detector_inst.clean_up()
        self.__cleanup()

    def test_font_view_30mph(self):
        """
        This method validates the direction of movement of the speeding car and validates the speed.
        :return:
        """

        speed_detector_inst = SpeedDetector(
            estimate_speed_from_video_file_name='sample_data/front_view_30mph.mp4',
            use_pi_camera=False, open_display=False)
        self.assertEqual(speed_detector_inst.perform_speed_detection(), True)
        # The centroid tracker object id = 2
        self.assertEqual(speed_detector_inst.get_direction_for_a_centroid_id(2), repr(Direction.LEFT_TO_RIGHT))
        self.assertLessEqual(speed_detector_inst.get_computed_speed_for_the_this_centroid_object(2), 30)
        speed_detector_inst.clean_up()
        self.__cleanup()

    def test_rear_view_30mph(self):
        """
        This method validates the direction of movement of the speeding car and validates the speed.
        :return:
        """

        speed_detector_inst = SpeedDetector(
            estimate_speed_from_video_file_name='sample_data/back_view_30mph.mp4',
            use_pi_camera=False, open_display=False)
        self.assertEqual(speed_detector_inst.perform_speed_detection(), True)
        # The centroid tracker object id = 0
        self.assertEqual(speed_detector_inst.get_direction_for_a_centroid_id(1), repr(Direction.RIGHT_TO_LEFT))
        self.assertLessEqual(speed_detector_inst.get_computed_speed_for_the_this_centroid_object(1), 30)
        speed_detector_inst.clean_up()
        self.__cleanup()


if __name__ == '__main__':
    unittest.main()
