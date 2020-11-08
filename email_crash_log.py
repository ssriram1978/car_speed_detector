from car_speed_detector.email_sender import EmailSender
print("sending log file")
email_sent_status = EmailSender().send_email(log_file='/home/pi/car_speed_detector.log')
print("log file sent to developers")

