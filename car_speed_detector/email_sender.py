# Import smtplib for the actual sending function
import email.mime.image
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
from car_speed_detector.car_speed_logging import logger

# And imghdr to find the types of our images
# Here are the email package modules we'll need

class EmailSender:
    # TODO make this as a CLI configurable param.
    username = 'speeddetector101@gmail.com'
    password = 'LearnIOT06!'
    rcptlist = ['srinivassriram06@gmail.com', 'arjunsikka05@gmail.com', 'kr.reddy.kaushik@gmail.com', 'adityaanand.muz@gmail.com', 'ssriram.78@gmail.com', 'abhisar.muz@gmail.com', 'raja.muz@gmail.com']
    host_name = socket.gethostname()

    @classmethod
    def send_email(cls, **kwargs):
        """

        """
        kwargs.get('temp_file', None)
        kwargs.get('image_name', None)
        kwargs.get('log_file', None)
        temp_file = kwargs['temp_file']
        image_name = kwargs['image_name']
        log_file = kwargs['log_file']
        logger().debug("Sending Email")
        receivers = ','.join(cls.rcptlist)

        msg = MIMEMultipart('mixed')
        msg['Subject'] = 'From GVW speed detector camera {} - Speeding car in GVW'.format(EmailSender.host_name)
        msg['From'] = cls.username
        msg['To'] = receivers

        if temp_file and image_name is not None:
            alternative = MIMEMultipart('alternative')
            textplain = MIMEText('Captured a picture of a speeding car.')
            alternative.attach(textplain)
            msg.attach(alternative)
            with open(temp_file.path, 'rb') as fp:
                #jpgpart = MIMEApplication(fp.read())
                jpgpart = email.mime.image.MIMEImage(fp.read())
                jpgpart.add_header('Content-Disposition', 'attachment', filename=image_name)
                msg.attach(jpgpart)


        if log_file is not None:
            msg.attach(MIMEText(log_file.read()))

        client = smtplib.SMTP('smtp.gmail.com', 587)
        client.starttls()
        #client = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        #client.ehlo()
        client.login(cls.username, cls.password)
        client.sendmail(cls.username, cls.rcptlist, msg.as_string())
        logger().debug("Email Sent")
        client.quit()
        os.remove(temp_file.path)
