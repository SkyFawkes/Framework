"""
This file controls the motor outputs.
Called frequently with forward and angular velocity values. Must be non-blocking or asynchronous.
It's designed to be swapped out with another file with the same functions, for a different motor setup
"""

import RPi.GPIO as GPIO
import asyncio
import motorController



class Motors:
    def __init__(self, enabled=False):
        self.enabled=enabled
        self.mMotorControl=motorController.motorController()

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
            self.mMotorControl.setMotorSpeed(RW,LW)


    async def beepOk(self):
        print('beepOk')

    async def beepError(self):
        print('beepError')


