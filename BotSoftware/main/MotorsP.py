"""
This file controls the motor outputs.
Called frequently with forward and angular velocity values. Must be non-blocking or asynchronous.
It's designed to be swapped out with another file with the same functions, for a different motor setup
"""

import RPi.GPIO as GPIO
import asyncio

# Pi GPIO motor pin setup
LFPin = 12  # Left forward
LRPin = 16  # Left backward
RFPin = 24  # Right forward
RRPin = 25  # Left backward

PWMFreq = 200  # Motor PWM frequency


class Motors:
    def __init__(self, enabled=False):

        # Initialise the pins and outputs. Run by main at startup.

        # Set up GPIOs pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([LFPin, LRPin, RFPin, RRPin], GPIO.OUT)

        # Set PWM frequencies
        self.LF = GPIO.PWM(LFPin, PWMFreq)
        self.LR = GPIO.PWM(LRPin, PWMFreq)
        self.RF = GPIO.PWM(RFPin, PWMFreq)
        self.RR = GPIO.PWM(RRPin, PWMFreq)

        # Initialise PWM outputs - 100 = high = motors off
        self.LF.start(100)
        self.LR.start(100)
        self.RF.start(100)
        self.RR.start(100)

        self.enabled = enabled  # This parameter enables the motors, set in main program

    def output(self, x, y):

        # Set the motor speeds with variables representing forward velocity and rotation

        # x is the rotation value
        # y is forward/reverse
        # Both are +/-50

        # Range check
        if x > 50: x = 50
        if x < -50: x = -50
        if y > 50: y = 50
        if y < -50: y = -50

        # Calculate wheel speeds from x and y (Wheel speeds range from 0-100)
        LW = y + x  # Left wheel
        RW = y - x  # Right wheel

        if self.enabled is True:  # Set PWM outputs only if motors are enabled

            # Convert wheel speeds to PWM outputs
            if LW > 0:
                self.LF.ChangeDutyCycle(100 - LW)
                self.LR.ChangeDutyCycle(100)
            elif LW < 0:
                self.LF.ChangeDutyCycle(100)
                self.LR.ChangeDutyCycle(100 + LW)
            else:
                self.LF.ChangeDutyCycle(100)
                self.LR.ChangeDutyCycle(100)

            if RW > 0:
                self.RF.ChangeDutyCycle(100 - RW)
                self.RR.ChangeDutyCycle(100)
            elif RW < 0:
                self.RF.ChangeDutyCycle(100)
                self.RR.ChangeDutyCycle(100 + RW)
            else:
                self.RF.ChangeDutyCycle(100)
                self.RR.ChangeDutyCycle(100)

    async def beepOk(self):

        # Make motors beep by controlling PWM frequency

        self.LF.ChangeFrequency(3520)  # A7
        self.LF.ChangeDutyCycle(80)
        await asyncio.sleep(0.025)

        self.LF.ChangeDutyCycle(100)
        await asyncio.sleep(0.1)

        self.LF.ChangeFrequency(5274)  # E8
        self.LF.ChangeDutyCycle(80)
        await asyncio.sleep(0.025)

        self.LF.ChangeDutyCycle(100)
        self.LF.ChangeFrequency(PWMFreq)

    async def beepError(self):

        # Make motors beep by controlling PWM frequency

        self.LF.ChangeFrequency(3520)  # A7
        self.LF.ChangeDutyCycle(80)
        await asyncio.sleep(0.05)

        self.LF.ChangeDutyCycle(100)
        await asyncio.sleep(0.1)

        self.LF.ChangeFrequency(3520)  # A7
        self.LF.ChangeDutyCycle(80)
        await asyncio.sleep(0.05)

        self.LF.ChangeDutyCycle(100)
        self.LF.ChangeFrequency(PWMFreq)
