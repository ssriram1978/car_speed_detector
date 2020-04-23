from constants import SEND_EMAIL, MAX_THRESHOLD_SPEED, LOG_FILE_NAME
import cv2
import os
from threading import Thread
from pathlib import Path
from imutils.io import TempFile
from email_sender import EmailSender

class SpeedValidator:
    log_file = None
    
    @classmethod
    def close_log_file(cls):
        # check if the log file object exists, if it does, then close it
        if not cls.log_file:
            cls.logFile.close()

    @classmethod
    def initialize_log_file(cls):
        if not cls.log_file:
            cls.log_file = open(os.path.join(Path(__file__).parent, LOG_FILE_NAME),mode="a")
        # set the file pointer to end of the file
        if cls.log_file.seek(0, os.SEEK_END) == 0:
            cls.log_file.write("Year,Month,Day,Time (in MPH),Speed\n")

    @classmethod
    def validate_speed(cls, trackable_object, time_stamp, frame):
        # Initialize log file.
        if not cls.log_file:
            cls.initialize_log_file()
            
        # check if the object has not been logged
        if not trackable_object.logged:
            # check if the object's speed has been estimated and it
            # is higher than the speed limit
            if trackable_object.estimated and trackable_object.speedMPH > MAX_THRESHOLD_SPEED:
                # set the current year, month, day, and time
                year = time_stamp.strftime("%Y")
                month = time_stamp.strftime("%m")
                day = time_stamp.strftime("%d")
                time = time_stamp.strftime("%H:%M:%S")

                if SEND_EMAIL:
                    # initialize the image id, and the temporary file
                    imageID = time_stamp.strftime("%H%M%S%f")
                    tempFile = TempFile()
                    cv2.imwrite(tempFile.path, frame)

                    # create a thread to upload the file to dropbox
                    # and start it
                    t = Thread(target=EmailSender.send_email, args=(tempFile,imageID,))
                    t.start()

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
