import socket
from . import client
import struct
import json
import os
import time

class FTPClient(client.Client):
    def __init__(self,server_ip,port):
        super().__init__(server_ip,port)
    
    def run(self):
        while True:
            cmd = input("==>").strip()
            if cmd == "exit":
                super().getSocket().close()
                break

            super().getSocket().send(cmd.encode("utf-8"))

            cmds = cmd.split(" ")
            if cmds[0] == "download":
                self.download(cmds[1], cmds[2])
            elif cmds[0] == "upload":
                self.upload(cmds[1], cmds[2])
            else:
                self.execute()

    def execute(self):
        header_pack = super().getSocket().recv(4)
        header_length = struct.unpack("i",header_pack)[0]

        header = json.loads(super().getSocket().recv(header_length).decode("utf-8"))

        result = super().getSocket().recv(header["result_length"]).decode("utf-8")

        if result:
            print (result)

    def download(self,filename,file_dir):
        header_pack = super().getSocket().recv(4)
        header_size = struct.unpack("i",header_pack)[0]

        header_json = super().getSocket().recv(header_size).decode("utf-8")

        header = json.loads(header_json)

        with open(file_dir + "\\" + filename, "wb") as f:
            file_size = header["file_size"]
            received_size = 0
            while received_size+1024<file_size:
                f.write(super().getSocket().recv(1024))
                received_size+=1024

                print ("Progress: {0:5.2f} %".format(received_size/file_size*100),end="\r")
            f.write(super().getSocket().recv(file_size-received_size))
            print ("Progress: 100.00 %")

    def upload(self,filename,file_dir):
        file_size=os.path.getsize(file_dir + "\\" + filename)
        header={
            "file_size":file_size,
            "file_name":filename
        }
        
        header_bytes=json.dumps(header).encode("utf-8")

        super().getSocket().send(struct.pack("i",len(header_bytes)))

        super().getSocket().send(header_bytes)

        return_code = super().getSocket().recv(2).decode("utf-8")
        if return_code == "1":
            print ("Your space is used up")
            return

        with open(file_dir + "\\" + filename, "rb") as f:
            sent_bytes = 0
            while sent_bytes + 1024 < file_size:
                super().getSocket().send(f.read(1024))
                sent_bytes += 1024

                print ("Progress: {0:5.2f} %".format(sent_bytes/file_size*100),end="\r")
            
            super().getSocket().send(f.read(file_size - sent_bytes))
            print ("Progress: 100.00 %")
                
        print ("File uploading successful!")