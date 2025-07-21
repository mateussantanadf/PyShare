import fdb
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'atividades.fdb')

def conectar():
    return fdb.connect(
        dsn=DB_PATH,
        user='sysdba',
        password='admin123',
        charset='UTF8'
    )