# This file is used to test the car speed whatsapp message sender functionality.
import os
import unittest
from car_speed_detector.whats_app_message_sender import WhatsAppMessageSender


class TestWhatsappMessageSender(unittest.TestCase):
    """
    This class unit tests WhatsAppMessageSender class.
    """

    def test_speed_detector(self):
        whatsapp_message_sender_inst = WhatsAppMessageSender(
            browser_location='/usr/bin/google-chrome',
            browser_executable_path='/home/sriramsridhar/Downloads/chromedriver')
        image_path = os.path.join(os.getcwd(), 'car_test.jpg')
        self.assertEqual(whatsapp_message_sender_inst.send_message(20, image_path=image_path), None)
