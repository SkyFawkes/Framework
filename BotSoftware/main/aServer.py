
# https://docs.python.org/3.7/library/asyncio-stream.html
# Runs on Pi, sets up sever to send images to PC

import asyncio
import json
import cv2


class Server:
    def __init__(self, info, lock):
        loop = asyncio.get_event_loop()
        loop.create_task(self.startServer())

        self.imSize = None
        self.info = info  # Shared info
        self.lock = lock  # Thread lock
        self.reader = None
        self.writer = None

    async def startServer(self):  # Start the server
        server = await asyncio.start_server(self.clientConnected, port=8888)
        addr = server.sockets[0].getsockname()
        print('Serving on ' + str(addr))

    async def clientConnected(self, reader, writer):  # Called when a client connects
        self.reader = reader
        self.writer = writer
        print('Client connected ===============================================')
        await self.sendPackets()

    async def sendPackets(self):
        while self.reader:
            localimage = None
            framedata = 0
            framenumber = 0
            jpgImage = 0
            size = 0

            with self.lock:
                # Use lock to avoid writing at same time as camera
                if self.info.image is not None:
                    localimage = self.info.image  # Copy image to save lock time
                    self.info.image = None
                    framedata = self.info.framedata
                    framenumber = self.info.frame
                else:
                    jpgImage = None
                    size = 0

            if localimage is not None:
                jpgImage = cv2.imencode('.jpg', localimage, [int(cv2.IMWRITE_JPEG_QUALITY),20])[1].tostring()
                size = len(jpgImage)

            # Create JSON header
            jsondata = {'a': 1, 'size': size, 'fdata': framedata, 'fnum': framenumber}
            jsonheader = json.dumps(jsondata).encode('utf-8')
            headerlength = len(jsonheader)
            print('JSON header: ' + str(jsondata))

            # Send JSON header
            #print('Sending header')
            self.writer.write(headerlength.to_bytes(2, byteorder='big'))
            self.writer.write(jsonheader)

            # Send jpg data
            if size != 0:
                self.writer.write(jpgImage)
            else:
                await asyncio.sleep(0.1)

            await self.writer.drain()
            await asyncio.sleep(0.02)

    def closeServer(self):
        self.writer.close()
        self.reader = None
        self.writer = None
