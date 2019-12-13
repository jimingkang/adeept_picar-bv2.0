#!/usr/bin/python3
import controls
import sensors
from threading import Thread

import numpy as np
import time

import RPi.GPIO as GPIO
#GPIO.setwarnings(False) #??? In original code
GPIO.setmode(GPIO.BCM)  # Set pin numbering system for board

#TODO: move all classes into a single file

class Safety(Thread):

    def __init__(self,car):
        Thread.__init__(self)
        self.car = car
        self.running = False
        #self.start()
        
    def run(self):
        self.running = True
        while self.running:
            time.sleep(.5)
            dist = self.car.sonar.ping()
            if dist<.3:
                self.car._mode = None
                self.car._stopped = True
                self.car.all_stop()
                

class PiCar:
    '''
    Provides an interface to control the car.

    Upon construction, this class initializes all controls and sensors.
    For controls, the car has a motor, a turning servo, and 2 servos controlling the head.
    For sensors, the car has a line sensor, a sonar, and a camera.
    The constructor expects all the peripherals to be plugged into the pi in a specific manner which can only be changed by directly changing the code of the constructor.
    '''

    def __init__(self):
        # Controls
        print("Initializing controls")
        self.motor = controls.Motor(17,27,18)
        self.tilt = controls.Servo(0,425,650,515,-30,30,0)
        self.pan = controls.Servo(1,160,650,395,-90,90,0)
        self.turn = controls.Servo(2,180,520,370,-45,45,0)

        # Sensors
        print("Initializing sensors")
        self.camera = sensors.Camera( resolution=(640,480) )
        self.sonar = sensors.Sonar()
        self.lineSensor = sensors.LineSensor(pin_middle=16,
                                             pin_left=19,
                                             pin_right=20,
                                             blackLine=True)
        # Variables
        self._mode = None
        self._stopped=False

        # Start safety thread
        self.safety_thread = Safety(car = self)
        #self.safety_thread.start()
        

    
    def __del__(self):
        self.close()


    def __enter__(self):
        return self


    def __exit__(self,exception_type, exception_value, traceback):
        self.close()


    def close(self):
        self.all_stop()
        self.safety_thread.running = False
        self.safety_thread.join()
        self.camera.close()
        GPIO.cleanup() #??? originally in sonar?


    def all_stop(self):
        '''Stop the car and face forward. Exit any current mode'''
        self._stopped = True
        self.motor.stop()
        self.all_ahead()

    def all_ahead(self):
        '''Bring all controls to forward'''
        self.turn.center()
        self.tilt.center()
        self.pan.center()

    def ebrake(self, dir=1):
        '''
        Hard brake by reversing for a second
        
        Change dir to -1 to use ebrake when reversed
        '''
        
        self.motor.pulse(dir*100,.2)


    def run_cmd(self, cmd,arg=None):
        '''Run a preset command'''
        # Must match client side commands
        if cmd == 'disconnect':
            self.close()
        elif cmd == 'forward':
            #self.motor.pulse(100,.1)
            self.motor.forward(100)
        elif cmd == 'reverse':
            #self.motor.pulse(-100,.1)
            self.motor.reverse(100)
        elif cmd == 'stop':
            self.motor.stop()
        elif cmd == 'coast':
            self.motor.coast()
        elif cmd == 'all_stop':
            self.all_stop(),
        elif cmd == 'all_ahead':
            self.all_ahead()
        elif cmd == 'left':
            self.turn.rotate(30)
        elif cmd == 'right':
            self.turn.rotate(-30)
        elif cmd== 'straight':
            self.turn.center()
        elif cmd == 'tilt_down':
            self.tilt.rotate(-1)
        elif cmd == 'tilt_up':
            self.tilt.rotate(1)
        elif cmd == 'pan_left':
            self.pan.rotate(1)
        elif cmd == 'pan_right':
            self.pan.rotate(-1)
        else:
            pass

    def sonar_scan(self, distance=1, scanSpeed=1, tiltAngle = 0): #TODO: impliment distance
        '''Measure distances across full range of sonar

        Car will first look all the way to the left. It will then slowly turn all the way to the right, while making a sonar measurement at each angle.
        distance determines how long the ping should wait for a response.
        scanSpeed determines how far apart the pings are angularly. A slower scanSpeed means more pings and denser set of results. scanSpeed must be an integer greater than 0.

        sonar_scan() returns a list of distances and a second list of corresponding angles.
        '''

        self.tilt.goto(tiltAngle)
        angles = [ang for ang in range(self.pan.MIN,
                                       self.pan.MAX+scanSpeed,
                                       scanSpeed)]
        for angle in angles:
            self.pan.goto(angle)
            results.append(self.sonar.ping(distance))

        return results, angles


    def pulse(self,runTime, coastTime):
        '''
        Continuously pulse the motor.

        Generally, this method should be called as a thread to run in the background. Otherwise it will block the program from running.
        '''
        self._stopped = False
        while not self._stopped:
            self.motor.forward(100)
            time.sleep(runTime)
            self.motor.coast()
            time.sleep(coastTime)
        self._stopped = True

    def follow_line(self, darkLine = False, speed=1,
                    gain = (1,1,1), nHist = 100,
                    runTime = .2, coastTime = .2,
                    maxAng = 15):
        '''
        Look for a line and drive along following it

        The follow line is a generator needs to be continuously called in order to continue following the line. 
        '''

        self._mode='follow_line'
        print("Line following mode")
        # Set up a history of observations
        obs = np.zeros((nHist,3))

        #motorThread = Thread(target=self.pulse, args=(runTime,coastTime))
        #motorThread.start()

        P = 0
        turnAng = 0
        while self._mode=='follow_line':
            # If about to run into wall, ebrake and shut off
            #TODO: unduplicate this code
            if self.sonar.ping()<.2:
                self.ebrake()
                self.all_stop()
                # this should also break the loop, but just in case
                return

            # Take measure with line sensor
            current = self.lineSensor() # Place new observation on the end
            if (current==[1,1,1]).all():
                current = obs[-1] 
            if (current==[1,0,1]).all():
                current = obs[-1] 
            obs[:-1] = obs[1:] # Drop first in observation
            obs[-1] = current
            #print(obs[-1])
            # Determine wheel angle based on control algorithm
            [left, center, right] = obs.sum(0)

            #Pprev = P
            P = current[2]-current[0]
            I = P*abs(right-left)/nHist
            D = (nHist-center)/nHist     # Hi if recently on line
            D = abs(turnAng/maxAng)
            # D will be 1 or 0
            # 1 means close to line (small turn)
            
            turnAng = (P*gain[0] + gain[1]*I) / (gain[2]*D+1)
            if turnAng>maxAng:
                turnAng = maxAng
            elif turnAng < -maxAng:
                turnAng = -maxAng
                
            print("{}  {} {}".format([left,center,right],[round(P), round(I), round(D)], round(turnAng)))
            
            # Pulse motor and turn wheels according to control algorithm
            self.turn.goto(turnAng)
            #time.sleep(1)

            if abs(turnAng)<12:
                self.motor.forward(70)
            elif abs(turnAng)<30:
                self.motor.forward(95)
            else:
                self.motor.forward(100)

            yield

        self._stopped = True


    def track_object(self):
        '''Keep an object in view and follow it'''
        pass

    def explore(self):
        pass



if __name__=='__main__':
    car = PiCar()
    try:
        
        follow = car.follow_line(darkLine=False,
                        speed=1,
                        gain=(5,50,1),
                        nHist = 50,
                        runTime = 1,
                        coastTime = .5,
                        maxAng = 35
        )
        
        follow = car.follow_line(darkLine=False,
                        speed=1,
                        gain=(10,20,0),
                        nHist = 150,
                        runTime = 1,
                        coastTime = .5,
                        maxAng = 35
        )
        while car._mode=='follow_line':
            try:
                next(follow)
            except:
                car._mode=None
                

    finally:
        car.all_stop()

 
