#!/usr/bin/python3

from picamera import PiCamera
from picamera.array import PiRGBArray

import RPi.GPIO as GPIO
#GPIO.setwarnings(False) #??? global

import numpy as np
import time

class Sonar:

    def __init__(self, txPin=11, rxPin=8):
        self.soundSpeed = 340

        GPIO.setup(txPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(rxPin, GPIO.IN)
        
        self.tx = txPin
        self.rx = rxPin


    def __del__(self):
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self,exception_type, exception_value, traceback):
        self.close()

    def close(self):
        pass

    def ping(self, maxRange=1, pulseWidth=.000015): #TODO: impliment distance
        '''Measure return time of a single ping'''

        # Transmit ping
        GPIO.output(self.tx, GPIO.HIGH)
        time.sleep(pulseWidth)
        GPIO.output(self.tx, GPIO.LOW)

        while not GPIO.input(self.rx):
            #??? waiting for ping to stop. Should already be done though
            # Forces the time to start/end at end of ping. Falling edge
            pass 
        t1 = time.time()
        while GPIO.input(self.rx):
            # Forces the time to start/end at end of ping. Falling edge
            pass
        t2 = time.time()
        return (t2-t1)*self.soundSpeed/2


class LineSensor:
    '''Line sensor consisting of 3 elements in a linear array'''
    
    def __init__(self,pin_middle=16, pin_left=19, pin_right=20, blackLine=True):
        '''Create instance of Line Sensor'''
        
        # Set up pins for linereader
        #GPIO.setwarnings(False) #??? global
        #GPIO.setmode(GPIO.BCM)  #??? global

        self.pin_middle = pin_middle
        self.pin_left = pin_left
        self.pin_right = pin_right

        print("Starting line sensor")
        time.sleep(2)
        GPIO.setup(self.pin_middle,GPIO.IN)
        GPIO.setup(self.pin_left,GPIO.IN)
        GPIO.setup(self.pin_right,GPIO.IN)

    def __del__(self):
        '''Called on destruction of instance'''
        self.close()
    
    def __enter__(self):
        '''Called at start of with statement'''
        return self
    
    def __exit__(self,exception_type, exception_value, traceback):
        '''Called at the end of with statement'''
        self.close()

    def __call__(self):
        '''Return the current state of the line sensor'''
        return np.array([GPIO.input(self.pin_left),
                         GPIO.input(self.pin_middle),
                         GPIO.input(self.pin_right)])

    def close(self):
        pass


class Camera(PiCamera):
    '''Camera class class which can read or stream over a socket'''

    def __init__(self, resolution=(640.480)):
        '''Constructor for camera'''

        print("Initializing picamera")
        PiCamera.__init__(self, resolution = resolution)
        time.sleep(1) # Give camera time to start up
        
        # Set up buffer for capture
        self.rawCapture = PiRGBArray(self)
        self.rawCapture.truncate(0)
        self.rawCapture.seek(0)
        
    def __del__(self):
        '''Destructor'''
        self.close()

    def __enter__(self):
        '''Called on with statement'''
        return self

    def __exit__(self,exception_type, exception_value, traceback):
        '''Called on exit from with statement'''
        self.close()

    def close(self):
        '''Close camera nicely'''
        PiCamera.close(self)

    def read(self):
        '''Return frame same as cv2.read()'''
        self.rawCapture.truncate(0)
        self.rawCapture.seek(0)
        PiCamera.capture(self,self.rawCapture, format="bgr",
                         use_video_port=True)
        return True,self.rawCapture.array

    def stream(self,sock):
        '''Continuous capture and send over network'''

        # Reset buffer
        self.rawCapture.truncate(0)
        self.rawCapture.seek(0)

        # Take pictures and send to client as quickly as client can handle
        for frame in self.capture_continuous(output=self.rawCapture,
                                             format= "bgr",
                                             use_video_port=True):

            # reformat image for sending
            image = frame.array
            encoded,buffer = cv2.imencode('.jpg',image)
            jpg_as_text = base64.b64encode(buffer)

            #TODO: send as numpy array and avoid using opencv
            # Send to client
            sock.send(jpg_as_text)

            # Reset buffer
            self.rawCapture.truncate(0)
            self.rawCapture.seek(0)
    

