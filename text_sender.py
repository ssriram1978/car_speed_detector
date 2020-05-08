import datetime; from twilio.rest import Client
textnumbers = [""]  # INSERT ANY PHONE NUMBERS HERE
sid = "" # INSERT ACCOUNT SID HERE
token = "" # INSERT AUTH TOKEN HERE
twilionumber = "" # INSERT THE TWILIO NUMBER HERE
client = Client(sid, token)
def textsend():
    try:
        for i in range(len(textnumbers)):
            now = datetime.datetime.now()
            client.messages.create(from_=(twilionumber),
                                    to=(textnumbers[i]),
                                    body=("Somebody is speeding at {} on {}, {} {}, {} ".format(now.strftime("%X"),
                                        now.strftime("%A"),now.strftime("%B"), now.strftime("%d"),now.strftime("%Y"))))
        print(len(textnumbers), "text messages succesfully sent!")
    except:
        print("There was an error, and {} messages could not be successfully sent.".format(len(textnumbers)))
textsend()
