from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2

class Camera(PiCamera):

    def __init__(self, distance, clientAddr, clientPort = 5555 resolution = (640,480)):
        PiCamera.__init__()
        PiCamera.resolution = resolution

        self.rawCapture = PiRGBArray(PiCamera, size=PiCamera.resolution)

        # Now connect the camera socket
        context = zmq.Context()
        self.footageSocket = context.socket(zmq.PUB)
        self.footageSocket.connect('tcp:{}:5555'.format(addr))
        self.distance = distance

        # Start stream
        self.stream()

    def stream(self):
        '''Send live stream'''
        
        #font = cv2.FONT_HERSHEY_SIMPLEX
        for frame in camera.capture_continuous(rawCapture,
                                               format = "bgr",
                                               use_video_port=True):
            image = frame.array

            # draw cross on image
            cv2.line(image,(300,240),(340,240),(128,255,128),1)
            cv2.line(image,(320,220),(320,260),(128,255,128),1)

            if opencv_mode == 1:
                pass: #TODO: impliment open cv modes
                

            if self.distance < 8:
                cv2.putText(image,'%s m'%str(round(self.distance,2)),
                            (40,40), font, 0.5,(255,255,255),
                            1,cv2.LINE_AA)


            # send image to client
            encoded, buffer = cv2.imencode('.jpg', image)
            jpg_as_text = base64.b64encode(buffer)
            footage_socket.send(jpg_as_text)
            rawCapture.truncate(0)


            

            
