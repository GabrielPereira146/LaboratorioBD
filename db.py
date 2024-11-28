import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost', 
        user='bruno', 
        password='1234',
        port=3306, 
        db='labbd', 
        auth_plugin='mysql_native_password'
    )
