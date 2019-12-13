#!/usr/bin/python3

# Imports


# Custom libraries
import led

from motor import Motor
from controls import Servo
from ultra import UltraSounder

from connection import ClientConnection


class PiCar:
    '''Builds a PiCar class'''

    def __init__(self):
        #TODO: impliment some behaviour if no client is found
        #client = ClientConnection()

        self.tiltServo     = Servo(pwm_pin=0,center=515,minVal=425,maxVal=650)
        self.panServo      = Servo(1,330,60,600)
        self.steeringServo = Servo(2,370,180,520)

        #motor = Motor(4,14,15)
        self.motor = Motor(17,27,18)

        self.sonar = UltraSounder()
        self.camera = Camera(sonar.distance,client.addr)

        #TODO: give car access to leds
        # mainly so it can do the police car thing
        

    def close(self):
        self.camera.close()
        pass #TODO: impliment code that closes everything nicely


    def turn(self,direction,angle=None):

        pass

    def shakedown(self):
        '''Run through all capabilities'''
        pass
