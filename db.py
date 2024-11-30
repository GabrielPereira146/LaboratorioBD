import pymysql
import streamlit as st

# Acessa as variáveis do Streamlit Secrets
DB_HOST = st.secrets["database"]["DB_HOST"]
DB_PORT = st.secrets["database"]["DB_PORT"]
DB_USER = st.secrets["database"]["DB_USER"]
DB_PASSWORD = st.secrets["database"]["DB_PASSWORD"]
DB_NAME = st.secrets["database"]["DB_NAME"]
DB_CHARSET = st.secrets["database"]["DB_CHARSET"]
DB_TIMEOUT = st.secrets["database"]["DB_TIMEOUT"]

# Função para conectar ao banco de dados
def get_connection():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset=DB_CHARSET,
            connect_timeout=DB_TIMEOUT
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
