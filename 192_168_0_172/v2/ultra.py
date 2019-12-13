#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

#transmitPin = 11?
#receivePin = 8?
soundSpeed = 340

class UltraSounder:
    '''Class that runs the ultra-sounder'''

    def __init__(self, transmitPin=11, recievePin=8):
        #GPIO.setmode(GPIO.BCM) #??? global
        GPIO.setup(transmitPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(recievePin, GPIO.IN)
        
        self.tx = transmitPin
        self.rx = recievePin


    def ping(self, pulseWidth = .000015):
        '''Send out a ping'''

        GPIO.output(self.tx, GPIO.HIGH)
        time.sleep(pulseWidth)
        GPIO.output(self.tx, GPIO.LOW)

    
    def check_distance(self,pulseWidth = .000015):
        '''Single ping and check distance'''

        self.ping(pulseWidth)
        while not GPIO.input(self.rx):
            #??? waiting for ping to stop. Should already be done though
            # Forces the time to start/end at end of ping. Falling edge
            pass 
        t1 = time.time()
        while GPIO.input(self.rx):
            # Forces the time to start/end at end of ping. Falling edge
            pass
        t2 = time.time()
        return (t2-t1)*soundSpeed/2

    @property
    def distance(self):
        ''' Static method for functions that need to grab it quickly'''
        return self.check_distance()

    def scan(self,servo, speed=3):
        '''Scan sonar distances across a servo'''

        #TODO: impliment a reverse scan?
        
        distances = []
        bearings = []
        servo.goto_min()
        val = servo.MIN

        time.sleep(.5) # position servo

        #TODO: see if we can allow warnings
        #??? why don't we want warnings... #??? should this be global
        GPIO.setwarnings(False) #Or it may print warnings

        while val < servo.MAX:
            servo.set_pwm(val)
            distances.append(str(round(self.ping(),2)))
            bearings.append( servo.pwm2angle(val) )

            val -= speed #??? this is hard to conceptulize

        # return to home
        servo.goto_center()
        return val,distances
        

    def __exit__(self):
        GPIO.cleanup()
        
        
        
        
