# encoding: utf-8

'''
Simple bluetooth controller interface
'''

import sys
import select
from evdev import ecodes, list_devices, AbsInfo, InputDevice
import subprocess
import time
import os.path

# Controller setup
Controller = '/dev/input/event0'
Gamepad = {0: 127, 1: 127, 2: 127, 5: 127, 314: 0, 315: 0}  # Initialise Gamepad dict

def main():

    # Search for controller
    while not os.path.exists(Controller):
        # Call script to connect to bluetooth controller
        print('Controller not found, searching')
        rc = subprocess.Popen(['/bin/bash', sys.path[0] + "/btconnect.sh"])

        for a in range(0, 10):
            time.sleep(1)
            if os.path.exists(Controller):
                break
            else:
                print('Searching...')

    print('Found controller')
    devices = [InputDevice(Controller)]

    print('Running (Crtl-C or Start+Select to exit)')
    fd_to_device = {dev.fd: dev for dev in devices}

    while True:

        # Wait for controller event:
        r, w, e = select.select(fd_to_device, [], [], 0.1)

        # Process all events in all controllers
        for fd in r:
            try:
                for event in fd_to_device[fd].read():
                    if event.type != ecodes.EV_SYN:
                        Gamepad[event.code] = event.value
                        # print(Gamepad)
            except:
                print('Lost connection to controller')
                return 0

        # Extract control info
        RX = int(((Gamepad[2] - 127) * 50) / 127)
        RY = int(((Gamepad[5] - 127) * -50) / 127)
        LX = int(((Gamepad[0] - 127) * 50) / 127)
        LY = int(((Gamepad[1] - 127) * -50) / 127)
        Select = Gamepad[314]
        Start = Gamepad[315]

        # Convert to control directions
        x = RX
        y = LY
        print(x, y)

        # Quit if Start & Select pushed
        if (Select == 1) and (Start == 1):
            return 0


if __name__ == '__main__':
    try:
        ret = main()
    except (KeyboardInterrupt, EOFError):
        ret = 0
    sys.exit(ret)
