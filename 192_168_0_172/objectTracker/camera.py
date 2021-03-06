from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import zmq
import base64
import numpy as np
import time


def send_array(socket, A, flags=0, copy=True, track=False):
    """send a numpy array with metadata"""
    A =  np.ascontiguousarray(A)
    md = dict(
        dtype = str(A.dtype),
        shape = A.shape,
    )
    socket.send_json(md, flags|zmq.SNDMORE)
    return socket.send(A, flags, copy=copy, track=track)

class Camera(PiCamera):

    def __init__(self, sonar=None, clientAddr=None, clientPort = 5555, resolution = (640,480)):
        PiCamera.__init__(self)
        self.resolution = resolution
        self.mode=None
        self.sonar = sonar

        self.rawCapture = PiRGBArray(self)
        self.rawCapture.truncate(0)
        self.rawCapture.seek(0)

        # Start stream
        #self.stream()

    def stream(self,addr='192.168.0.169',port = 5555):
        '''Send live stream'''

        # Now connect the camera socket
        context = zmq.Context()
        footageSocket = context.socket(zmq.PUB)
        footageSocket.connect('tcp://{}:{}'.format(addr,port))

        self.rawCapture.truncate(0)
        self.rawCapture.seek(0)
        
        #font = cv2.FONT_HERSHEY_SIMPLEX
        for frame in self.capture_continuous(output=self.rawCapture,
                                               format = "bgr",
                                               use_video_port=True):

            image = frame.array

            # draw cross on image
            #cv2.line(image,(300,240),(340,240),(128,255,128),1)
            #cv2.line(image,(320,220),(320,260),(128,255,128),1)

            if self.mode == 'opencv':
                pass #TODO: impliment open cv modes
                
            '''
            try:
                if self.sonar.distance < 8:
                    cv2.putText(image,'%s m'%str(round(self.sonar.distance,2)),
                                (40,40), font, 0.5,(255,255,255),
                                1,cv2.LINE_AA)
            except:
                pass
            '''


            # send image to client
            encoded, buffer = cv2.imencode('.jpg', image)
            jpg_as_text = base64.b64encode(buffer)
            footageSocket.send(jpg_as_text)
            #footageSocket.send(image)
            #send_array(footageSocket,image)
            
            
            self.rawCapture.truncate(0)
            self.rawCapture.seek(0)

            #time.sleep(.1)

if __name__=="__main__":
    camera = Camera()
    camera.stream(addr='192.168.0.169')

            
