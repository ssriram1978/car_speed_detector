import datetime;import os;from twilio.rest import Client
accountsid="INSERT_ACCOUNT_SID_HERE"
accounttoken="INSERT_ACCOUNT_TOKEN_HERE"
twilionumber="INSERT_TWILIO_PHONE_NUMBERS_HERE"
#USE THIS LINK TO FIND YOUR TWILIO ACCOUNT SID, ACCOUNT TOKEN, & PHONE NUMBER -> https://www.twilio.com/console
mynumbers= ["INSERT_ANY_PHONE_NUMBERS_HERE]
class ClassTextSend:
  def FuncTextSend(self):
      for i in range(len(mynumbers)):
            client = Client(accountsid,accounttoken)
            now = datetime.datetime.now()
            client.messages.create(from_=(twilionumber),
                                     to=(mynumbers[i]),
                                 body=("Somebody is speeding at {} on {}, {} {}, {} ".format(now.strftime("%X"),
                                 now.strftime("%A"),now.strftime("%B"),now.strftime("%d"),now.strftime("%Y"))))
            print("Text message successfully sent")
TextSender=ClassTextSend()
TextSender.FuncTextSend()
