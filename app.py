import streamlit as st
import pandas as pd

from auth import registrar_usuario, login_user, logout_user
from pages import list_schools, show_teachers_students, school_orderby_students, get_school_stats, show_school_class, favoritar, list_favorites, desfavoritar
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
    if st.button("Professores e Alunos de Escola"):
        st.session_state.current_page = "ProfEAlunos"
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

        

# Se a página atual for "escolas"
elif st.session_state.current_page == "escolas":
    # Título da página
    st.title("Escolas da Cidade")

    # Opção para ordenar
    order_by = st.selectbox("Ordenar por", ["Alfabetica", "Numero de Alunos"])
    if order_by == "Alfabetica":
        schools = list_schools()
    elif order_by == "Numero de Alunos":
        schools = school_orderby_students()
    else:
        schools = list_schools()

    # Linha divisória
    st.markdown("---")

    if not schools:
        st.write("Nenhuma escola encontrada.")
    else:
        # Crie um DataFrame com os resultados
        df = pd.DataFrame(schools, columns=["CO_ENTIDADE", "NO_ENTIDADE", "num_alunos"])  

        # Adiciona a coluna de favoritos se o usuário estiver logado
        if st.session_state.get("logged_in", False):
           
            favoritos = [item['ID_ESC'] for item in list_favorites()]
            # Adicionar uma coluna de botões (interativa)
            def render_favorito_button(no_entidade):
                
                if no_entidade in favoritos:
                    estrela = "⭐"
                else:
                    estrela = "☆"

                if st.button(estrela, key=f"fav_{no_entidade}"):
                    if no_entidade in favoritos:
                        desfavoritar(no_entidade)
                    else:
                        favoritar(no_entidade)

                return estrela

            # Criar uma tabela personalizada
            for _, row in df.iterrows():
                col1, col2, col3, col4 = st.columns([2, 6, 2, 2])
                with col1:
                    st.write(row["CO_ENTIDADE"])  # Código da escola
                with col2:
                    st.write(row["NO_ENTIDADE"])  # Nome da escola
                with col3:
                    st.write(row["num_alunos"])  # Número de alunos
                with col4:
                    render_favorito_button(row["CO_ENTIDADE"])  # Botão de favoritos

        else:
            # Exiba a tabela sem a coluna de favoritos
            st.table(df)

elif st.session_state.current_page == "ProfEAlunos":
        # Busca professores e alunos de uma escola
    try:
        st.title("Professores e Alunos")
        st.text_input("Codigo Escola", key="escola")
        if st.button("Buscar"):
            st.write(f"Professores e alunos: ")
            teachers_students = show_teachers_students(st.session_state.escola)
            # Crie um DataFrame com os resultados
            df = pd.DataFrame(teachers_students)
            # Exiba o DataFrame como tabela
            st.table(df)
    except:
        st.write(f" Codigo da escola nao encontrado ")


elif st.session_state.current_page == "Turmas":
    
    # Página de turmas
    st.title("Turmas")
    st.text_input("Codigo Escola", key="escola")
    if st.button("Buscar"):
        st.write(f"Turmas: ")
        turmas = show_school_class(st.session_state.escola)
        df = pd.DataFrame(turmas)
        # Exiba o DataFrame como tabela
        st.table(df)

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
                              st.session_state.register_password, st.session_state.register_dt_nasc)

elif st.session_state.current_page == "user_profile":

    # Página do perfil do usuário
    st.title("Perfil do Usuário")
    if st.session_state.logged_in:
        st.write(f"Bem-vindo ao seu perfil, {st.session_state.username}!")
        st.write("Escolas favoritas:")
        favorites = list_favorites()
        df = pd.DataFrame(favorites)
        # Exiba o DataFrame como tabela
        st.table(df)
  
    else:
        st.warning("Você não está logado. Por favor, faça login.")


# Mostrar total de alunos, professores e turmas por escola

elif st.session_state.current_page == "Estatísticas":
    # Página de estatísticas
    st.title("Estatísticas por Escola")
    results = get_school_stats()
    df = pd.DataFrame(results)
        # Exiba o DataFrame como tabela
    st.table(df)


