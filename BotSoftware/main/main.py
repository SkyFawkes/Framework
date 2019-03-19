"""
Main program for Sky Fawkes PiWars robot

Asynchronous routines:
runBot (main loop)
awaitFrame - waits until new frame arrives from camera thread
"""

# Import libraries
import asyncio
import threading
import time
import os

print(os.uname()[1])

# Include files
import realTimeProcessing
import captureVideo
import aServer
import MotorsS as Motors
#import MotorsP as Motors
import Bluetooth

MotorsEnabled = False  # Disabled by default, override below

class SharedInfo:
    def __init__(self):
        # Set up info to be accessible from other classes
        self.image = None
        self.frame = 0
        self.framedata = 0


class MainFrame:
    def __init__(self):
        self.info = SharedInfo()
        self.lock = threading.Lock()
        self.CurrentFrame = 0
        self.FrameData = 0

        # Initialise motors & controller
        self.motors = Motors.Motors(MotorsEnabled)
        self.bt = Bluetooth.Bluetooth()

    async def run(self):

        # Connect to bluetooth controller
        await self.bt.connect()

        # Start camera systems
        mCapture = captureVideo.capture()
        mServer = aServer.Server(info=self.info, lock=self.lock)
        mRealTime = realTimeProcessing.RealTimeProcessing(mCapture=mCapture, mServer=mServer,
                                                          info=self.info, lock=self.lock)
        await self.motors.beepOk()

        starttime = time.time()
        CurrentTime = 0

        while True:
            # Wait for new frame data to arrive
            loop = asyncio.get_event_loop()
            await self.awaitFrame()
            print(CurrentTime, self.CurrentFrame, self.FrameData, threading.active_count())

            # Act on frame data
            x = (320 - self.FrameData) / 6.4  # Convert FrameData to +/-50
            self.motors.output(x, 0)

            CurrentTime = time.time() - starttime
            if CurrentTime > 60:
                break

        await self.close()

    async def runRC(self):

        # Connect to bluetooth controller
        await self.bt.connect()
        await self.motors.beepOk()

        while True:
            [x, y] = await self.bt.get()
            if x is None:
                break

            print(x, y)
            self.motors.output(x, y)

            await asyncio.sleep(0.01)

        await self.close()

    async def runAuto(self):
        await self.motors.beepOk()

        # Forward
        print('Forward')
        self.motors.output(0, 80)
        await asyncio.sleep(1)
        #print('Reverse')
        #self.motors.output(0, -25)
        #await asyncio.sleep(1)
        #print('Right')
        #self.motors.output(25, 0)
        #await asyncio.sleep(1)
        #print('Left')
        #self.motors.output(-25, 0)
        #print('Stop')
        await asyncio.sleep(1)
        self.motors.output(0, 0)

        await self.close()

    async def close(self):
        print('Close everything')
        loop = asyncio.get_event_loop()
        loop.stop()

    async def awaitFrame(self):
        # Loop continuously until frame number increases
        n = 0
        while True:
            n += 1
            with self.lock:
                if self.info.frame > self.CurrentFrame:
                    self.CurrentFrame = self.info.frame
                    self.FrameData = self.info.framedata
                    #print(n)
                    return
            await asyncio.sleep(0.002)

print('Starting everything up.....')

MotorsEnabled = True  # Uncomment to enable motors

loop = asyncio.get_event_loop()  # Get asyncio event loop
bot = MainFrame()
#loop.create_task(bot.run())  # Autonomous
#loop.create_task(bot.runRC())  # Remote control
loop.create_task(bot.runAuto())  # Automatic motor test

loop.run_forever()
loop.close()
