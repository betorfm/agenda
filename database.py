import psycopg2

def conectar():
    return psycopg2.connect(
        dbname="agenda",
        user="postgres",
        password="Developer123**",
        host="localhost",
        port="5432"
    )

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contatos (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            telefone VARCHAR(15),
            email VARCHAR(100)
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Executa a criação da tabela ao importar o módulo
criar_tabela()