import hashlib
import streamlit as st
from db import get_connection

def validar(nome, email, senha, dt_nasc):
    if nome == "" or email == "" or senha == "" or dt_nasc == "":
        return False
    return True

def registrar_usuario():
    nome = st.session_state.register_username
    email = st.session_state.register_email
    senha = st.session_state.register_password
    dt_nasc = st.session_state.register_dt_nasc

    if senha != st.session_state.password_confirmation:
        st.error("As senhas não coincidem. Por favor, tente novamente.")
        return

    if not validar(nome, email, senha, dt_nasc):
        st.error("Preencha todos os campos.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    inp = f"INSERT INTO Usuario VALUES (9, '{nome}', '{email}', now(), 10, sha('{senha}')), '{dt_nasc}'"
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
    
    inp = f"SELECT * FROM Usuario WHERE email = '{email}' AND senha = sha('{password}');"
    cursor.execute(inp)
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()

    if len(result) > 0:
        username = result[0][1]
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.current_page = "home"
        st.success("Login realizado com sucesso!")
    else:
        st.error("Usuário ou senha incorretos!")

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.current_page = "home"
