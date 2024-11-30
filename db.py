import toml
import pymysql

# Carrega as configurações do arquivo config.toml
config = toml.load("config.toml")

def get_connection():
    db_config = config["database"]
    
    # Conectando ao banco de dados usando as variáveis de configuração
    return pymysql.connect(
        host=db_config.get("DB_HOST"),
        port=db_config.get("DB_PORT"),
        user=db_config.get("DB_USER"),
        password=db_config.get("DB_PASSWORD"),
        database=db_config.get("DB_NAME"),
        charset=db_config.get("DB_CHARSET"),
        connect_timeout=db_config.get("DB_TIMEOUT"),
        read_timeout=db_config.get("DB_TIMEOUT"),
        write_timeout=db_config.get("DB_TIMEOUT"),
        cursorclass=pymysql.cursors.DictCursor,
    )
