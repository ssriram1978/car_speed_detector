# This file is used to test the car speed whatsapp message sender functionality.
import os
import unittest
from car_speed_detector.whats_app_message_sender import WhatsAppMessageSender


class TestWhatsappMessageSender(unittest.TestCase):
    """
    This class unit tests WhatsAppMessageSender class.
    """

    def test_whatsapp_message_sender(self):
        WhatsAppMessageSender().send_whatsapp_message(speed=10,
                                                      image_path=os.path.join(os.path.dirname(__file__),
                                                                              '../sample_data/speeding_car.jpg'))

