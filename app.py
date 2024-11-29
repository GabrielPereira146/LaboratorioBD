import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

from auth import registrar_usuario, login_user, logout_user
from pages import school_orderby_students, get_school_stats, show_school_class
from pathlib import Path

def read_tables_for_export():
    # Obtenha o diretório do script atual
    current_directory = Path(__file__).resolve().parent
    sql_files_paths = [] #vetor de caminhos de diretório dos arquivos a serem exportados em csv
    sql_queries = [] #vetor dos conteudos dos arquivos

    # Caminho absoluto para os arquivos .sql na mesma pasta
    sql_files_paths[0] = current_directory / 'arquivo.sql' #mudar os nomes dos arquivos pra cada botão
    sql_files_paths[1] = current_directory / 'arquivo.sql' #mudar os nomes dos arquivos pra cada botão
    sql_files_paths[2] = current_directory / 'arquivo.sql' #mudar os nomes dos arquivos pra cada botão
    sql_files_paths[3] = current_directory / 'arquivo.sql' #mudar os nomes dos arquivos pra cada botão
    sql_files_paths[4] = current_directory / 'arquivo.sql' #mudar os nomes dos arquivos pra cada botão
    sql_files_paths[5] = current_directory / 'arquivo.sql' #mudar os nomes dos arquivos pra cada botão

    # Ler o conteúdo dos arquivos SQL
    for i in sql_files_paths: 
        with open(sql_files_paths[i], 'r') as f:
            sql_queries[i] = f.read()
        f.close(sql_files_paths[i])
        
# def export_csv():
#     downloads_path = str(Path.home() / "Downloads")
    # df = []
    # df[0] = pd.read_sql(sql_files_paths[0])
    # df[1] = pd.read_sql(sql_files_paths[1])
    # df[2] = pd.read_sql(sql_files_paths[2])
    # df[3] = pd.read_sql(sql_files_paths[3])
    # df[4] = pd.read_sql(sql_files_paths[4])
    # df[5] = pd.read_sql(sql_files_paths[5])
    # @st.cache_data
    # def convert_df(df):
    #   return df.to_csv(index=False).encode('utf-8')


# csv = convert_df(df) arrumar pra cada botão

# st.download_button(
#    "Press to Download",
#    csv,
#    "file.csv",
#    "text/csv",
#    key='download-csv'
# )



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
    st.image("LogoLabBDvec.svg", use_container_width=True)
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
    if st.button("Turmas de Escola"):
        st.session_state.current_page = "Turmas"
    if st.button("Estatísticas"):
        st.session_state.current_page = "Estatísticas"
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
    st.markdown('<style>.stButton > button#home { color: #f30f5bff; font-weight: bold; }</style>', unsafe_allow_html=True)
    # Página inicial
    # Logo ou imagem no topo
    st.image("LogoLabBDvec.svg", use_container_width=True)

    # Título e descrição principal
    st.title("Laboratório de Banco de Dados")
    st.subheader("Projeto baseado no Censo Escolar")
    st.markdown("""
        Este site foi desenvolvido como parte da disciplina **Laboratório de Banco de Dados**, com o objetivo de explorar e aplicar 
        técnicas de modelagem e manipulação de dados utilizando o banco de dados do **Censo Escolar**. 
        Aqui, você pode visualizar informações sobre escolas, alunos, professores e muito mais.
    """)

    # Linha divisória
    st.markdown("---")

    # Seção sobre o projeto
    st.header("📊 Sobre o Projeto")
    st.markdown("""
    - **Objetivo**: Criar um sistema para análise e visualização de dados do Censo Escolar.
    - **Disciplina**: Laboratório de Banco de Dados.
    - **Técnicas utilizadas**: Modelagem de banco de dados, consultas SQL e integração com interfaces gráficas.
    """)

    # Seção dos integrantes
    st.header("👥 Integrantes do Grupo")
    integrantes = ["Amanda Reis", "Diogo", "Gil", "Gabriel Pereira", "Lucas Goes"]
    for integrante in integrantes:
        st.markdown(f"- {integrante}")

        

elif st.session_state.current_page == "escolas":
    # Página de escolas
    st.title("Escolas da Cidade")

    order_by = st.selectbox("Ordenar por", ["Alfabetica", "Numero de Alunos"])
    if order_by == "Alfabetica":
        print("Alfabetica")
        # schools = list_schools()
    elif order_by == "Numero de Alunos":
        print("Numero de Alunos")
        # schools = school_orderby_students()
    else:
        print("Default")
        #schools = list_schools()
    # Linha divisória
    st.markdown("---")
    # for school in list_schools():
    #     st.write(f"{school[1]} - {school[2]} {':' if not st.session_state.logged_in else '❤️' if school[0] in st.session_state.favorites else '☆' if st.button(f' favorite {school[0]}') else ''}")

elif st.session_state.current_page == "OrderByAlunos":
        # Ordenados por alunos
        st.title("Ordenados por numero de alunos")
        for school in school_orderby_students():
            st.write(f"{school[0]} - {school[1]}")


elif st.session_state.current_page == "Turmas":
    # Página de turmas
    st.title("Turmas")
    st.text_input("Codigo Escola", key="escola")
    for classroom in show_school_class(st.session_state.escola):
        st.write(f"{classroom[0]} - {classroom[1]}")

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
    is_admin = st.checkbox("Registrar como administrador", key="register_is_admin")
    st.text_input("Username", key="register_username")
    st.text_input("Email", key="register_email")
    st.text_input("Data de Nascimento", key="register_dt_nasc")
    st.text_input("Senha", type="password", key="register_password")
    st.text_input("Confirme a Senha", type="password", key="password_confirmation")
    
    if is_admin:
        st.text_input("Senha de Validação", type="password", key="admin_validation_password")
    
    if st.button("Registrar"):
        if is_admin and st.session_state.admin_validation_password != "admin123":
            st.error("Senha de validação inválida para administrador.")
        else:
            registrar_usuario(st.session_state.register_username, st.session_state.register_email, 
                              st.session_state.register_password, st.session_state.register_dt_nasc, is_admin)

elif st.session_state.current_page == "user_profile":

    # Página do perfil do usuário
    st.title("Perfil do Usuário")
    if st.session_state.logged_in:
        st.write(f"Bem-vindo ao seu perfil, {st.session_state.username}!")
    else:
        st.warning("Você não está logado. Por favor, faça login.")


# Mostrar total de alunos, professores e turmas por escola

elif st.session_state.current_page == "Estatísticas":
    # Página de estatísticas
    st.title("Estatísticas por Escola")
    results = get_school_stats()
    for row in results:
        st.write(f"Escola: {row[0]}")
        st.write(f"Total de Alunos: {row[1]}")
        st.write(f"Total de Professores: {row[2]}")
        st.write(f"Total de Turmas: {row[3]}")
