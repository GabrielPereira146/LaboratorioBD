import streamlit as st

# Configuração inicial
st.set_page_config(
    page_title="Censo Escolar",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Controle de navegação e estado
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Funções para login/logout
def login_user(username, password):
    if username == "admin" and password == "1234":
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

# Barra lateral para navegação
with st.sidebar:
    # Logo no topo
    st.image("https://via.placeholder.com/150x50.png?text=Logo", use_container_width=True)
    st.markdown("---")

    # Customizar a barra lateral com CSS
    st.markdown("""
        <style>
            .css-1d391kg {  # Botão da barra lateral
                border: none;
                background-color: #1E90FF;  /* Cor de fundo */
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            .css-1d391kg:hover {
                background-color: #4682B4;  /* Cor de fundo ao passar o mouse */
            }
        </style>
        """, unsafe_allow_html=True)

    # Botões de navegação
    if st.button("Home"):
        st.session_state.current_page = "home"

    if st.session_state.logged_in:
        if st.button("Usuário"):
            st.session_state.current_page = "user_profile"
        if st.button("Logout"):
            logout_user()
    else:
        if st.button("Login/Registrar"):
            st.session_state.current_page = "login"

# Controle da página atual
def hide_page_title():
    """Função para ocultar o título padrão."""
    st.markdown(
        """
        <style>
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

hide_page_title()

if st.session_state.current_page == "home":
    # Página inicial
    st.title("Bem-vindo ao Censo Escolar!")
    st.write("Explore e visualize os dados escolares aqui.")
elif st.session_state.current_page == "login":
    # Página de login/registro
    st.title("Login ou Registro")
    st.subheader("Faça login ou registre-se para acessar mais funcionalidades.")

    # Formulário de login
    st.text_input("Usuário", key="login_username")
    st.text_input("Senha", type="password", key="login_password")
    if st.button("Entrar"):
        login_user(st.session_state.login_username, st.session_state.login_password)

    st.markdown("---")

    # Formulário de registro
    st.text_input("Novo Usuário", key="register_username")
    st.text_input("Nova Senha", type="password", key="register_password")
    if st.button("Registrar"):
        # Simular registro (substituir pela lógica do banco)
        st.success(f"Usuário {st.session_state.register_username} registrado com sucesso!")

elif st.session_state.current_page == "user_profile":
    # Página do perfil do usuário
    st.title("Perfil do Usuário")
    if st.session_state.logged_in:
        st.write(f"Bem-vindo ao seu perfil, {st.session_state.username}!")
    else:
        st.warning("Você não está logado. Por favor, faça login.")
