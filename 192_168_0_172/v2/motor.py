#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

#motor = Motor(17,27,18)

class Motor():
    '''Class to control a motor'''

    def __init__(self, en, pin1, pin2):
        '''Set up pins and start motor'''

        GPIO.setwarnings(False)  #??? is this global
        GPIO.setmode(GPIO.BCM)   #??? is this global
        GPIO.setup(en, GPIO.OUT)
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)

        self.en = en
        self.pin1 = pin1
        self.pin2 = pin2

        self.pwm = 0
        # this could pop an error and need try: except: pass
        self.pwm = GPIO.PWM(en,1000)
            

    def stop(self):
        '''Stops motor'''
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)
        GPIO.output(self.en,   GPIO.LOW)

    def forward(self, speed):
        '''Drives forward'''
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin2, GPIO.LOW)
        self.pwm.start(100)
        self.pwm.ChangeDutyCycle(speed)

    def reverse(self, speed):
        '''Drives backwards'''
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.HIGH)
        self.pwm.start(100)
        self.pwm.ChangeDutyCycle(speed)

    def drive(self, speed):
        '''checks direction and moves'''
        if speed>0:
            self.forward(speed)
        elif speed<0:
            self.reverse(-speed)
        else:
            self.stop()

    def __exit__():
        self.stop()
        GPIO.cleanup()
            
