from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from core.handlers import handle_message
import asyncio
import os

TOKEN = os.getenv("8209483660:AAFYEkfcpXNhw2_UBTNL-8UxUhcgqXnBcr0")  # o Render vai armazenar isso

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou seu bot de finanças 💰")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    resposta = handle_message(msg)
    await update.message.reply_text(resposta)

def iniciar_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("🤖 Bot do Telegram está rodando...")
    app.run_polling()

if __name__ == "__main__":
    iniciar_bot()