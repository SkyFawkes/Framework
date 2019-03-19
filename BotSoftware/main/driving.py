import motorController
from time import sleep
import pygame
import sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode([10,10]) #make a 10x10 window


motors = motorController.motorController()
speed = 0
distance = 0
running = True
mode = True #speed mode while true, distance mode while false
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_w:
            speed = speed + 1
            mode = True
        elif event.type == KEYDOWN and event.key == K_s:
            speed = speed - 1
            mode = True
        elif event.type == KEYDOWN and event.key == K_x:
            speed = 0
            mode = True
        elif event.type == KEYDOWN and event.key == K_a:
            distance = 10
            mode = False
            motors.setDistance(distance,distance,50,50)
        elif event.type == KEYDOWN and event.key == K_d:
            distance = -10
            mode = False
            motors.setDistance(distance,distance,50,50)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
            speed = 0
            mode = True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
            running = False
            speed = 0
            mode = True

    if mode == True:
        motors.setMotorSpeed(speed,speed)
