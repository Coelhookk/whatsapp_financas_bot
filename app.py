from flask import Flask, request
from core.database import init_db
from core.handlers import handle_message
from telegram_bot import iniciar_bot
import threading

app = Flask(__name__)

@app.before_request
def setup():
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
    # Inicia o Telegram em outra thread
    t = threading.Thread(target=iniciar_bot)
    t.start()

    # Roda o Flask
    app.run(host="0.0.0.0", port=5000)