import streamlit as st
from streamlit_option_menu import option_menu

from auth import registrar_usuario, login_user, logout_user
from pages import list_schools, show_school_class, show_teacher_students_class, school_orderby_students



# Configuração inicial
st.set_page_config(
    page_title="Censo Escolar",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Controle de navegação e estado
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.current_page = "home"



# Barra lateral para navegação
with st.sidebar:
    # Logo no topo
    st.image("LogoLabBD.png", use_container_width=True)
    st.markdown("---")

    # Botões de navegação
    btn_home = st.button("Home")
    if btn_home:
        st.session_state.current_page = "home"
    if st.button("Escolas da Cidade"):
        st.session_state.current_page = "escolas"

    if st.button("Total de Alunos, Professores e Turmas"):
        st.session_state.current_page = "Counts"
    if st.button("Ordenados por numero de alunos"):
        st.session_state.current_page = "OrderByAlunos"
    if st.button("Turmas"):
        st.session_state.current_page = "Turmas"
    if st.session_state.logged_in:
        if st.button("Usuário"):
            st.session_state.current_page = "user_profile"
        if st.button("Logout"):
            logout_user()
        
    else:
        if st.button("Login/Registrar"):
            st.session_state.current_page = "login"

# Controle da página atual

if st.session_state.current_page == "home":
    # Página inicial
    st.title("Bem-vindo ao Censo Escolar!")
    st.markdown("Esta aplicação website tem como função a consulta de escolas participantes do Censo Escolar de Rio Claro.")
    st.markdown("Experimente realizar buscas por escolas, turmas ou alunos que desejar através dos botões e tabelas abaixo!")
    

elif st.session_state.current_page == "escolas":
    # Página de escolas
    st.title("Escolas da Cidade")
    for school in list_schools():
        st.write(f"{school[1]} - {school[2]}")

elif st.session_state.current_page == "Counts":
    # Página de alunos, professores e turmas
    st.title("Total de Alunos, Professores e Turmas")

elif st.session_state.current_page == "OrderByAlunos":
    # Ordenados por alunos
    st.title("Ordenados por numero de alunos")
    for school in school_orderby_students():
        st.write(f"{school[0]} - {school[1]}")


elif st.session_state.current_page == "Turmas":
    # Página de turmas
    st.title("Turmas")

elif st.session_state.current_page == "login":
    # Página de login/registro
    st.title("Login ou Registro")
    st.subheader("Faça login ou registre-se para acessar mais funcionalidades.")


    # Formulário de login
    st.text_input("Email", key="email")
    st.text_input("Senha", type="password", key="login_password")
    if st.button("Entrar"):
        login_user(st.session_state.email, st.session_state.login_password)

    st.markdown("---")

    # Formulário de registro
    st.text_input("Username", key="register_username")
    st.text_input("Email", key="register_email")
    st.text_input("Data de Nascimento", key="register_dt_nasc")
    st.text_input("Senha", type="password", key="register_password")
    st.text_input("Confirme a Senha", type="password", key="password_confirmation")
    
    if st.button("Registrar"):
        registrar_usuario(st.session_state.register_username, st.session_state.register_email, st.session_state.register_password, st.session_state.register_dt_nasc)

elif st.session_state.current_page == "user_profile":

    # Página do perfil do usuário
    st.title("Perfil do Usuário")
    if st.session_state.logged_in:
        st.write(f"Bem-vindo ao seu perfil, {st.session_state.username}!")
    else:
        st.warning("Você não está logado. Por favor, faça login.")
