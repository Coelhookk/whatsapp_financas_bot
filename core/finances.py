from datetime import datetime
from core.database import get_connection

def add_transacao(tipo, valor, descricao):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO financas (tipo, descricao, valor, data) VALUES (?, ?, ?, ?)",
        (tipo, descricao, valor, datetime.now().strftime("%Y-%m-%d")),
    )
    conn.commit()
    conn.close()

def get_saldo():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(valor) FROM financas WHERE tipo='entrada'")
    entradas = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(valor) FROM financas WHERE tipo='saida'")
    saidas = cur.fetchone()[0] or 0
    conn.close()
    return entradas - saidas
