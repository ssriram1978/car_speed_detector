#!/bin/bash
cd /home/pi
echo "export PYTHONPATH=$PYTHONPATH:/home/pi/git/car_speed_detector"
export PYTHONPATH=$PYTHONPATH:/home/pi/git/car_speed_detector
echo "running log sender script..."
python3 /home/pi/git/car_speed_detector/car_speed_detector/email_sender.py /home/pi/car_speed_detector.log
