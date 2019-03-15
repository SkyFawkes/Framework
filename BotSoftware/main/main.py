# Import libraries
import asyncio
import threading
import time

# Include files
import realTimeProcessing
import captureVideo
import aServer
import MotorsP
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
        self.motors = MotorsP.Motors(MotorsEnabled)
        self.bt = Bluetooth.Bluetooth()

    async def runBot(self):

        # Start camera systems
        mCapture = captureVideo.capture()
        mServer = aServer.Server(info=self.info, lock=self.lock)
        mRealTime = realTimeProcessing.RealTimeProcessing(mCapture=mCapture, mServer=mServer,
                                                          info=self.info, lock=self.lock)
        starttime = time.time()
        CurrentTime = 0
        await self.motors.motorBeep()

        while True:
            # Wait for new frame data to arrive
            loop = asyncio.get_event_loop()
            await loop.create_task(self.awaitFrame())
            print(CurrentTime, self.CurrentFrame, self.FrameData)

            # Act on frame data
            x = (320 - self.FrameData) / 3.2
            self.motors.output(x, 0)

            CurrentTime = time.time() - starttime
            if CurrentTime > 60:
                break

        await self.closeBot()

    async def runBotRC(self):
        await self.bt.connect()
        await self.motors.motorBeep()

        while True:
            [x, y] = await self.bt.get()
            if x is None:
                break

            print(x, y)
            self.motors.output(x, y)

            await asyncio.sleep(0.01)

        await self.closeBot()

    async def closeBot(self):
        print('Close everything')
        loop = asyncio.get_event_loop()
        loop.stop()

    async def awaitFrame(self):
        # Loop continuously until frame number increases
        while True:
            with self.lock:
                if self.info.frame > self.CurrentFrame:
                    self.CurrentFrame = self.info.frame
                    self.FrameData = self.info.framedata
                    return
            await asyncio.sleep(0.002)

print('mmaaabbb')

#MotorsEnabled = True

loop = asyncio.get_event_loop()  # Get asyncio event loop
bot = MainFrame()
loop.create_task(bot.runBot())  # Autonomous
# loop.create_task(bot.runBotRC())  # Remote control

loop.run_forever()
loop.close()
