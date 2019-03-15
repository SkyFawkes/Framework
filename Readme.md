# Framework
This repository contains the code that ties together the separate elements of our robot, and instructions on how to set up the Pi from scratch.

## Setup
The following instructions assume the Pi is running headless (without a keyboard or monitor).
### Install Raspbian
Install  [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/). [Etcher](https://www.balena.io/etcher/) is a convenient tool for doing this.

Before moving the card to the Pi, copy files 'ssh' and 'wpa_supplicant.conf' from the 'Setup' folder of this repository into the boot partition of the newly copied SD card. Then open 'wpa_supplicant.conf' and enter the right wifi credentials.

Move the card over to the Pi and switch it on.

### Set up Raspbian

Use an SSH client like Putty or MobaXterm to connect to the Pi. You may be able to do this with its hostname ('raspbian') or by finding its IP with [Advanced IP Scanner](https://www.advanced-ip-scanner.com/) or your router's interface. The default username is 'pi' and password is 'raspberry'.

Next, make sure the software is up to date:
```
sudo apt-get update && sudo apt-get -y upgrade
```
and install some basics:
```
sudo apt-get -y install python3-dev python3-pip python3-rpi.gpio
```
### Setting up bluetooth control
```
sudo pip3 install evdev
sudo bluetoothctl
scan on
```
Turn on the controller and set it to discoverable mode.
Its name and MAC address should appear on the screen. Pair it using its MAC address, for example:
```
pair E4:17:D8:CB:08:68
connect E4:17:D8:CB:08:68
exit
```
Try to access it:
```
ls /dev/input
cat /dev/input/event0
```
You should see random characters on the screen. Exit with clrt-C and try:
```
python3 /usr/local/lib/python3.5/dist-packages/evdev/evtest.py
```
### Setting up PiCam and OpenCV
Connect the camera module to the Pi using the connector by the HDMI port, with the contacts facing the HDMI port. The power up the Pi.
```
sudo raspi-config
```
Enable the camera in the settings.
Then install the following:
```
sudo apt-get install libhdf5-serial-dev libharfbuzz0b libatlas3-base libwebp6 libtiff5 libjasper1 libilmbase12 libopenexr22 libgstreamer1.0-0 libavcodec57 libavformat57 libswscale4 libgtk-3-0
sudo pip3 install opencv-contrib-python-headless
sudo pip3 install picamera
```
