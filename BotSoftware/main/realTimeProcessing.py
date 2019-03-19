import cv2
import numpy as np
import time

height = 240  # Height of video line to process

class RealTimeProcessing:
    def __init__(self, mCapture=None, mServer=None, info=None, lock=None):
        mCapture.startVideoAndProcessing(self)
        self.mServer = mServer  # Server to send data to periodically
        self.frameCount = 0
        self.info = info
        self.lock = lock

    def write(self, s):  # Called by camera whenever new frame is captured
        self.frameCount += 1

        starttime = time.time()
        bgr = np.frombuffer(s, dtype=np.dtype('B'))
        bgr = np.reshape(bgr, (480, 640, 3))
        bgr = cv2.flip(bgr, -1)  # If camera is upside down

        # Process frame
        maxIndex = self.findMaxGrad(bgr).item()

        with self.lock:  # Use lock to avoid writing at same time as main thread
            self.info.frame = self.frameCount
            self.info.framedata = maxIndex
            if self.frameCount % 1 == 0:
                self.info.image = bgr

        #print('Time to process frame: ' + str((time.time() - starttime) * 1000) + ' ms')

    def cannyTest(self, bgr):
        grey=cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        grey=cv2.Canny(grey, 100, 200, apertureSize=3)

    def houghTest(self,bgr):
        grey=cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        grey=cv2.Canny(grey, 100,200,apertureSize=3)

    def findMaxGradOld(self, bgr):
        line = bgr[height, 0:640, 1].astype(np.int16)  # 639 or 640?
        line = cv2.blur(line, (15, 15))  # (15,1)?

        grad = np.zeros(640, 'int16')
        for i in range(1, line.shape[0]):
            grad[i] = line[i-1]-line[i]

        Result = np.argmax(grad)
        return Result

    def findMaxGrad(self, bgr):
        line = bgr[height-2:height+2, 0:640, 1].astype(np.int16)  # Get 5-line strip from image
        line = cv2.resize(line, (640, 1), interpolation=cv2.INTER_AREA)
        line = cv2.blur(line, (15, 1))  # (15,1)?
        #print(line)

        grad = np.zeros(640, 'int16')
        for i in range(1, line.shape[1]):
            grad[i] = line[0,i-1]-line[0,i]

        Result = np.argmax(grad)
        return Result

    def findMaxGrad(self, bgr):
        line = bgr[height-2:height+2, 0:640, 0:2].astype(np.int16)  # Get 5-line strip from image
        line = cv2.resize(line, (640, 1), interpolation=cv2.INTER_AREA)
        line = cv2.blur(line, (15, 1))  # (15,1)?
        line = cv2.cvtColor(line, cv2.COLOR_BGR2HSV)
        #print(line)

        grad = np.zeros(640, 'int16')
        for i in range(1, line.shape[1]):
            grad[i] = line[0,i-1]-line[0,i]

        Result = np.argmax(grad)
        return Result

    def colourDetect(self, bgr):
        line = bgr[height, 0:639, 1].astype(np.int16)  # 639 or 640?
        line = cv2.blur(line, (15, 15))  # (15,1)?

        grad = np.zeros(640,'int16')
        for i in range(1, line.shape[0]):
            grad[i] = line[i-1]-line[i]

        maxIndex=np.argmax(grad)
        return maxIndex

    def flush(self):
        cv2.destroyAllWindows()
