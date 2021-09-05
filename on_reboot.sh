#!/bin/bash
echo "source /usr/local/bin/virtualenvwrapper.sh" &> /home/pi/car_speed_detector.log
source /usr/local/bin/virtualenvwrapper.sh
echo "source /opt/intel/openvino/bin/setupvar.sh" &>> /home/pi/car_speed_detector.log
source /opt/intel/openvino/bin/setupvars.sh
echo "loading virtualenvwrapper.sh..." &>> /home/pi/car_speed_detector.log
source `which virtualenvwrapper.sh`
echo "accessing virtualenv py3cv4..." &>> /home/pi/car_speed_detector.log
workon py3cv4
cd /home/pi
echo "export PYTHONPATH=$PYTHONPATH:/home/pi/git/car_speed_detector"
export PYTHONPATH=$PYTHONPATH:/home/pi/git/car_speed_detector
echo "running Python script..." &>> /home/pi/car_speed_detector.log
python3 /home/pi/git/car_speed_detector/car_speed_detector/speed_detector.py &>> /home/pi/car_speed_detector.log
echo "script exiting..." &>> /home/pi/car_speed_detector.log
python3 /home/pi/git/car_speed_detector/email_crash_log.py
python3 /home/pi/git/car_speed_detector/car_speed_detector/email_sender.py
echo "rebooting..." &>> /home/pi/car_speed_detector.log
sudo reboot
