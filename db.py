import os
import pymysql
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def get_connection():
    return pymysql.connect(
        charset=os.getenv("DB_CHARSET", "utf8mb4"),
        connect_timeout=int(os.getenv("DB_TIMEOUT", 10)),
        cursorclass=pymysql.cursors.DictCursor,
        db=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        read_timeout=int(os.getenv("DB_TIMEOUT", 10)),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        write_timeout=int(os.getenv("DB_TIMEOUT", 10)),
    )
