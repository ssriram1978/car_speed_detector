#!/bin/bash
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/pi/test.log
source /usr/local/bin/virtualenvwrapper.sh
echo "source /opt/intel/openvino/bin/setupvar.sh" >> /home/pi/test.log
source /opt/intel/openvino/bin/setupvars.sh
echo "loading virtualenvwrapper.sh..." >> /home/pi/test.log
source `which virtualenvwrapper.sh`
echo "accessing virtualenv..." >> /home/pi/test.log
workon py3cv4
cd /home/pi
echo "running Python script..." >> /home/pi/test.log
python3 /home/pi/git/car_speed_detector/car_speed_detector/speed_detector.py 
echo "script exiting..." >> /home/pi/test.log
