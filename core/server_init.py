from .server import ftp_server
from config import server_config

# class ServerThread(Thread):
#     def __init__(self,server):
#         self.__server = server
#         super().__init__(name="Thread-" + server.getName())
    
#     def run(self):
#         print (self.__server.getName() + " started!")
#         self.__server.run()

# ssh = ssh_server.SSHServer(server_config.server_ip, server_config.ssh_port)
ftp = ftp_server.FTPServer(server_config.server_ip, server_config.ftp_port)
print ("Server init successful!")

ftp.run()