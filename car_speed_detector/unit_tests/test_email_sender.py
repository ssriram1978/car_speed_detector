# This file is used to test the car speed detector email sender functionality.

import unittest
import os
import os.path
from car_speed_detector.email_sender import EmailSender
from imutils.io import TempFile

# TODO Arjun, Adi

class TestEmailSender(unittest.TestCase):
    """
    This class unit tests Email Sender class.
    """

    def test_email_sender_with_speeding_car(self):
        print("testing email sender...")
        os.system("cp /home/pi/git/car_speed_detector/car_speed_detector/sample_data/car.jpeg2 /home/pi/git/car_speed_detector/car_speed_detector/sample_data/car.jpeg")
        temp_file = TempFile()
        temp_file.path = '/home/pi/git/car_speed_detector/car_speed_detector/sample_data/car.jpeg'
        temp_file1 = TempFile()
        temp_file1.path = '/home/pi/git/car_speed_detector/car_speed_detector/sample_data/car.jpeg2'
        email_sent_status = EmailSender().send_email(temp_file=temp_file,
                                                     image_name='car.jpeg')
        self.assertEqual(email_sent_status, True)
        print("Email sent unit test passed")
        
        # TODO Arjun : Check if car.jpeg is actually deleted.
        self.assertEqual(os.path.exists(temp_file.path), False)
        print("file delete test passed")
        
    def test_email_sender_with_debug_log(self):
        print("testing email sender...")
        os.system("cp /home/pi/git/car_speed_detector/car_speed_detector/sample_data/car.jpeg2 /home/pi/git/car_speed_detector/car_speed_detector/sample_data/car.jpeg")
        os.system("touch car_logging.log")
        os.system("Email Sent >> car_logging.log")
        email_sent_status = EmailSender().send_email(log_file='car_logging.log')
        self.assertEqual(email_sent_status, True)
        
    


if __name__ == '__main__':
    unittest.main()
