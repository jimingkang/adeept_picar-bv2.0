#!/usr/bin/python3

# Imports


# Custom libraries
import led

from motor import Motor
from controls import Servo
from ultra import UltraSounder
from camera import Camera

from connection import ClientConnection


class PiCar:
    '''Builds a PiCar class'''

    def __init__(self):
        #TODO: impliment some behaviour if no client is found
        #client = ClientConnection()

        self.tilt     = Servo(pwm_pin=0,center=515,minVal=425,maxVal=650)
        self.pan      = Servo(1,330,60,600)
        self.wheel    = Servo(2,370,180,520)

        #motor = Motor(4,14,15)
        self.motor = Motor(17,27,18)

        self.sonar = UltraSounder()
        self.camera = Camera(sonar=self.sonar,clientAddr=None)

        #TODO: give car access to leds
        # mainly so it can do the police car thing

    def drive_f(self,speed=100):
        '''
        Drive forward
        
        If no speed is specified, go full speed
        '''
        self.motor.drive(speed)
        pass
    
    def drive_r(self,speed=100):
        '''
        Drive in reverse

        If no speed is specified, go full speed
        '''
        self.motor.drive(-speed)
        pass
    
    def turn_l(self,angle=None):
        '''
        Turn wheels to the left

        If no angle specified, incriment from current position
        '''
        if angle:
            self.wheel.rotate(angle)
        else:
            self.wheel.goto_max()
            
        pass
    
    def turn_r(self,angle=None):
        '''
        Turn wheels to the right

        If no angle specified, incriment from current position
        '''
        if angle:
            self.wheel.rotate(-angle)
        else:
            self.wheel.goto_min()
        pass
    
    def look_l(self,angle=None):
        '''
        Pan head to the left

        If no angle specified, incriment from current position
        '''
        if angle:
            self.pan.rotate(angle)
        else:
            self.pan.goto_max()

        pass
    
    def look_r(self,angle=None):
        '''
        Pan head to the right

        If no angle specified, incriment from current position
        '''
        if angle:
            self.pan.rotate(-angle)
        else:
            self.pan.goto_min()

        pass
    
    def look_u(self,angle=None):
        '''
        Tilt head up

        If no angle specified, incriment from current position
        '''

        if angle:
            self.tilt.rotate(angle)
        else:
            self.pan.goto_max()

        pass
    
    def look_d(self,angle=None):
        '''
        Tilt head down

        If no angle specified, incriment from current position
        '''
        if angle:
            self.tilt.rotate(-angle)
        else:
            self.pan.goto_min()
        
        pass
    
    def all_stop(self):
        '''Stop motor'''

        self.motor.stop()

        pass

    def all_ahead(self):
        '''Move all servos to center position'''

        self.wheel.goto_center()
        self.pan.goto_center()
        self.tilt.goto_center()

        pass

    def sonar_scan(self,):
        '''Scan sonar from left to right'''
        
        pass

    def __del__(self):
        '''Close everything nicely so the resources can be used again'''
        self.camera.close()
        pass #TODO: impliment code that closes everything nicely


    def shakedown(self):
        '''Run through all capabilities'''
        pass
