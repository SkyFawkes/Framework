'''
Asynchronous client

Runs on PC
Connects to aServerBot.py running on Pi

Based on asyncClient2.py

'''

import asyncio
import json
import sys
import numpy as np
import cv2

# ServerName = 'localhost'  # Local
# ServerName = '172.24.136.105'  # Work
ServerName = 'piwars'  # Home

async def Receive():

    while True:
        while True:
            print('Looking for server')
            try:
                reader, writer = await asyncio.open_connection(host=ServerName, port=8888)
                print('Connected')
                break
            except:
                pass

        a = 0
        while True:

            # Read header size (2 bytes)
            data = await reader.read(2)  # Read header length (2 bytes)
            addr = writer.get_extra_info('peername')

            if not data:
                # No data received; server disconnected
                print('No response from server')
                break

            headerlength = int.from_bytes(data, byteorder='big')
            print(f"Header length: {headerlength!r} from {addr!r}")

            if headerlength > 1000:
                print('Header length seems too big')
                break

            # Read JSON header
            data = await reader.read(headerlength)

            if len(data) != headerlength:
                print('Did not receive expected header')
                break

            jsondata = json.loads(data)
            print(f"JSON header: {jsondata}")

            # Extract JSON info
            size = jsondata['size']
            a = jsondata['a']
            framedata = jsondata['framedata']

            if size > 0:
                # Read incoming data in loop to get full message
                data = b''
                left = size
                while left > 0:
                    data = data + await reader.read(left)
                    left = size - len(data)

                print('image received')
                array = np.frombuffer(data, np.uint8)
                image = cv2.imdecode(array, cv2.IMREAD_COLOR)
                image = cv2.line(image, (framedata, 0), (framedata, 480), (0, 255, 0), 2)
                image = cv2.line(image, (0, 240), (639, 240), (0, 255, 0), 1)

                print(image.shape)
                cv2.imshow("test", image)
                cv2.waitKey(1)

            #print("Responding with OK")
            #writer.write(b'OK')

            print(a)
            if a == 10:
                break

        print('Closing the connection')
        await writer.drain()  # Wait for output buffer to empty
        writer.close()


async def main():
    # New main routine, starts coroutines then checks continually for completion

    task1 = asyncio.create_task(Receive())  # Create data receiving task

    while True:
        # AllTasks = asyncio.Task.all_tasks()
        # print(AllTasks)

        #print(f'task1: {task1.done()}, task2: {task2.done()}')

        await asyncio.sleep(0.5)


assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
asyncio.run(main())
