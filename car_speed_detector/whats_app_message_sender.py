from twilio.rest import Client
import socket
from car_speed_detector.constants import CAR_SPEED, SPEEDING_CAR_IMAGE
import os
import boto3
import time
import sys, traceback
from dotenv import load_dotenv
from car_speed_detector.car_speed_logging import logger

load_dotenv(verbose=True)


class WhatsAppMessageSender(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WhatsAppMessageSender, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.__s3_bucket = None
        self.__host_name = None
        self._instance = None
        self.__client = None
        self.__from_whatsapp_number = None
        self.__to_whatsapp_number = None
        # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
        self.__client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
        self.__host_name = socket.gethostname().lower()

        # this is the Twilio sandbox testing number
        self.__from_whatsapp_number = os.environ['WHATSAPP_FROM_NUMBER']
        # replace this number with your own WhatsApp Messaging number
        self.__to_whatsapp_number = os.environ['WHATSAPP_TO_NUMBER']

        try:
            logger().info("Trying to create bucket {}.".format(self.__host_name))
            self.__s3_bucket = self.__make_bucket(self.__host_name, 'public-read')
        except Exception:
            logger().error("Exception in user code:")
            logger().error("-" * 60)
            traceback.print_exc(file=sys.stdout)
            logger().error("-" * 60)

    def __make_bucket(self, name, acl):
        session = self.__aws_session()
        s3_resource = session.resource('s3')
        return s3_resource.create_bucket(Bucket=name, ACL=acl)

    def __aws_session(self, region_name='us-east-1'):
        return boto3.session.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=os.getenv('AWS_ACCESS_KEY_SECRET'),
                                     region_name=region_name)

    def send_whatsapp_message(self, **kwargs):
        # client.messages.create(body='From GVW Car speed detector camera {}, speeding car in GVW - {} mph.'.format(cls.__host_name, kwargs[CAR_SPEED]),
        #                   from_=from_whatsapp_number,
        #                   to=to_whatsapp_number)
        logger().info("kwargs = {}".format(kwargs))
        if SPEEDING_CAR_IMAGE not in kwargs or CAR_SPEED not in kwargs:
            return
        logger().info(
            f"Uploading the speeding car image url {kwargs[SPEEDING_CAR_IMAGE]} to {self.__host_name} s3 location.")
        s3_url = self.__upload_file_to_bucket(kwargs[SPEEDING_CAR_IMAGE])
        logger().info("sending a whatsapp message to {}".format(s3_url))
        message = self.__client.messages.create(
            body='From GVW Car speed detector camera {}, speeding car in GVW - {} mph.'.format(self.__host_name,
                                                                                               kwargs[CAR_SPEED]),
            media_url=[s3_url],
            #media_url=['https://s3.amazonaws.com/srirams-macbook-pro.local/owl.png'],
            from_=self.__from_whatsapp_number,
            to=self.__to_whatsapp_number
        )
        logger().info("whatsapp message sent status = {}".format(message))

    def __upload_file_to_bucket(self, file_path):
        if not os.path.exists(file_path):
            return ""
        file_dir, file_name = os.path.split(file_path)
        if not self.__s3_bucket:
            return
        self.__s3_bucket.upload_file(
            Filename=file_path,
            Key=file_name,
            ExtraArgs={'ACL': 'public-read'}
        )
        s3_url = f"https://{self.__host_name}.s3.amazonaws.com/{file_name}"
        time.sleep(2)
        return s3_url
