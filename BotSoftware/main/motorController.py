import spidev
from time import sleep
import sys
import ctypes


class motorController():

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # SPI bus 0, device 0
        self.spi.max_speed_hz = 10000  # max speed of 1MHz, practical limit is 10kHz

    def __del__(self):
        self.spi.close()

    def setMotorSpeed(self, speed_r, speed_l):  # set the motor speed from -100 to + 100
        speed_r = speed_r + 128
        speed_l = speed_l + 128
        #data_out = [ord('S'), speed_r, speed_l, 255]  # test of Speed setting
        data_out = [ord('S'), speed_r, speed_l, 255]  # test of Speed setting
        recv = self.send(data_out)
        return recv

    def setDistance(self, distance_r, distance_l, speed_r,
                    speed_l):  # set the motor distance as a max speed. all in range of -100 to 100
        speed_r = speed_r + 128
        speed_l = speed_l + 128
        distance_r = distance_r + 128
        distance_l = distance_l + 128
        data_out = [ord('D'), distance_r, distance_l, speed_r, speed_l, 255]
        recv = self.send(data_out)
        return recv

    def setMaxAccel(self, maxAccel):
        data_out = [ord('A'), maxAccel, 255]
        recv = self.send(data_out)
        return recv

    def getADC(self, n):
        data_out = [ord('V'), n, 255]
        recv = self.send(data_out)
        return recv

    def send(self, data_out):
        print(data_out)
        r = self.spi.xfer(data_out)
        print('Sent ' + str(data_out))
        # print('Received '+ str(r))
        #        sleep(1)
        return r


if __name__ == "__main__":
    myMC = motorController()
    r = myMC.setMotorSpeed(10, 10)
    print('Received', str(r))
    r = myMC.setDistance(10, 10, 50, 50)
    print('Received', str(r))
    #    r=myMC.setMotorSpeed(10,10)
    #    print('Received', str(r))

    #    r=myMC.setMaxAccel(100)
    #    print('Received', str(r))
    #r = myMC.getADC(5)
    print('Received', str(r))
    #motorController.spi.close()