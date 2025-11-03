from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import asyncio

# --- Configuração ---
TOKEN = os.getenv("BOT_TOKEN")  # Defina no Render Dashboard
app = Flask(__name__)

# Cria a aplicação do Telegram
application = Application.builder().token(TOKEN).build()

# --- Banco de dados simples em memória ---
saldo_total = 0.0

# --- Comandos do bot ---

async def start(update: Update, context):
    await update.message.reply_text("Olá! 👋 Seu bot de finanças está online pelo Render.\n"
                                    "Use /add, /remove e /saldo para gerenciar seu dinheiro!")

async def add(update: Update, context):
    global saldo_total
    try:
        valor = float(context.args[0])
        saldo_total += valor
        await update.message.reply_text(f"✅ Adicionado R$ {valor:.2f}\n💰 Saldo atual: R$ {saldo_total:.2f}")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Use assim: /add 100")

async def remove(update: Update, context):
    global saldo_total
    try:
        valor = float(context.args[0])
        saldo_total -= valor
        await update.message.reply_text(f"❌ Retirado R$ {valor:.2f}\n💰 Saldo atual: R$ {saldo_total:.2f}")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Use assim: /remove 50")

async def saldo(update: Update, context):
    await update.message.reply_text(f"💰 Seu saldo atual é: R$ {saldo_total:.2f}")

async def echo(update: Update, context):
    await update.message.reply_text(f"Você disse: {update.message.text}")

# --- Registrando os comandos ---
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("add", add))
application.add_handler(CommandHandler("remove", remove))
application.add_handler(CommandHandler("saldo", saldo))
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
    return "Bot de finanças ativo via Render!", 200

# --- Inicialização ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
