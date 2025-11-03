import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/financas.db")

def get_connection():
    return sqlite3.conncet(DB_PATH, check_same_thread=False)

def init_db():
    conn + get_connection()
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS financas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        descricao TEXT,
        valor REAL,
        data TEXT
    )''')
    conn.commit()
    conn.close()