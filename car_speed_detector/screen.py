import os

#Finding Tempreture
find_temp = "/opt/vc/bin/vcgencmd measure_temp"
temperature = os.system(find_temp)

#Finding Speed
def get_speed()
    file = open("Speeds.csv", "r")
    lines = file.readlines()
    speed = lines[-1]
    file.close()
    return speed
