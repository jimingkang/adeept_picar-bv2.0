#!/usr/bin/python3
# File name   : findline.py
# Description : line tracking 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12
import RPi.GPIO as GPIO
import time
import motor
import turn
import led
import numpy

def num_import_int(initial):        #Call this function to import data from '.txt' file
    with open("set.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=int(snum)
    return n

#??? do I use all of these
status     = 1          #Motor rotation
forward    = 1          #Motor forward
backward   = 0          #Motor backward

left_spd   = num_import_int('E_M1:')         #Speed of the car
right_spd  = num_import_int('E_M2:')         #Speed of the car
left       = num_import_int('E_T1:')         #Motor Left
right      = num_import_int('E_T2:')         #Motor Right

# these had to be switched
# for some reason the originals were wrong...
#line_pin_right = 19
#line_pin_left = 20
line_pin_right = 20
line_pin_middle = 16
line_pin_left = 19

#right 280, middle 370, left 500
#TODO: allow these to be more controlled
midTurn = 370
shallowTurn = 20

#??? why are these colors like this
left_R = 22
left_G = 23
left_B = 24

#??? why are these colors like this
right_R = 10
right_G = 9
right_B = 25

#??? never used
#on  = GPIO.LOW
#off = GPIO.HIGH

spd_ad_1 = 1
spd_ad_2 = 1

class LineFinder:

    def __init__(self):
        self.readerInput = [0,0,0]
        self.observations = [[0,0,0], #TODO: add as default options
                             [0,0,0],
                             [0,0,0],
                             [0,0,0],
                             [0,0,0],
                             [0,0,0],
                             [0,0,0],
                             [0,0,0],
                             [0,0,0],
                             [0,0,0],
                             [0,0,0],
                             [0,0,0]]

        # Set up pins for linereader
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(line_pin_right,GPIO.IN)
        GPIO.setup(line_pin_middle,GPIO.IN)
        GPIO.setup(line_pin_left,GPIO.IN)

        # Define PID controller
        self.pCorrection = 5
        self.iCorrection = 1
        self.dCorrection = 1
        
        try:
            motor.setup()
        except: #??? what exception are 
            pass 

    def update(self):
        '''
        update control algorithm

        Observations come in the form of [L M R]
        L: left side input (0:1)
        M: middle input (0:1)
        R: right side input (0:1)

        '''
        readerInput = [GPIO.input(line_pin_right),
                       GPIO.input(line_pin_middle),
                       GPIO.input(line_pin_left)]

        print(readerInput)
        self.observations.append(readerInput)
        print(self.observations)
        return(readerInput)

    def simple_pid(self, status=None,
                   center = 0, fullTurn = 45, shallowTurn = 15):
        '''
        Return a turn angle and motor speed based latest observation
        '''
        if status==None:
            status = self.update()
        
        if   status==[0,0,0]:
            wheelAngle = center
        elif status==[1,0,0]:
            wheelAngle = fullTurn
        elif status==[1,1,0]:
            wheelAngle = shallowTurn
        elif status==[0,0,1]:
            wheelAngle = -fullTurn
        elif status==[0,1,1]:
            wheelAngle = -shallowTurn
        elif status==[1,0,1]:
            wheelAngle = center
        elif status==[0,1,0]:
            wheelAngle = center
            
        #TODO: raise error properly
        elif status==[1,1,1]:
            pass
        else:
            pass

        return wheelAngle

        
    def discrete_pid(self, observations = None):
        '''
        Return a turn angle and motor speed based on observations

        As the car spends more time off the track,
        all numbers and min number go up.
        the difference between max and center represents initial angle off track
        or something like that
        '''
        if observations==None:
            observations = self.observations

        pError = observations[0]
        iError = [sum(i) for i in zip(*observations)]  # get a sum of all
        #TODO: figure out the d error
        dError = [0,0,0]
        # d error could be based on current turn angle
        # or difference between top and bottom

        # Sum up the error values with their corrections
        error = [sum(i) for i in zip((self.pCorrection*pError,
                                      self.iCorrection*iError,
                                      self.dCorrection*dError))]

        wheelAngle = error[0]-error[2]
        if wheelAngle>0:
            wheelAngle -= error[1]
        elif wheelAngle<0:
            wheelAngle += error[1]
        else:
            pass

        return wheelAngle
            
        

    def run():
        '''
        Turn wheels based on observation of lineFinder
        '''

        #self.update()
        #wheelAngle = self.discrete_pid()
        # Line following decision
        try:
            wheelAngle = self.simple_pid()
            print(wheelAngle)
        except:
            print("Line not found")
            
        
        #TODO: fininish the turn


'''
def line_finder_2(status):
    if status==[0,0,0]:
        turn.middle()
        motor.motor_right(status,backward,right_spd*spd_ad_1)
        pass
    elif status==[1,0,0]:
        turn.turn_ang(midTurn-shallowTurn)
        motor.motor_right(status,backward,right_spd*spd_ad_2)
    elif status==[1,1,0]:
        turn.right()
        motor.motor_right(status,backward,right_spd*spd_ad_2)
    elif status==[0,0,1]:
        turn.turn_ang(midTurn+shallowTurn)
        motor.motor_right(status,backward,right_spd*spd_ad_2)
    elif status==[0,1,1]:
        turn.left()
        motor.motor_right(status,backward,right_spd*spd_ad_2)
    elif status==[1,0,1]:
        print("[1,0,1] status confusing")
        pass
    elif status==[0,1,0]:
        print("[0,1,0] thin line")
        pass
    elif status==[1,1,1]:
        #turn.middle()
        motor.motor_right(status,forward,right_spd*spd_ad_2)
    else:
        print("I'm confused")
        pass
'''

'''
def line_finder_1(status):
    status_middle,status_right,status_left =status
    status_middle == 0:
        #print("Go forward")
        turn.middle()
        led.both_off()
        led.yellow()
        #motor.motor_left(status, forward,left_spd*spd_ad_1)
    elif status_right == 0:
        #print("Turn left")
        turn.left()
        led.both_off()
        led.side_on(left_R)
        #motor.motor_left(status, forward,left_spd*spd_ad_2)
        motor.motor_right(status,backward,right_spd*spd_ad_2)
    elif status_left == 0:
        #print("Turn right")
        turn.right()
        led.both_off()
        led.side_on(right_R)
        #motor.motor_left(status, forward,left_spd*spd_ad_2)
        motor.motor_right(status,backward,right_spd*spd_ad_2)
    else:
        print("Go backward")
        #turn.middle()
        led.both_off()
        led.cyan()
        #motor.motor_left(status, backward,left_spd)
        motor.motor_right(status,forward,right_spd)
'''


if __name__ == '__main__':
    try:
        lineFollower = LineFinder()
        while True:
            lineFollower.update()
    except KeyboardInterrupt:
        motor.motorStop()

    
