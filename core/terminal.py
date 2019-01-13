from .client import ftp_client
from config import server_config

while True:
    client=ftp_client.FTPClient(server_config.server_ip, server_config.ftp_port)
    print ('''Welcome to FTP service.
    1. Log in
    2. Sign up
    q. Quit
    How can I help you?''')
    c=input("==>").strip()

    if c=="q":break

    elif c=="1":
        print ("Please enter your name: ")
        name = input("==>").strip()
        print ("Please enter your password: ")
        passcode = input("==>").strip()

        
        return_code = client.start(name,passcode)
        if return_code:
            print ('''
    To download a file, command is download + [file name] + [target directory]
    To upload a file, command is upload + [file name] + [file parent directory]
    To quit, command is exit
            ''')
            client.run()
        else:
            print ("Login Failed!")

    # elif c=="2":
    #     print ("Please enter your name")
    #     name = input("==>").strip()
    #     print ("Please enter your password")
    #     passcode = input("==>").strip()

    #     user.signup(name,passcode)