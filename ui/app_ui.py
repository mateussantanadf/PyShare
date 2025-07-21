import tkinter as tk
from tkinter import messagebox
from database.db_config import conectar

def salvar_atividades(entry_nome, entry_atividade):
    nome = entry_nome.get()
    atividade = entry_atividade.get()

    if not nome or not atividade:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO atividades (nome, atividade) VALUES (?, ?)", (nome, atividade))
    con.commit()
    con.close()

    entry_nome.delete(0, tk.END)
    entry_atividade.delete(0, tk.END)
    messagebox.showinfo("Sucesso", "Atividade registrada com sucesso.")

def iniciar_ui():
    app = tk.Tk()
    app.title("Cadastro de Atividades")

    tk.Label(app, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
    entry_nome = tk.Entry(app, width=30)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(app, text="Atividade:").grid(row=1, column=0, padx=10, pady=5)
    entry_atividade = tk.Entry(app, width=30)
    entry_atividade.grid(row=1, column=1, padx=10, pady=5)

    btn = tk.Button(app, text="Salvar", command=lambda: salvar_atividades(entry_nome, entry_atividade))
    btn.grid(row=2, column=0, columnspan=2, pady=10)
    
    app.mainloop()