
"""
To set up a Bluetooth controller on a Raspberry Pi:

sudo apt-get update
sudo apt-get -y install python3-pip
sudo pip3 install evdev

sudo bluetoothctl
scan on
- turn controller on, set it to be discoverable
- Wait for controller to appear with its address
- for example E4:17:D8:CB:08:68 or 00:FF:01:00:1F:02

pair E4:17:D8:CB:08:68
connect E4:17:D8:CB:08:68
exit

"""

import asyncio
import os
import subprocess
from evdev import ecodes, list_devices, AbsInfo, InputDevice
import select
import sys

# Controller setup
Controller = '/dev/input/event0'
Gamepad = {0: 127, 1: 127, 2: 127, 5: 127, 314: 0, 315: 0}  # Initialise Gamepad dict

class Bluetooth():
    def __init__(self):
        self.fd = None  # Initialise device list

    async def connect(self):
        # Search for controller
        print('Search for controller')

        while not os.path.exists(Controller):
            # Call script to connect to bluetooth controller
            print('Controller not found, searching')
            rc = subprocess.Popen(['/bin/bash', sys.path[0] + "/btconnect.sh"])

            for a in range(0, 10):
                await asyncio.sleep(2)
                if os.path.exists(Controller):
                    break
                else:
                    print('Searching...')

        print('Found controller')
        devices = [InputDevice(Controller)]
        self.fd = {dev.fd: dev for dev in devices}

    async def get(self):

        # Get controller event:
        r, w, e = select.select(self.fd, [], [], 0)

        # Process all events in all controllers
        for fd in r:
            try:
                for event in self.fd[fd].read():
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

        # Quit if Start & Select pushed
        if (Select == 1) and (Start == 1):
            return [None, None]

        return [x,y]
