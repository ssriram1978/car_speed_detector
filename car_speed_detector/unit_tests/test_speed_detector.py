# This file is used to test the car speed detector functionality.

import unittest

from car_speed_detector.speed_detector import SpeedDetector


class TestSpeedDetector(unittest.TestCase):
    """
    This class unit tests SpeedDetector class.
    """
    def test_speed_detector(self):
        speed_detector_inst = SpeedDetector(estimate_speed_from_video_file_name='sample_data/cars.mp4')
        self.assertEqual(speed_detector_inst.perform_speed_detection(), True)


if __name__ == '__main__':
    unittest.main()
