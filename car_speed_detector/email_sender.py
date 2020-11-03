# Import smtplib for the actual sending function
import email.mime.image
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import socket
from car_speed_detector.car_speed_logging import logger
from email import encoders
from car_speed_detector.constants import TEMP_FILE, IMAGE_NAME, LOG_FILE

# And imghdr to find the types of our images
# Here are the email package modules we'll need

class EmailSender:
    # TODO make this as a CLI configurable param.
    username = 'speeddetector101@gmail.com'
    password = 'LearnIOT06!'
    recipient_list = ['srinivassriram06@gmail.com', 'arjunsikka05@gmail.com', 'kr.reddy.kaushik@gmail.com', 'adityaanand.muz@gmail.com', 'ssriram.78@gmail.com', 'abhisar.muz@gmail.com', 'raja.muz@gmail.com']
    host_name = socket.gethostname()

    @classmethod
    def send_email(cls, **kwargs):
        """

        """
        status = True
        try:
            logger().debug("Sending Email")
            receivers = ','.join(cls.rcptlist)

            msg = MIMEMultipart('mixed')
            msg['Subject'] = 'From GVW speed detector camera {} - Speeding car in GVW'.format(EmailSender.host_name)
            msg['From'] = cls.username
            msg['To'] = receivers

            if TEMP_FILE in kwargs and IMAGE_NAME in kwargs:
                alternative = MIMEMultipart('alternative')
                textplain = MIMEText('Captured a picture of a speeding car.')
                alternative.attach(textplain)
                msg.attach(alternative)
                with open(TEMP_FILE.path, 'rb') as fp:
                    #jpgpart = MIMEApplication(fp.read())
                    jpgpart = email.mime.image.MIMEImage(fp.read())
                    jpgpart.add_header('Content-Disposition', 'attachment', filename=IMAGE_NAME)
                    msg.attach(jpgpart)


            if LOG_FILE in kwargs:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(LOG_FILE, "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=LOG_FILE)
                msg.attach(part)

            client = smtplib.SMTP('smtp.gmail.com', 587)
            client.starttls()
            #client = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            #client.ehlo()
            client.login(cls.username, cls.password)
            client.sendmail(cls.username, cls.rcptlist, msg.as_string())
            logger().debug("Email Sent")
            client.quit()
            os.remove(TEMP_FILE.path)
        except:
            status = False
        return status
