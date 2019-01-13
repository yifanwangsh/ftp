import socket
import os
import json
import struct
import subprocess
from . import server
from . import user

class FTPServer(server.Server):
    def __init__(self,ip_addr,port):
        super().__init__(ip_addr,port)
        self.__dir = None

    def run(self):
        while True:
            conn,client_addr = super().getSocket().accept()
 
            user_id = super().login(conn)
            if not user_id: continue
            self.setDir(super().server_home_dir + "\\" + user_id)
            print ("Client " + str(client_addr) + "connected!")

            while True:
                try:
                    cmd = conn.recv(1024).decode("utf-8")
                    cmds = cmd.split(" ")
                
                    if cmds[0] == "download":
                        self.download(conn,cmds[1])
                    elif cmds[0] == "upload":
                        self.upload(conn,cmds[1],user_id)
                    else:
                        self.execute(conn,cmd,user_id)
                except (ConnectionAbortedError,ConnectionResetError):
                    print ("Client connection is aborted!")
                    break
            inp = input("Close the server?")
            if inp=="Y":
                super().getSocket().close()
                break

    def execute(self,conn,cmd,userid):
        if "cd" in cmd and not cmd=="cd":
            result = subprocess.Popen(cmd + " & cd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.__dir)
            
            home_dir = super().server_home_dir + "\\" + userid
            absDir = result.stdout.read().decode("utf-8")[:-2]
            
            if not absDir in home_dir or absDir == home_dir:
                self.setDir(absDir)
        else:    
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.__dir)
        
        stdout = result.stdout.read()
        stderr = result.stderr.read()

        header = {
            "result_length": len(stdout) + len(stderr)
        }

        header_bytes = json.dumps(header).encode("utf-8")

        conn.send(struct.pack("i",len(header_bytes)))
        conn.send(header_bytes)

        conn.send(stdout+stderr)            

    def download(self,conn,filename):
        file_size = os.path.getsize(self.__getAbsPath(filename))
        header = {
            "file_size":file_size,
            "file_name":filename
        }
        header_bytes = json.dumps(header).encode("utf-8")
        
        conn.send(struct.pack("i",len(header_bytes)))

        conn.send(header_bytes)

        with open(self.__getAbsPath(filename), "rb") as f:
            # for line in f:
            #     conn.send(line)
            sent_bytes = 0
            while sent_bytes + 1024 < file_size:
                conn.send(f.read(1024))
                sent_bytes += 1024

                print ("Progress: {0:5.2f} %".format(sent_bytes/file_size*100),end="\r")
            
            conn.send(f.read(file_size - sent_bytes))
            print ("Progress: 100.00 %")
    
    def upload(self,conn,filename,userid):
        header_pack = conn.recv(4)
        header_length = struct.unpack("i",header_pack)[0]

        header = json.loads(conn.recv(header_length).decode("utf-8"))

        file_size = header["file_size"]

        home_dir = super().server_home_dir + "\\" + userid
        if not user.User(userid).isInLimit(file_size, home_dir):
            conn.send(str(socket.errno.EPERM).encode("utf-8"))
            return
        else:
            conn.send("0".encode("utf-8"))
            
        with open(self.__getAbsPath(filename), "wb") as f:
            received_size = 0
            while received_size + 1024 < file_size:
                f.write(conn.recv(1024))
                received_size+=1024
                
                print ("Progress: {0:5.2f} %".format(received_size/file_size*100),end="\r")
            
            f.write(conn.recv(file_size - received_size))
            print ("Progress: 100.00 %")
        
    def __getAbsPath(self, filename):
        return self.__dir + "\\" + filename

    def setDir(self, dir):
        self.__dir = dir