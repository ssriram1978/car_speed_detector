import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import argparse


class CrashReport:
    """
        This class composes and sends an email when the car_speed_detector crashes.
    """

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-l", "--log_file", type=str,
                            help="Provide the log file to send via email", required=True)

    def perform_job(self):
        self.email_send()

    def email_send(self):
        """
        This method sends an email
        :return:
        """
        msg = MIMEMultipart()
        sender_email = "speeddetector101@gmail.com"
        receiver_email = "adityaanand.muz@gmail.com"
        password = "LearnIOT06!"
        msg['From'] = 'speeddetector101@gmail.com'
        msg['To'] = "adityaanand.muz@gmail.com"
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'The Car Speed Detector has crashed!'
        body = "The Car Speed Detector has crashed and the crash log is attached below"

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(self.args.log_file, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=self.args.log_file)
        msg.attach(part)

        msg.attach(MIMEText(body, "plain"))
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email.split(","), msg.as_string())
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))
        else:
            email_sent_status = True
        finally:
            return email_sent_status


if __name__ == '__main__':
    CrashReport().perform_job()