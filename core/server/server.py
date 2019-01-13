import socket
import struct
import json
import os
import psycopg2

from . import user

class Server:
    server_home_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "\\db\\home"
    def __init__(self, ip_addr,port):
        self.__ip_addr=ip_addr
        self.__socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__socket.bind((self.__ip_addr,port))
        self.__socket.listen(5)
        
    def getSocket(self):
        return self.__socket

    def login(self,conn):
        info_length = struct.unpack("i",conn.recv(4))[0]
        login_info = json.loads(conn.recv(info_length).decode("utf-8"))
        userid = user.login(login_info["username"],login_info["password"])
        if userid:
            conn.send("1".encode("utf-8"))
        else:
            conn.send("0".encode("utf-8"))
        return userid