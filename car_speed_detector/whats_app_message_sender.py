from twilio.rest import Client
import socket
from car_speed_detector.constants import CAR_SPEED, SPEEDING_CAR_IMAGE
import os
import boto3
import time
from dotenv import load_dotenv

load_dotenv(verbose=True)

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
host_name = socket.gethostname()

# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:+19788097936'

def aws_session(region_name='us-east-1'):
    return boto3.session.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_ACCESS_KEY_SECRET'),
                                region_name=region_name)
session = aws_session()
s3_resource = session.resource('s3')

def make_bucket(name, acl):
    session = aws_session()
    s3_resource = session.resource('s3')
    return s3_resource.create_bucket(Bucket=name, ACL=acl)

s3_bucket = make_bucket(host_name, 'public-read')

def upload_file_to_bucket(bucket_name, file_path):
    session = aws_session()
    s3_resource = session.resource('s3')
    file_dir, file_name = os.path.split(file_path)

    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_file(
      Filename=file_path,
      Key=file_name,
      ExtraArgs={'ACL': 'public-read'}
    )

    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    time.sleep(2)
    return s3_url


def send_whatsapp_message(**kwargs):
    #client.messages.create(body='From GVW Car speed detector camera {}, speeding car in GVW - {} mph.'.format(host_name, kwargs[CAR_SPEED]),
    #                   from_=from_whatsapp_number,
    #                   to=to_whatsapp_number)
    s3_url = upload_file_to_bucket(host_name, kwargs[SPEEDING_CAR_IMAGE])
    print("sending a whatsapp message to {}".format(s3_url))
    message = client.messages.create(body='From GVW Car speed detector camera {}, speeding car in GVW - {} mph.'.format(host_name, kwargs[CAR_SPEED]),
             #media_url=[s3_url],
             media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
            from_=from_whatsapp_number,
            to=to_whatsapp_number
        )  

    print("whatsapp message sent status = {}".format(message))

if __name__ == '__main__':
    send_whatsapp_message(speed=10,image_path='/home/pi/speeding_car_images/145234833414.jpg')
