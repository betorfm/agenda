import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda - CRUD com Tkinter e PostgreSQL")
        self.root.geometry("900x500") # Tamanho inicial da janela

        #Elementos da Interface
        self.setup_ui()

    def setup_ui(self):
        # Atribui pesos às colunas para expansão proporcional
        self.root.grid_columnconfigure(0, weight=1)  # Coluna 0 com peso
        self.root.grid_columnconfigure(1, weight=1)  # Coluna 1 com peso maior
        self.root.grid_columnconfigure(2, weight=1)  # Coluna 2 com peso
        self.root.grid_columnconfigure(3, weight=1)  # Coluna 3 com peso

        # Campos de entrada
        tk.Label(self.root, text="Nome", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#333", borderwidth=2, relief="solid").grid(row=0, column=0, padx=10, pady=10)
        self.nome_entry = tk.Entry(self.root, width=80)
        self.nome_entry.grid(row=0, column=1,columnspan=3, padx=10, pady=10)

        tk.Label(self.root, text="Telefone").grid(row=1, column=0, padx=1, pady=10)
        self.telefone_entry = tk.Entry(self.root, width=80)
        self.telefone_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

        tk.Label(self.root, text="Email").grid(row=2, column=0, padx=1, pady=10)
        self.email_entry = tk.Entry(self.root, width=80)
        self.email_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

        # Botões CRUD
        tk.Button(self.root, text="Criar", command=self.criar_contato, font=("Arial", 12, "bold"),
          bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white").grid(row=3, column=0, pady=10)
        tk.Button(self.root, text="Ler", command=self.ler_contatos).grid(row=3, column=1, pady=10)
        tk.Button(self.root, text="Atualizar", command=self.atualizar_contato).grid(row=3, column=2, pady=10)
        tk.Button(self.root, text="Deletar", command=self.deletar_contato).grid(row=3, column=3, pady=10)

        # Tabela de dados
        self.tabela = ttk.Treeview(self.root, columns=("ID", "Nome", "Telefone", "Email"), show="headings")
        self.tabela.grid(row=5, column=0, columnspan=4, padx=10, pady=20)
        self.tabela.heading("ID", text="ID")
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("Telefone", text="Telefone")
        self.tabela.heading("Email", text="Email")


    def criar_contato(self):
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()

        if nome:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contatos (nome, telefone, email) VALUES (%s, %s, %s)", (nome, telefone, email))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Sucesso", "Contato criado com sucesso!")
            self.limpar_campos()
        else:
            messagebox.showwarning("Erro", "O campo Nome é obrigatório!")


    def ler_contatos(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contatos")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Limpar tabela
        for i in self.tabela.get_children():
            self.tabela.delete(i)

        # Inserir os dados na tabela
        for row in rows:
            self.tabela.insert("", "end", values=row)


    def atualizar_contato(self):
        selected_item = self.tabela.selection()
        if selected_item:
            contato = self.tabela.item(selected_item)["values"]
            id_contato = contato[0]

            nome = self.nome_entry.get()
            telefone = self.telefone_entry.get()
            email = self.email_entry.get()

            if nome:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE contatos SET nome = %s, telefone = %s, email = %s WHERE id = %s",
                    (nome, telefone, email, id_contato),
                )
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Sucesso", "Contato atualizado com sucesso!")
                self.limpar_campos()
                self.ler_contatos()
            else:
                messagebox.showwarning("Erro", "O campo Nome é obrigatório!")
        else:
            messagebox.showwarning("Erro", "Selecione um contato para atualizar!")


    def deletar_contato(self):
        selected_item = self.tabela.selection()
        if selected_item:
            contato = self.tabela.item(selected_item)["values"]
            id_contato = contato[0]

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contatos WHERE id = %s", (id_contato,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Sucesso", "Contato deletado com sucesso!")
            self.ler_contatos()
        else:
            messagebox.showwarning("Erro", "Selecione um contato para deletar!")


    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()