import os
from datetime import datetime
from pathlib import Path
from threading import Thread

import cv2
from car_speed_detector.constants import SEND_EMAIL, MAX_THRESHOLD_SPEED, LOG_FILE_NAME, TEMP_FILE, IMAGE_NAME, LOG_FILE
from car_speed_detector.email_sender import EmailSender
from imutils.io import TempFile
from car_speed_detector.whats_app_message_sender import WhatsAppMessageSender
from car_speed_detector.car_speed_logging import logger
from car_speed_detector.email_sender import EmailSender


class SpeedValidator:
    log_file = None

    @classmethod
    def close_log_file(cls):
        # check if the log file object exists, if it does, then close it
        if cls.log_file:
            cls.log_file.close()

    @classmethod
    def initialize_log_file(cls):
        if not cls.log_file:
            cls.log_file = open(os.path.join(Path(__file__).parent, LOG_FILE_NAME), mode="a")
        # set the file pointer to end of the file
        if cls.log_file.seek(0, os.SEEK_END) == 0:
            cls.log_file.write("Year,Month,Day,Time (in MPH),Speed\n")

    @classmethod
    def validate_speed(cls, trackable_object):
        # Initialize log file.
        if not cls.log_file:
            cls.initialize_log_file()
        if not trackable_object:
            return
        # check if the object has not been logged
        if not trackable_object.logged:
            # check if the object's speed has been estimated and it
            # is higher than the speed limit
            if trackable_object.estimated and trackable_object.speedMPH > MAX_THRESHOLD_SPEED:
                mid_point = len(trackable_object.tracked_object_frame_list) // 2
                time_stamp = trackable_object.timestamp_list[mid_point]
                frame = trackable_object.tracked_object_frame_list[mid_point]

                # set the current year, month, day, and time
                year = time_stamp.strftime("%Y")
                month = time_stamp.strftime("%m")
                day = time_stamp.strftime("%d")
                time = time_stamp.strftime("%H:%M:%S")

                if SEND_EMAIL:
                    # initialize the image id, and the temporary file
                    imageID = time_stamp.strftime("%H%M%S%f")
                    tempFile = TempFile()

                    # write the date and speed on the image.
                    cv2.putText(frame, datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
                    # write the speed: first get the size of the text
                    size, base = cv2.getTextSize("%.0f mph" % trackable_object.speedMPH, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)
                    # then center it horizontally on the image
                    cntr_x = int((frame.shape[1] - size[0]) / 2)
                    cv2.putText(frame, "%.0f mph" % trackable_object.speedMPH,
                                (cntr_x, int(frame.shape[0] * 0.2)), cv2.FONT_HERSHEY_SIMPLEX, 2.00, (0, 255, 0), 3)
                    cv2.imwrite(tempFile.path, frame)

                    # create a thread to send the image via email.
                    # and start it
                    # TODO Aditya - Fix this error.
                    t = Thread(target=EmailSender.send_email, kwargs=dict(temp_file='tempfile.jpg',image_names='car.jpg2', ))
                    t.start()
                    image_path = os.path.join(os.getcwd(), "{}.jpg".format(imageID))
                    logger().info("Writing car image {} to hard drive.".format(image_path))
                    cv2.imwrite(image_path, frame)
                    #t2 = Thread(target=WhatsAppMessageSender().send_message(speed=trackable_object.speedMPH,
                     #                                                       image_path=image_path))
                    #t2.start()
                    # log the event in the log file
                    info = "{},{},{},{},{},{}\n".format(year, month,
                                                        day, time, trackable_object.speedMPH, imageID)
                else:
                    # log the event in the log file
                    info = "{},{},{},{},{}\n".format(year, month,
                                                     day, time, trackable_object.speedMPH)
                cls.log_file.write(info)

                # set the object has logged
                trackable_object.logged = True
