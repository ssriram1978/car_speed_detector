import datetime;import os;from twilio.rest import Client
accountsid="INSERT_LIVE_ACCOUNT_SID_HERE"
accounttoken="INSERT_LIVE_ACCOUNT_TOKEN_HERE"
twilionumber="INSERT_YOUR_TWILIO_NUMBER_HERE"
#USE THIS LINK TO FIND YOUR TWILIO ACCOUNT SID, ACCOUNT TOKEN, & PHONE NUMBER -> (https://www.twilio.com/console)
mynumber="INSERT_YOUR_PHONE_NUMBER_HERE"
class ClassTextSend:
  def FuncTextSend(self):
    client = Client(accountsid,accounttoken)
    now = datetime.datetime.now()
    client.messages.create(from_=(twilionumber),
                                to=(mynumber),
                          body=("Somebody is speeding at {} on {}, {} {}, {} ".format(now.strftime("%X"),
                           now.strftime("%A"),now.strftime("%B"),now.strftime("%d"),now.strftime("%Y"))))
    print("Text message successfully sent")
TextSender=ClassTextSend()
TextSender.FuncTextSend()
