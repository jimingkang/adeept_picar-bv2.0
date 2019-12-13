#!/usr/bin/python
import socket
from threading import Thread

#TODO: include some basic safety protocols to ensure car doesn't crash
host = '127.0.0.1'
controlport = 5000
footageport = 5555
backlog = 5
size = 1024

class ControlThread(Thread):
    def __init__(self, car=None):
        Thread.__init__(self)

        self.car = car

        host=""
        self.size = 1024
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host,controlport))
        
        self.start()

    def run(self):
        while True:
            self.sock.listen(5) 
            client,address = self.sock.accept()
            print("New client")
            while True:
                data = client.recv(self.size).rstrip().decode()
                if not data:
                    continue
                if data == "disconnect":
                    client.close()
                    break
                if data == "exit":
                    client.close()
                    return
                try:
                    print(data)
                except:
                    print("Error executing: {}".format(data))

class FootageThread(Thread):

    def __init__(self, camera, addr):
        Thread.__init__(self)

    def run(self):
        pass

if __name__=="__main__":
    
    control = ControlThread()
    
    #with car as PiCar():
    # Start control thread
    # Start footage thread
        

    pass
