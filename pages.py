import pandas as pd
from db import get_connection
import streamlit as st

#Selecionar uma escola e listar todas as turmas
@st.cache_data(ttl=600)
def show_school_class(school_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    inp = f"""SELECT t.ID_TURMA
            FROM turma t
            JOIN escola e ON t.CO_ENTIDADE = e.CO_ENTIDADE
            WHERE e.CO_ENTIDADE = {school_id};"""
    cursor.execute(inp)
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return result

#Ordena as escolas por número de alunos
@st.cache_data(ttl=600)
def school_orderby_students():
    conn = get_connection()
    cursor = conn.cursor()
    
    inp = """SELECT e.CO_ENTIDADE, e.NO_ENTIDADE, COUNT(m.CO_PESSOA_FISICA) AS num_alunos
             FROM matricula m JOIN escola e ON m.CO_ENTIDADE = e.CO_ENTIDADE
             GROUP BY e.CO_ENTIDADE
             ORDER BY num_alunos DESC;"""
    cursor.execute(inp)
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return result

#Ordena as escolas por ordem alfabética
@st.cache_data(ttl=600)
def list_schools():
    conn = get_connection()
    cursor = conn.cursor()
    
    inp = """SELECT e.CO_ENTIDADE, e.NO_ENTIDADE, COUNT(m.CO_PESSOA_FISICA) AS num_alunos
             FROM matricula m JOIN escola e ON m.CO_ENTIDADE = e.CO_ENTIDADE
             GROUP BY e.CO_ENTIDADE
             ORDER BY e.NO_ENTIDADE;"""
    cursor.execute(inp)
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return result

#Listar as escolas da cidade
def get_school_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT
            DISTINCT e.NO_ENTIDADE,
            COALESCE(x.total_alunos, 0) AS total_alunos,
            COALESCE(y.total_professores, 0) AS total_professores,
            COALESCE(z.total_turmas, 0) AS total_turmas
        FROM escola e
        LEFT JOIN (
            SELECT m.CO_ENTIDADE AS entidade,
                COUNT(DISTINCT m.CO_PESSOA_FISICA) AS total_alunos
            FROM matricula m
            GROUP BY m.CO_ENTIDADE
        ) AS x ON x.entidade = e.CO_ENTIDADE
        LEFT JOIN (
            SELECT d.CO_ENTIDADE AS entidade,
                COUNT(DISTINCT d.CO_PESSOA_FISICA) AS total_professores
            FROM docente d
            GROUP BY d.CO_ENTIDADE
        ) AS y ON y.entidade = e.CO_ENTIDADE
        LEFT JOIN (
            SELECT t.CO_ENTIDADE AS entidade,
                COUNT(DISTINCT t.ID_TURMA) AS total_turmas
            FROM turma t
            GROUP BY t.CO_ENTIDADE
        ) AS z ON z.entidade = e.CO_ENTIDADE
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return results

#Selecionar os professores e alunos de cada escola (drill-down)
@st.cache_data(ttl=600)
def show_teachers_students(school_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # print("[Profs] - school_id")
    # print(school_id)

    #colocar o parâmetro e substituir no lugar de e.CO_ENTIDADE
    inp = f"""
  SELECT 
    'Professor' AS Tipo,
    d.CO_PESSOA_FISICA AS Cod_Pessoa
FROM docente d
WHERE d.CO_ENTIDADE = {school_id}

UNION ALL

SELECT 
    'Aluno' AS Tipo,
    m.CO_PESSOA_FISICA AS Cod_Pessoa
FROM matricula m
WHERE m.CO_ENTIDADE = {school_id}

        """
    cursor.execute(inp)
    result = cursor.fetchall()

    # print("[Profs] - result")
    # print(result)
    
    cursor.close()
    conn.close()
    return result


@st.cache_data(ttl=600)
def favoritar(id_escola):
    conn = get_connection()
    cursor = conn.cursor()
    
    inp = f"INSERT INTO bookmark(ID_USU, ID_ESC) VALUES ({st.session_state.user_id}, {id_escola});"
    cursor.execute(inp)
    conn.commit()
    
    cursor.close()
    conn.close()

    return

def desfavoritar(id_escola):
    conn = get_connection()
    cursor = conn.cursor()
    
    inp = f"DELETE FROM bookmark WHERE ID_USU = {st.session_state.user_id} AND ID_ESC = {id_escola};"
    cursor.execute(inp)
    conn.commit()
    
    cursor.close()
    conn.close()

    return

def list_favorites():
    conn = get_connection()
    cursor = conn.cursor()
    
    inp = f"""
        SELECT b.ID_ESC, e.NO_ENTIDADE 
        FROM bookmark b
        JOIN escola e ON b.ID_ESC = e.CO_ENTIDADE
        WHERE b.ID_USU = {st.session_state.user_id}
    ;"""
    cursor.execute(inp)
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return result


def export_to_csv(tabela):
    conn = get_connection()
    cursor = conn.cursor()
    inp = f"SELECT * FROM {tabela};"
    cursor.execute(inp)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(result)

@st.cache_data(ttl=600)
def mapa():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT CO_ENTIDADE, NO_ENTIDADE, LAT, LON FROM escolas_geoloc;"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(result, columns=["CO_ENTIDADE", "NO_ENTIDADE", "LAT", "LON"])
