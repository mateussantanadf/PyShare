from flask import Flask, request, render_template
from db_writer import write_queue, db_writer
import threading
import socket
import os
import sys
import subprocess
import time
import requests

# IMPORTS PARA CRIAR ATALHO NO STARTUP DO WINDOWS
try:
    import winshell
    from win32com.client import Dispatch
except ImportError:
    winshell = None
    Dispatch = None

app = Flask(__name__)

# Inicia a thread de escrita ao iniciar o app
threading.Thread(target=db_writer, daemon=True).start()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form["nome"]
        atividade = request.form["atividade"]
        comando = "INSERT INTO atividades (nome, atividade) VALUES (?, ?)"
        parametros = (nome, atividade)
        write_queue.put((comando, parametros))
        return render_template("index.html", mensagem="Atividade registrada com sucesso!")
    return render_template("index.html")

@app.route("/atividades")
def ver_atividades():
    import sqlite3
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, atividade, data_hora FROM atividades ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return render_template("atividades.html", atividades=dados)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = "127.0.0.1"
    return ip

def configurar_ngrok_authtoken(token):
    subprocess.run(["ngrok", "config", "add-authtoken", token])

def iniciar_ngrok(porta=5000, tentativas=10, espera=1):
    caminho_ngrok = os.path.join(os.getcwd(), "ngrok.exe")
    if not os.path.exists(caminho_ngrok):
        print("ngrok.exe não encontrado na pasta do projeto.")
        return None

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen(
        [caminho_ngrok, "http", f"127.0.0.1:{porta}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        startupinfo=startupinfo
    )

    url = None
    for i in range(tentativas):
        time.sleep(espera)
        try:
            r = requests.get("http://localhost:4040/api/tunnels")
            url = r.json()["tunnels"][0]["public_url"]
            print(f"URL pública do ngrok: {url}")
            break
        except Exception:
            print(f"Tentativa {i+1} de {tentativas} falhou, aguardando ngrok iniciar...")
    if url is None:
        print("Falha ao obter URL pública do ngrok após várias tentativas.")
    return url

def registrar_no_startup():
    if not winshell or not Dispatch:
        print("Bibliotecas para criar atalho não instaladas. Ignorando registro no startup.")
        return

    startup_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    nome_atalho = "MeuAppAtividade.lnk"
    caminho_atalho = os.path.join(startup_path, nome_atalho)

    if not os.path.exists(caminho_atalho):
        try:
            target = sys.executable
            working_dir = os.getcwd()

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(caminho_atalho)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = working_dir
            shortcut.IconLocation = target
            shortcut.save()
            print(f"Atalho criado em {caminho_atalho}")
        except Exception as e:
            print("Erro ao registrar no startup:", e)

def criar_atalho_navegador(url, nome_atalho="Atalho - Sistema Web.url"):
    atalho_path = os.path.join(os.path.expanduser("~"), "Desktop", nome_atalho)
    # Remove atalho anterior se existir
    if os.path.exists(atalho_path):
        os.remove(atalho_path)
    with open(atalho_path, "w") as f:
        f.write(f"[InternetShortcut]\nURL={url}\n")
    print(f"Atalho criado em: {atalho_path}")

if __name__ == "__main__":
    registrar_no_startup()
    ip_local = get_local_ip()
    criar_atalho_navegador(f"http://{ip_local}:5000", "Atalho - Sistema Local.url")

    flask_thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000), daemon=True)
    flask_thread.start()

    time.sleep(3)

    configurar_ngrok_authtoken("SEU_TOKEN")  # Descomente se necessário

    url_ngrok = iniciar_ngrok(porta=5000)
    if url_ngrok and url_ngrok.startswith("http"):
        print(f"Acesse remotamente: {url_ngrok}")
        #criar_atalho_navegador(url_ngrok, "Atalho - Sistema Remoto.url")
        criar_atalho_navegador(url_ngrok.replace(":5000", ""), "Atalho - Sistema Remoto.url")
    else:
        print("ngrok não iniciou corretamente ou URL inválida.")

    flask_thread.join()
