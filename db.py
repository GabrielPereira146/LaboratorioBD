import pymysql

def get_connection():
    timeout = 10
    return pymysql.connect(
      charset="utf8mb4",
      connect_timeout=timeout,
      cursorclass=pymysql.cursors.DictCursor,
      db="defaultdb",
      host="labbd-gabrielp1464.g.aivencloud.com",
      password="AVNS_0SzlA9PDfK5a94gL_4I",
      read_timeout=timeout,
      port=13848,
      user="avnadmin",
      write_timeout=timeout,
    )
    

