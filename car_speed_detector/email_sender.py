# Import smtplib for the actual sending function
import email.mime.image
import sys, traceback
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import socket
from car_speed_detector.car_speed_logging import logger
from email import encoders
from car_speed_detector.constants import USERNAME, PASSWORD, TEMP_FILE, IMAGE_NAME, LOG_FILE
from dotenv import load_dotenv
load_dotenv(verbose=True)
# And imghdr to find the types of our images
# Here are the email package modules we'll need

class EmailSender:
    main_recipient_list = os.getenv('RECIPIENTS_LIST').split(',')
    developer_recipient_list = os.getenv('DEVELOPERS_LIST').split(',')
    host_name = socket.gethostname()

    @classmethod
    def send_email(cls, **kwargs):
        """

        """
        status = True
        try:
            logger().info("Sending Email kwargs={}.".format(kwargs))

            msg = MIMEMultipart('mixed')
            msg['From'] = os.getenv(USERNAME)
            alternative = MIMEMultipart('alternative')
                
            if IMAGE_NAME in kwargs:
                textplain = MIMEText('Captured a picture of a speeding car.')
                alternative.attach(textplain)
                msg.attach(alternative)
                image_name=kwargs[IMAGE_NAME].split('/')[-1]
                with open(kwargs[IMAGE_NAME], 'rb') as fp:
                    jpgpart = email.mime.image.MIMEImage(fp.read())
                    jpgpart.add_header('Content-Disposition', 'attachment', filename=image_name)
                    msg.attach(jpgpart)
                    logger().info("successfully attached jpeg {} in Email".format(image_name))


            if LOG_FILE in kwargs:
                textplain = MIMEText('Sending crash dump..')
                alternative.attach(textplain)
                msg.attach(alternative)
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(kwargs[LOG_FILE], "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=kwargs[LOG_FILE])
                msg.attach(part)
                logger().info("Successfully attached log file. {}".format(kwargs[LOG_FILE]))

            client = smtplib.SMTP('smtp.gmail.com', 587)
            client.starttls()
            #client = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            client.login(os.getenv(USERNAME), os.getenv(PASSWORD))
            if LOG_FILE in kwargs:
                msg['Subject'] = 'The Car Speed Detector has broke on {}'.format(EmailSender.host_name)
                client.sendmail(os.getenv(USERNAME), cls.developer_recipient_list, msg.as_string())
            if LOG_FILE not in kwargs:
                msg['Subject'] = 'From GVW speed detector camera {} - Speeding car in GVW'.format(EmailSender.host_name)
                client.sendmail(os.getenv(USERNAME), cls.main_recipient_list, msg.as_string())
            logger().info("Email Sent")
            client.quit()
        except Exception as e:
                logger().error("Caught an exception while sending an email {}....".format(
                    type(e).__name__ + ': ' + str(e)))
                print("Exception in user code:")
                print("-" * 60)
                traceback.print_exc(file=sys.stdout)
                print("-" * 60)
                status = False
        #finally:
            #if TEMP_FILE in kwargs:
            #    logger().info("Removing temp file name={}.".format(kwargs[TEMP_FILE].path))
            #    os.system("rm -rf {}".format(kwargs[TEMP_FILE].path))
        return status
