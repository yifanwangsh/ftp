import socket
import json
import struct

class Client:
    def __init__(self,server_ip,port):
        self.__socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__socket.connect((server_ip,port))
        
    def start(self,name,passcode):
        login_info = {
            "username":name,
            "password":passcode
        }

        login_bytes = json.dumps(login_info).encode("utf-8")
        self.__socket.send(struct.pack("i",len(login_bytes)))
        self.__socket.send(login_bytes)

        return_code = self.__socket.recv(1).decode("utf-8")
        return return_code == "1"

    def getSocket(self):
        return self.__socket