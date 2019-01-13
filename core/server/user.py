import psycopg2
import time
import hashlib
import os

class User:
    def __init__(self,id):
        self.__id = id

    def getId(self):
        return self.__id

    def getName(self):
        query_user_name_sql = "SELECT name FROM user_info WHERE id = \'" + self.getId() + "\'"
        return read(query_user_name_sql)[0][0]

    def isInLimit(self, storage, home_dir):
        for path, dirs, files in os.walk(home_dir):
            for f in files:
                fp = os.path.join(path, f)
                storage += os.path.getsize(fp)
        
        query_storage_limit_sql = "SELECT storage_limit FROM user_info WHERE id = \'" + self.getId() + "\'"
        limit = read(query_storage_limit_sql)[0][0]
        return storage <= limit

def read(sql):
    conn=psycopg2.connect(host="localhost",dbname="ftp",user="postgres",password="admin")
    cursor=conn.cursor()

    cursor.execute(sql)

    data=cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def write(sql):
    conn=psycopg2.connect(host="localhost",dbname="ftp",user="postgres",password="admin")
    cursor=conn.cursor()

    cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()

def login(name, passcode):
    query_user_auth_info_sql = "SELECT u.id FROM user_auth_info AS a LEFT JOIN user_info AS u ON a.id=u.id WHERE u.name=\'" + name + "\' AND a.password=\'" + passcode + "\' LIMIT 1"
    authenticated = read(query_user_auth_info_sql)
    
    if authenticated:
        print (authenticated[0][0] + " login successful!")
        return authenticated[0][0]
    else: 
        print ("Login failed!")
        return None

def generateId():
    return hashlib.md5(str.encode(str(time.time()))).hexdigest()

def signup(name, passcode):
    newid = generateId()
    update_user_auth_info_sql = "INSERT INTO user_auth_info (id,password) VALUES (\'" + newid + "\',\'" + passcode + "\')"
    update_user_info_sql = "INSERT INTO user_info (id,name) VALUES (\'" + newid + "\',\'" + name + "\')"
    
    write(update_user_auth_info_sql)
    write(update_user_info_sql)

    server_home_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\db\\home"
    os.system("cd " + server_home_dir + " & mkdir " + newid)
    print ("New user signed up!\n")