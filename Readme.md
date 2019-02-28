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
