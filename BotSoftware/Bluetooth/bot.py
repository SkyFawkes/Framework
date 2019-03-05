# encoding: utf-8

'''
Simple robot control program
'''

import sys
import select
import RPi.GPIO as GPIO
from evdev import ecodes, list_devices, AbsInfo, InputDevice
import subprocess
import time
import os.path

# Controller setup
Controller = '/dev/input/event0'
Gamepad = {0:127,1:127,2:127,5:127,314:0,315:0} # Initialise Gamepad dict
LFPin   = 12
LRPin   = 16
RFPin   = 24
RRPin   = 25
PWMFreq = 200

def main():

    # Set up GPIOs
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([LFPin, LRPin, RFPin, RRPin], GPIO.OUT)
    LF = GPIO.PWM(LFPin, PWMFreq)
    LR = GPIO.PWM(LRPin, PWMFreq)
    RF = GPIO.PWM(RFPin, PWMFreq)
    RR = GPIO.PWM(RRPin, PWMFreq)
    LF.start(100)
    LR.start(100)
    RF.start(100)
    RR.start(100)

    # Search for controller
    while not os.path.exists(Controller):
        # Call script to connect to bluetooth controller
        print('Controller not found, searching')
        rc = subprocess.Popen(['/bin/bash', sys.path[0] + "/btconnect.sh"])
        
        for a in range(0,10):
            time.sleep(1)
            if os.path.exists(Controller):
                break
            else:
                print('Searching...')

    print('Found controller')
    devices = [InputDevice(Controller)]

    LF.ChangeFrequency(3520)
    LF.ChangeDutyCycle(80)
    time.sleep(0.025)
    LF.ChangeDutyCycle(100)
    time.sleep(0.1)
    LF.ChangeFrequency(5280)
    LF.ChangeDutyCycle(80)
    time.sleep(0.025)
    LF.ChangeDutyCycle(100)
    LF.ChangeFrequency(PWMFreq)

    print('Running (Crtl-C or Start+Select to exit)')
    fd_to_device = {dev.fd: dev for dev in devices}
    
    while True:

        # Wait for controller event:
        r, w, e = select.select(fd_to_device, [], [])

        # Process all events in all controllers
        for fd in r:
            try:
                for event in fd_to_device[fd].read():
                    if event.type != ecodes.EV_SYN:
                        Gamepad[event.code] = event.value
                        #print(Gamepad)
            except:
                print('Lost connection to controller')
                return 0

        # Extract control info
        RX = int(((Gamepad[2] - 127) * 50) / 127)
        RY = int(((Gamepad[5] - 127) * -50) / 127)
        LX = int(((Gamepad[0] - 127) * 50) / 127)
        LY = int(((Gamepad[1] - 127) * -50) / 127)
        Select = Gamepad[314]
        Start  = Gamepad[315]

        # Convert to control directions
        x = RX
        y = LY
        #print(x,y)
        
        # Calculate wheel speeds
        LW = y + x
        RW = y - x

        # Calculate PWM outputs
        if LW > 0:
            LF.ChangeDutyCycle(100 - LW)
            LR.ChangeDutyCycle(100)
        elif LW < 0:
            LF.ChangeDutyCycle(100)
            LR.ChangeDutyCycle(100 + LW)
        else:
            LF.ChangeDutyCycle(100)
            LR.ChangeDutyCycle(100)

        if RW > 0:
            RF.ChangeDutyCycle(100 - RW)
            RR.ChangeDutyCycle(100)
        elif RW < 0:
            RF.ChangeDutyCycle(100)
            RR.ChangeDutyCycle(100 + RW)
        else:
            RF.ChangeDutyCycle(100)
            RR.ChangeDutyCycle(100)

        # Quit if Start & Select pushed
        if (Select == 1) and (Start == 1):
            return 0

if __name__ == '__main__':
    try:
        ret = main()
    except (KeyboardInterrupt, EOFError):
        ret = 0
    GPIO.cleanup()
    sys.exit(ret)
