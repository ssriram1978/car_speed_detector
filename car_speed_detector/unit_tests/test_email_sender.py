# This file is used to test the car speed detector email sender functionality.

import unittest
import os
import os.path
from car_speed_detector.email_sender import EmailSender
from imutils.io import TempFile


class TestEmailSender(unittest.TestCase):
    """
    This class unit tests Email Sender class.
    """

    def test_email_sender_with_speeding_car(self):
        print("testing email sender...")
        email_sent_status = EmailSender().send_email(image_name=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                              '../sample_data/car.jpg'))
        self.assertEqual(email_sent_status, True)
        print("Email sent unit test passed")
        
        
    def test_email_sender_with_debug_log(self):
        print("testing email sender...")
        os.system("touch car_logging.log")
        os.system("Email Sent >> car_logging.log")
        email_sent_status = EmailSender().send_email(log_file='car_logging.log')
        self.assertEqual(email_sent_status, True)
        
    


if __name__ == '__main__':
    unittest.main()
