from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")  # Defina essa variável no Render Dashboard
app = Flask(__name__)

# Cria a aplicação do Telegram
application = Application.builder().token(TOKEN).build()

# --- Comandos do bot ---
async def start(update: Update, context):
    await update.message.reply_text("Olá! 🤖 Seu bot está online pelo Render com webhook!")

async def echo(update: Update, context):
    await update.message.reply_text(f"Você disse: {update.message.text}")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# --- Webhook endpoint ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok", 200

# --- Página inicial ---
@app.route("/", methods=["GET"])
def home():
    return "Bot do Telegram rodando via Render!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))