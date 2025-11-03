from flask import Flask, request
from core.database import init_db
from core.handlers import handle_message

app = Flask(__name__)

# 🔹 Inicializa o banco logo no início, compatível com Flask 3
with app.app_context():
    init_db()

@app.route("/", methods=["GET"])
def home():
    return "Bot de Finanças ativo! 🚀"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    msg = request.form.get("Body")
    resposta = handle_message(msg)
    return f"<Response><Message>{resposta}</Message></Response>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)