import tkinter as tk
from database.db_config import buscar_atividades, conectar

def salvar_atividades(entry_nome, entry_atividade):
    nome = entry_nome.get()
    atividade = entry_atividade.get()

    if nome and atividade:
        con = conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO atividades (nome, atividade) VALUES (?, ?)", (nome, atividade))
        con.commit()
        con.close()

        entry_nome.delete(0, tk.END)
        entry_atividade.delete(0, tk.END)

def exibir_atividades(text_widget):
    text_widget.delete("1.0", tk.END)  # Limpa o conteúdo anterior
    atividades = buscar_atividades()
    for id, nome, atividade in atividades:
        text_widget.insert(tk.END, f"{id} - {nome}: {atividade}\n")

def iniciar_ui():
    app = tk.Tk()
    app.title("Cadastro de Atividades")

    tk.Label(app, text="Nome:").pack()
    entry_nome = tk.Entry(app)
    entry_nome.pack()

    tk.Label(app, text="Atividade:").pack()
    entry_atividade = tk.Entry(app)
    entry_atividade.pack()

    btn = tk.Button(app, text="Salvar", command=lambda: salvar_atividades(entry_nome, entry_atividade))
    btn.pack(pady=5)

    text_resultado = tk.Text(app, height=10, width=50)
    text_resultado.pack()

    btn_exibir = tk.Button(app, text="Exibir Atividades", command=lambda: exibir_atividades(text_resultado))
    btn_exibir.pack(pady=5)

    app.mainloop()
