'''Test of line following'''

from threading import Thread

import controls
import sensors

import numpy as np
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

motor = controls.Motor(17,27,18)
turn = controls.Servo(2,180,520,370,-25,25,0)

lineSensor = sensors.LineSensor(pin_middle=16,
                                     pin_left=19,
                                     pin_right=20,
                                     blackLine=True)

def pulse(runTime, coastTime):
    while not stop:
        motor.forward(100)
        time.sleep(runTime)
        motor.coast()
        time.sleep(coastTime)

runTime = .2
coastTime = .2

motorThread = Thread(target=pulse, args=(runTime,coastTime))

stop = False

motorThread.start()

nHist = 1000

kp = 5
ki = 1
kd = 1


obs = np.ones((nHist,3))

while not stop:
    current = lineSensor()
    if (current = [1, 1, 1]).all():
        current=obs[-1]
        
    obs[:-1] = obs[1:]
    #print(obs[-1])
    [left,center,right] = obs.sum(0)
    
    P = right-left
    I = P*center
    D = 3000-(right+left+center)

    turnAng = kp*P+ki*I/(kd*D+1)
    #turnAng = P
    print([kp*P, ki*I, kd*D, turnAng])
    #print(turnAng)
    turnAng = max(turnAng, -15)
    turnAng = min(turnAng, 15)
    turn.goto(turnAng)
    time.sleep(.1)
    

stop = True
motorThread.join()
                     
