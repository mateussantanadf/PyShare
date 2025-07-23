import sqlite3
import os
import sys
from queue import Queue
from threading import Thread

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "atividades.db")

# Fila de requisições de gravação
gravar_fila = Queue()

def conectar():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def inicializar_banco():
    if not os.path.exists(DB_PATH):
        print("Criando banco de dados SQLite...")
        con = conectar()
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

def gravar_worker():
    while True:
        nome, atividade = gravar_fila.get()
        try:
            con = conectar()
            cur = con.cursor()
            cur.execute("INSERT INTO atividades (nome, atividade) VALUES (?, ?)", (nome, atividade))
            con.commit()
            con.close()
        except Exception as e:
            print("Erro ao gravar:", e)
        finally:
            gravar_fila.task_done()

# Inicia a thread da fila de gravação
Thread(target=gravar_worker, daemon=True).start()

def adicionar_atividade(nome, atividade):
    gravar_fila.put((nome, atividade))

def buscar_atividades():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, atividade FROM atividades")
    resultados = cur.fetchall()
    con.close()
    return resultados
