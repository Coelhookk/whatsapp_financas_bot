from core.finances import add_transacao, get_saldo

def handle_message(msg):
    msg = msg.lower().strip()
    resp = "❓ Comando não reconhecido. Tente: 'add gasto', 'add ganho' ou 'saldo'."

    if msg.startswith("add gasto"):
        _, _, valor, *desc = msg.split()
        add_transacao("saida", float(valor), " ".join(desc))
        resp = f"💸 Gasto de R${valor} registrado."
    elif msg.startswith("add ganho"):
        _, _, valor, *desc = msg.split()
        add_transacao("entrada", float(valor), " ".join(desc))
        resp = f"💰 Ganho de R${valor} registrado."
    elif msg == "saldo":
        saldo = get_saldo()
        resp = f"📊 Saldo atual: R${saldo:.2f}"

    return resp
