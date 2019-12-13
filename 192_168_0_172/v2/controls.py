#! /bin/python3
'''
Set up controls for servos that control the car
'''

import Adafruit_PCA9685

# set up a pulse width modulation function to send to servos
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

class Servo():
    '''Servo class controls a servo'''

    def __init__(self, pwm_pin, center, minVal, maxVal, orientation=None):
        self.pwm_pin = pwm_pin
        self.center = center
        self.MIN = minVal
        self.MAX = maxVal
        self.fullRange = self.MAX-self.MIN
        self.orientation = orientation

        # set to initial position
        self.goto_center()

    def goto_center(self):
        '''Center servo'''
        pwm.set_pwm(self.pwm_pin, 0, self.center)

    def goto_max(self):
        pwm.set_pwm(self.pwm_pin, 0, self.MAX)
        
    def goto_min(self):
        pwm.set_pwm(self.pwm_pin, 0, self.MIN)

    def rotate(self,angle):
        '''Rotate to a specified value if in range'''   
        pwmVal = self.angle2pwm(angle)

        # Force range
        if pwmVal<self.MIN:
            print("Angle too small")
            pwmVal = self.MIN
        if pwmVal>self.MAX:
            print("Angle too large")
            pwmVal = self.MAX

        # change pwm value for specified servo
        #???: what is the 0 argument
        pwm.set_pwm(self.pwm_pin, 0, pwmVal)

    #TODO: define left right up down max based on orientation

    def set_pwm(self,val):
        '''change pwm value of pin directly'''
        pwm.set_pwm(self.pwm_pin, 0, val)

    def get_pwm(self):
        #TODO: impliment get_pwm
        pass
            
    def pwm2angle(self,pwmVal):
        '''converts pwm values to angles'''
        return int((pwmVal-self.center)*360./self.fullRange)

    def angle2pwm(self,angle):
        '''converts angles values to pwm'''
        return int(angle*self.fullRange/360. + self.center)
        

#steeringServo = Servo(2,370,500,280)
#panServo = Servo(1,310,476,140)
#tiltServo = Servo(0,425,295,662)
