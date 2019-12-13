import socket

class ClientConnection:

    '''Connection to client on computer'''

    def __init__(self, host='',tcpPort=10223,tcpBufferSize = 1024):
        '''Set up connection to client'''

        self.tcpBufferSize = 1024

        try: # Check our ip address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("1.1.1.1",80))
            ipaddr_check = s.getsockname()[0]
            print(ipaddr_check)
            s.close()
        except:
            print("No WiFi: Start hotspot")
            #TODO: impliment wifi hotspot

        tcpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServerSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #???
        tcpServerSocket.bind( (host,tcpPort) )
        tcpServerSocket.listen(5) #??? magic number
        # waiting for client
        print("Waiting for connection")
        
        self.tcpClientSocket, self.addr = tcpServerSocket.accept()
        print("...connected from : {}".format(addr))

        #tcpClientSocket.send('initial information')

    def read_command(self):
        data = ''
        data = self.tcpCliSock.recv(self.tcpBufferSize).decode()
        return data

if __name__=="__main__":
    pass
