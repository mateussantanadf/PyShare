# db_writer.py
import threading
import sqlite3
from queue import Queue

write_queue = Queue()

def db_writer():
    while True:
        comando, parametros = write_queue.get()
        try:
            conn = sqlite3.connect("dados.db")
            cursor = conn.cursor()
            cursor.execute(comando, parametros)
            conn.commit()
            conn.close()
        except Exception as e:
            print("Erro ao gravar no banco:", e)
        finally:
            write_queue.task_done()
