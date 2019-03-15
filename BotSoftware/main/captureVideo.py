import time
from picamera import PiCamera
import io

# CONSTANTS
FRAME_RATE = 30
ISO = 400
EXPOSURE_TIME = 30  # msec #8 good for no colour break up on proj
MANUAL_EXPOSE = True
CAMERA_RES = (640, 480)  # 1640x1232, 1640,922, 640x480


class capture():
    # Start video capture
    camera = None

    def __init__(self):
        print(FRAME_RATE, 'fps')

        self.camera = PiCamera(resolution=CAMERA_RES, framerate=FRAME_RATE, sensor_mode=7)
        self.camera.image_denoise = False
        self.camera.iso = ISO

        # Use auto white balance (values output later)
        self.camera.awb_mode = 'auto'

        # Use manual white balance (use auto values)
        #self.camera.awb_mode = 'off'
        #self.camera.awb_gains = (1.03, 1.7)

        time.sleep(2)  # Wait camera start up and AWB to stabilise
        g = self.camera.awb_gains
        print(g)

        print('auto shutter speed:', self.camera.exposure_speed)

        # Lock exposure
        if MANUAL_EXPOSE is True:
            self.camera.shutter_speed = int(EXPOSURE_TIME*1000)
            print('manual shutter speed', self.camera.shutter_speed)

        # Start preview
        self.camera.start_preview()

        time.sleep(1)


    def startVideoAndProcessing(self, realTimeProcessing):
        try:
            self.camera.start_recording(realTimeProcessing, format='bgr')

        except Exception as e:
            print("Camera video error:", e)
        return True

    def wait(self, time):
        try:
            self.camera.wait_recording(time)
        except Exception as e:
            print("Camera video error:", e)
            return False
        return True

    def stopVideo(self):
        try:
            self.camera.stop_recording()
        except Exception as e:
            print("Camera video error:", e)
        return True

    def closeCamera(self):
        #self.camera.stop_preview()
        self.camera.close()

    def captureColourJPG(self):
        # resolution should be set to 1440,1088
        img = None
        try:
            mStream = io.BytesIO()
            self.camera.capture(mStream, format='jpeg', use_video_port=True, resize=(640, 480), quality=10)  # TODO can I hardware resize for speed?
        except Exception as e:
            print("Camera error", e)
            return None
        #mStream.close()
        return mStream


if __name__ == "__main__":
    mCapture=capture()
    #print(mCapture.getImage())
    #print(mCapture.startVideo('testVideo.h264'))
    #mCapture.startVideoAndProcessing()
    #mCapture.wait(50)
    time.sleep(60)
    mCapture.closeCamera()
