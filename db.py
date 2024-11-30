import os
import pymysql

def get_connection():
    timeout = 10
    return pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        read_timeout=timeout,
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        write_timeout=timeout,
    )
