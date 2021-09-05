# Car Speed Detector
Car Speed Detector

This project is a community based project. 
It aims to do the following:
1. Demonstrate how to run an openly available image classification machine learning models on Intel® Movidius™ Neural Compute Stick.
2. Perform image classification and speed computation of a moving object (car).
3. Generate alarm (email) if the speed exceeds beyond the threshold limit.

How to install the correct Intel Openvino toolkit compatible with this application?
------------------------------
Just run this script provided in this git repository. 
```
/bin/bash /home/pi/git/car_speed_detector/install_openvino.sh
```

How to run this application automatically on rebooting raspberry Pi?
-----------------
Enable '''@/bin/bash /home/pi/git/car_speed_detector/on_reboot.sh''' in LXDE autostart script as shown below.
'''
cat /etc/xdg/lxsession/LXDE-pi/autostart
@lxpanel --profile LXDE-pi
@/bin/bash /home/pi/git/car_speed_detector/on_reboot.sh
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
'''
# Contributors:
  Abhisar Anand, Aditya Anand, Arjun Sikka, Srinivas Sriram, and Sriram Sridhar
