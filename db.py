import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost', 
        user='root', 
        password='root',
        port=3306, 
        db='atividade4_lab', 
        auth_plugin='mysql_native_password'
    )
