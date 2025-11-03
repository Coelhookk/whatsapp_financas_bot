from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler
import asyncio
import os

# =========================================================
# Configurações
# =========================================================
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)

# =========================================================
# Dados dos usuários
# =========================================================
users_data = {}  # Exemplo: {chat_id: saldo}

# =========================================================
# Comandos do bot
# =========================================================
async def start(update, context):
    chat_id = update.effective_chat.id
    users_data.setdefault(chat_id, 0.0)
    await update.message.reply_text(
        "💰 Olá! Sou seu bot de finanças!\n\n"
        "Use:\n"
        "/add 50 → adiciona 50 ao saldo\n"
        "/remove 30 → retira 30 do saldo\n"
        "/saldo → mostra quanto você tem agora 💵"
    )

async def add(update, context):
    chat_id = update.effective_chat.id
    users_data.setdefault(chat_id, 0.0)
    try:
        valor = float(context.args[0])
        users_data[chat_id] += valor
        await update.message.reply_text(f"✅ Adicionado R$ {valor:.2f}\n💰 Saldo atual: R$ {users_data[chat_id]:.2f}")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Use assim: /add 50")

async def remove(update, context):
    chat_id = update.effective_chat.id
    users_data.setdefault(chat_id, 0.0)
    try:
        valor = float(context.args[0])
        users_data[chat_id] -= valor
        await update.message.reply_text(f"💸 Retirado R$ {valor:.2f}\n💰 Saldo atual: R$ {users_data[chat_id]:.2f}")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Use assim: /remove 30")

async def saldo(update, context):
    chat_id = update.effective_chat.id
    saldo_atual = users_data.get(chat_id, 0.0)
    await update.message.reply_text(f"💰 Seu saldo atual é R$ {saldo_atual:.2f}")

# =========================================================
# Configuração do bot
# =========================================================
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("add", add))
application.add_handler(CommandHandler("remove", remove))
application.add_handler(CommandHandler("saldo", saldo))

# Inicializa o Application fora do loop
async def init_app():
    if not application._initialized:
        await application.initialize()
        await application.start()

asyncio.get_event_loop().run_until_complete(init_app())

# =========================================================
# Rota do Webhook
# =========================================================
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.ensure_future(application.process_update(update))
    return "ok"

@app.route('/')
def index():
    return "Bot de Finanças ativo no Render 🚀"

# =========================================================
# Execução local (opcional)
# =========================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
