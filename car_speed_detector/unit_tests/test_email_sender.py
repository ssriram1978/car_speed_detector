# This file is used to test the car speed detector email sender functionality.

import unittest
import os
from car_speed_detector.email_sender import EmailSender


# TODO Arjun, Adi

class TestEmailSender(unittest.TestCase):
    """
    This class unit tests Email Sender class.
    """

    def test_email_sender(self):
        email_sent_status = EmailSender().send_email(temp_file='sample_data/car.jpg',
                                                     image_name='car.jpg',
                                                     log_file='sample_data/car_logging.log')
        self.assertEqual(email_sent_status, True)


if __name__ == '__main__':
    unittest.main()
