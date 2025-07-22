import sqlite3
import os

# Caminho da pasta atual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho absoluto do banco
DB_PATH = os.path.join(BASE_DIR, "atividades.db")

def conectar():
    inicializar_banco()
    return sqlite3.connect(DB_PATH)

def inicializar_banco():
    if not os.path.exists(DB_PATH):
        print("Criando banco de dados SQLite...")
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                atividade TEXT NOT NULL
            )
        ''')
        con.commit()
        con.close()

def buscar_atividades():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, atividade FROM atividades")
    resultados = cur.fetchall()
    con.close()
    return resultados
