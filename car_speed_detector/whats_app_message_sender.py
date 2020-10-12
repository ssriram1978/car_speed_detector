# This file defines the logic to send an alert with the speeding car image in whatsapp.

#from selenium import webdriver
from datetime import datetime
from car_speed_detector.constants import WHATSAPP_CHAT_GROUP_NAME, BROWSER_LOCATION, BROWSER_EXECUTABLE_PATH
from car_speed_detector.car_speed_logging import logger
from car_speed_detector.singleton_template import Singleton
import time


class WhatsAppMessageSender(metaclass=Singleton):
    """
    This class implements the logic to send Whatsapp message to the specified group with the information about the
    speeding car.
    """

    def __init__(self, browser_location=BROWSER_LOCATION, browser_executable_path=BROWSER_EXECUTABLE_PATH):
        pass
        speeding_car_opts = webdriver.ChromeOptions()
        speeding_car_opts.binary_location = browser_location
        self.driver = webdriver.Chrome(executable_path=browser_executable_path, options=speeding_car_opts)
        self.driver.get('https://web.whatsapp.com')
        time.sleep(10)

    def send_message(self, speed, temp_file, image_name):
        """
        This method is used by the caller to trigger an alert via whatsapp with the
        speeding car image and a text alert.
        :param temp_file: an instance of type TempFile.
        :param image_name: Name of the image.
        :return:
        """
        pass
        to = (WHATSAPP_CHAT_GROUP_NAME)
        now = datetime.now()
        message = (
            "From GVW, there is a speeding car of speed = {}, at time = {} on date = {} - day = {}, month = {} , "
            "year = {}.".format(speed, now.strftime("%X"), now.strftime("%d"), now.strftime("%A"), now.strftime("%B"),
                                now.strftime("%Y")))
        logger().info(message)

        # finds the name of the group chat
        user = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(to))
        # clicks on the name of the group chat
        user.click()
        # finds the message box
        messagebox = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        # pastes the message into the message box
        messagebox.send_keys(message)
        # finds the button to send the message
        button = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]')
        # clicks the button to send the message
        button.click()
        #TODO Send the image in whatsapp.
        # with open(temp_file.path, 'rb') as fp:
        # jpgpart = email.mime.image.MIMEImage(fp.read())
        #             jpgpart.add_header('Content-Disposition', 'attachment', filename=image_name)
        # attach jpgpart into messagebox = driver.find_element_by_xpath
        # finds the button to send the message

