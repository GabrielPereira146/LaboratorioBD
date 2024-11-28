from db import get_connection
import streamlit as st

def list_schools():
    conn = get_connection()
    cursor = conn.cursor()
    
    inp = "SELECT * FROM vw_escola;"
    cursor.execute(inp)
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return result

def show_school_class(school_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    inp = f"SELECT turmas FROM escola WHERE id_escola = {school_id};"
    cursor.execute(inp)
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return result

def show_teacher_students_class():
    conn = get_connection()
    cursor = conn.cursor()
    
    inp = """SELECT p.nome AS professor, e.nome AS estudante, s.nome AS sala 
             FROM vw_escola e 
             INNER JOIN vw_turma t ON e.id_escola = t.id_escola 
             INNER JOIN vw_professor p ON p.id_professor = t.id_professor 
             INNER JOIN vw_sala s ON s.id_sala = t.id_sala"""
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
