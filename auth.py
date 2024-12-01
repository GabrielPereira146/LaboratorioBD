import hashlib
import streamlit as st
from db import get_connection
from datetime import datetime

def validar(nome, email, senha, dt_nasc):
    if nome == "" or email == "" or senha == "" or dt_nasc == "":
        return False
    return True

def registrar_usuario(nome, email, senha, dt_nasc):
    nome = st.session_state.register_username
    email = st.session_state.register_email
    senha = st.session_state.register_password
    dt_nasc = st.session_state.register_dt_nasc
    admin = False
    # admin = st.session_state.register_admin

    data_obj = datetime.strptime(dt_nasc, "%d/%m/%Y")  # Converte a string para um objeto datetime
    data_formatada = data_obj.strftime("%Y-%m-%d")


    if senha != st.session_state.password_confirmation:
        st.error("As senhas não coincidem. Por favor, tente novamente.")
        return

    if not validar(nome, email, senha, dt_nasc):
        st.error("Preencha todos os campos.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    if admin:
        role = "admin"
    else:
        role = "user"
    
    inp = f"INSERT INTO usuario(NOME, EMAIL, IDADE, DATA_CADASTRO, SENHA, DATA_NASCIMENTO) VALUES ('{nome}', '{email}', 21, now(), sha('{senha}'), '{data_formatada}')"
    try:
        cursor.execute(inp)
        conn.commit()
        st.success(f"Usuário {nome} registrado com sucesso!")
    except Exception as e:
        conn.rollback()
        st.error(f"Erro ao cadastrar o usuário: {e}")
    finally:
        cursor.close()
        conn.close()

def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    
    inp = f"SELECT * FROM usuario WHERE email = '{email}' AND senha = sha('{password}');"
    cursor.execute(inp)
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()

    if result:
        print(result)
        username = result[0]['NOME']
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_id = result[0]['ID']
        st.session_state.current_page = "home"
        st.success("Login realizado com sucesso!")
    else:
        st.error("Usuário ou senha incorretos!")

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.current_page = "home"
