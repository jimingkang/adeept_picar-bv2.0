#!/usr/bin/python
import socket
import zmq
import time
from threading import Thread
import cv2
import base64

try:
    from picar import PiCar
except:
    print("No Picar did not load")

clientaddr = '192.168.1.151'
clientaddr = '192.168.1.156'
clientaddr = '192.168.0.146'
clientaddr = '192.168.0.169'

#TODO: include some basic safety protocols to ensure car doesn't crash

class Reciever(Thread):
    def __init__(self, addr="", port = 5000):
        Thread.__init__(self, daemon=True)

        self.size = 1024
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #???
        sock.bind((addr,port))
        sock.listen(5) 
        self.client,self.address = sock.accept()
        print("New client")
        self.cmd = None
        self.start()

    def recv_cmd(self):
        self.cmd = self.client.recv(self.size).rstrip().decode()
        return cmd

    def read(self):
        cmd = self.cmd
        self.cmd = None
        return cmd

    def run(self):
        while True:
            self.cmd = self.client.recv(self.size).rstrip().decode()
            


class FootageStream(Thread):
    '''Continuously serves requests for the latest frame'''
    
    def __init__(self, camera,addr,port=5555):
        print("initializing live stream")
        Thread.__init__(self)
        self.camera = camera
        context = zmq.Context()
        self.sock = context.socket(zmq.PUB)
        self.sock.connect('tcp://{}:{}'.format(addr[0],port)) #??? why not bind
        
        print("starting thread")
        self._running = False
        self.start()

    def run(self):
        '''Send images to the connected socket'''
        self._running = True
        while(self._running):
            #TODO: adjust this to match the picamera commands
            ret,image = self.camera.read()
            #image = cv2.resize(frame, (640,480))
            
            #if self.mode == 'opencv':
            #    pass #TODO: impliment open cv modes
            
            # send image to client
            encoded, buffer = cv2.imencode('.jpg', image)
            jpg_as_text = base64.b64encode(buffer)
            #TODO: send as a numpy array
            self.sock.send(jpg_as_text)
            
        # Runs after close
        self.sock.shutdown()
        self.sock.close()

    def close(self):
        self._running=False
        
            
def main():
    '''Start the picar and wait for commands'''
    print("Initializing reciever")
    reciever = Reciever()
    print("Initializing car")
    with PiCar() as car:
        stream = FootageStream(camera=car.camera,addr = reciever.address)
        while True: #TODO: detect when socket is broken properly
            #print("command?")
            cmd = reciever.read()

            '''
            # Safety stop
            dist = car.sonar.ping()
            if car._mode:
                if dist<.2:
                    car._mode = None
                    car._stopped = True
                    car.ebrake()
                    cmd = None

            '''
            
            # Override commands here
            if cmd == "all_stop":
                car.all_stop()
                car._mode=None

            if cmd =="follow_line":
                if car._mode=='follow_line':
                    car._mode=None
                    car.all_stop()
                else:
                    car._mode = 'follow_line'
                    follow = car.follow_line(darkLine=False,
                                             speed=1,
                                             gain=(10,60,0),
                                             nHist = 100,
                                             runTime = 1,
                                             coastTime = .5,
                                             maxAng = 30
                    )

                    
            # Continue running current mode
            if car._mode == None:
                car.run_cmd(cmd)
            elif car._mode == 'follow_line':
                try:
                    next(follow)
                except:
                    print("Couldnt follow line")
                    car._mode=None
            elif car._mode == 'track_object':
                pass
            else:
                pass
                

        stream.close()
        car.all_stop()


if __name__=="__main__":
    main()
            
