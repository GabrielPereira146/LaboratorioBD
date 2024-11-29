from db import get_connection
import streamlit as st


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


def school_orderby_students():
    conn = get_connection()
    cursor = conn.cursor()
    
    inp = """SELECT e.CO_ENTIDADE, COUNT(m.CO_PESSOA_FISICA) AS num_alunos
             FROM matricula m JOIN escola e ON m.CO_ENTIDADE = e.CO_ENTIDADE
             GROUP BY e.CO_ENTIDADE
             ORDER BY num_alunos DESC;"""
    cursor.execute(inp)
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return result

def get_school_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT
            DISTINCT e.CO_ENTIDADE,
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