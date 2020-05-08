import datetime; import os; from twilio.rest import Client
textinglist=["+1", "+1", ] #INSERT ANY PHONE NUMBERS HERE
def TextSender():
  for i in (testinglist):
    sid = os.environ.get('INSERT_TWILIO_ACCOUNT_SID_HERE')
    token = os.environ.get('INSERT_TWILIO_AUTHETIFICATION_TOKER_HERE')
    client = Client(sid,token)
    now = datetime.datetime.now()
    client.messages.create(from_=os.environ.get('INSERT_TWILIO_PHONE_NUMBER_HERE'),
                        to=os.environ.get(i),
                          body=("Somebody is speeding at {} on {}, {} {}, {} ".format(now.strftime("%X"),
                            now.strftime("%A"),now.strftime("%B"),now.strftime("%d"),now.strftime("%Y"))))
    print("Text message successfully sent")
 TextSender()
