import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import pandas as pd
import re

#conexao = sqlite3.connect("db_clientes.db")
#c = conexao.cursor()
#
#c.execute(''' CREATE TABLE clientes ( 
#    nome text,
#    sobrenome text,
#    email text,
#    telefone text
#    )
#''')
#
#conexao.commit()
#conexao.close()

def validar_email(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email)

def validar_telefone(telefone):
    return telefone.isdigit()

def cadastrar_cliente():
    if not entry_nome.get() or not entry_sobrenome.get() or not entry_email.get() or not entry_telefone.get():
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return

    if not validar_email(entry_email.get()):
        messagebox.showerror("Erro", "Email inválido")
        return

    if not validar_telefone(entry_telefone.get()):
        messagebox.showerror("Erro", "Telefone deve conter apenas números")
        return

    try:
        conexao = sqlite3.connect("db_clientes.db")
        c = conexao.cursor()

        c.execute("INSERT INTO clientes VALUES (:nome, :sobrenome, :email, :telefone)",
                  {
                      'nome': entry_nome.get(),
                      'sobrenome': entry_sobrenome.get(),
                      'email': entry_email.get(),
                      'telefone': entry_telefone.get()
                  })

        conexao.commit()
        conexao.close()
        entry_nome.delete(0, "end")
        entry_email.delete(0, "end")
        entry_sobrenome.delete(0, "end")
        entry_telefone.delete(0, "end")
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar cliente: {e}")


def exporta_clientes():
    try:
        conexao = sqlite3.connect("db_clientes.db")
        c = conexao.cursor()

        c.execute("SELECT *, oid FROM clientes")
        clientes_cadastrados = c.fetchall()
        clientes_cadastrados = pd.DataFrame(clientes_cadastrados, columns=['nome', 'sobrenome', 'email', 'telefone', 'Id_banco'])
        clientes_cadastrados.to_excel('banco_clientes.xlsx')
        conexao.commit()
        conexao.close()
        messagebox.showinfo("Sucesso", "Clientes exportados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar clientes: {e}")

def criar_interface():
    global entry_nome, entry_sobrenome, entry_email, entry_telefone

    janela = tk.Tk()
    janela.title("Cadastro de Clientes")
    janela.configure(bg='#e0f7fa')

    # Estilo
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12), background='#e0f7fa')
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12), background='#00796b', foreground='black')
    style.configure("TFrame", background='#b2dfdb')

    # Frame pro form
    frame = ttk.Frame(janela, padding="20 20 20 20", style="TFrame", borderwidth=2, relief="groove")
    frame.grid(row=0, column=0, padx=20, pady=20, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Título
    title = ttk.Label(frame, text="Cadastro de Clientes", font=("Helvetica", 16, "bold"), background='#b2dfdb')
    title.grid(row=0, column=0, columnspan=2, pady=10)

    # Labels
    label_nome = ttk.Label(frame, text='Nome', style="TLabel")
    label_nome.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

    label_sobrenome = ttk.Label(frame, text='Sobrenome', style="TLabel")
    label_sobrenome.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

    label_email = ttk.Label(frame, text='Email', style="TLabel")
    label_email.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

    label_telefone = ttk.Label(frame, text='Telefone', style="TLabel")
    label_telefone.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

    # Entradas
    entry_nome = ttk.Entry(frame, width=30)
    entry_nome.grid(row=1, column=1, padx=10, pady=10)

    entry_sobrenome = ttk.Entry(frame, width=30)
    entry_sobrenome.grid(row=2, column=1, padx=10, pady=10)

    entry_email = ttk.Entry(frame, width=30)
    entry_email.grid(row=3, column=1, padx=10, pady=10)

    entry_telefone = ttk.Entry(frame, width=30)
    entry_telefone.grid(row=4, column=1, padx=10, pady=10)

    # Botões
    botao_cadastrar = ttk.Button(janela, text="Cadastrar Cliente", command=cadastrar_cliente, style="TButton", width=30)
    botao_cadastrar.grid(row=1, column=0, padx=20, pady=10, ipadx=10, ipady=5)

    botao_exportar = ttk.Button(janela, text="Exportar Base de Clientes", command=exporta_clientes, style="TButton", width=30)
    botao_exportar.grid(row=2, column=0, padx=20, pady=10, ipadx=10, ipady=5)

    janela.mainloop()

if __name__ == "__main__":
    criar_interface()