import sqlite3
import os

# Caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/financas.db")

# Função para abrir conexão
def get_connection():
    
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# Função para inicializar o banco
def init_db():
    
    conn = get_connection()
    cur = conn.cursor()

    # Criação da tabela, se não existir
    cur.execute('''CREATE TABLE IF NOT EXISTS financas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        descricao TEXT,
        valor REAL,
        data TEXT
    )''')

    conn.commit()
    conn.close()