# Import smtplib for the actual sending function
import smtplib

# And imghdr to find the types of our images
import imghdr

# Here are the email package modules we'll need
from email.message import EmailMessage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from car_speed_logging import logger

class EmailSender:
    # TODO make this as a CLI configurable param. 
    username = 'xyz@todo'
    password = 'password'
    rcptlist = ['srinivassriram06@gmail.com', 'arjunsikka05@gmail.com', 'kr.reddy.kaushik@gmail.com', 'adityaanand.muz@gmail.com', 'ssriram.78@gmail.com', 'abhisar.muz@gmail.com', 'raja.muz@gmail.com']
    
    @classmethod
    def send_email(cls, image, image_name):
        """
        
        """
        logger().debug("Sending Email")
        receivers = ','.join(rcptlist)

        msg = MIMEMultipart('mixed')
        msg['Subject'] = 'From GVW speed detector camera - Speeding car in GVW'
        msg['From'] = cls.username
        msg['To'] = cls.receivers

        alternative = MIMEMultipart('alternative')
        textplain = MIMEText('Captured a picture of a speeding car.')
        alternative.attach(textplain)
        msg.attach(alternative)
        jpgpart = MIMEApplication(image)
        jpgpart.add_header('Content-Disposition', 'attachment', filename=image_name)
        msg.attach(jpgpart)

        client = smtplib.SMTP('smtp.gmail.com', 587)
        client.starttls()
        client.login(cls.username, password)
        client.sendmail(cls.username, rcptlist, msg.as_string())
        logger().debug("Email Sent")
        client.quit()
