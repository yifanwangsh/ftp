import psycopg2

conn=psycopg2.connect(host="localhost",dbname="ftp",user="postgres",password="admin")
cursor=conn.cursor()

create_user_auth_info_sql="CREATE TABLE user_auth_info (id VARCHAR NOT NULL PRIMARY KEY, password VARCHAR NOT NULL)"
create_user_info_sql="CREATE TABLE user_info (id VARCHAR NOT NULL PRIMARY KEY, name VARCHAR NOT NULL, storage_limit integer NOT NULL DEFAULT 1048576)"

cursor.execute(create_user_auth_info_sql)
cursor.execute(create_user_info_sql)

conn.commit()
cursor.close()
conn.close()