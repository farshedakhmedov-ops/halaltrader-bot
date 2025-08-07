from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from pybit.unified_trading import HTTP
import os

# Настройки окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Пример: https://yourapp.onrender.com/webhook

# Инициализация Telegram-бота
bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

# Авторизация Bybit
session = HTTP(
    testnet=False,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)

is_trading = False  # глобальный флаг

def start(update, context):
    global is_trading
    is_trading = True
    update.message.reply_text("🚀 Автотрейдинг запущен!")
    # Здесь начнется торговля — пока пример
    # Можно вставить свою стратегию
    # Например: open_trades()

def stop(update, context):
    global is_trading
    is_trading = False
    update.message.reply_text("🛑 Автотрейдинг остановлен!")

def balance(update, context):
    wallet_balance = session.get_wallet_balance(accountType="UNIFIED")
    usdt = wallet_balance["result"]["list"][0]["coin"][0]["walletBalance"]
    update.message.reply_text(f"💰 Баланс: {usdt} USDT")

# Обработчики команд
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("stop", stop))
dispatcher.add_handler(CommandHandler("balance", balance))

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "ok"

# Установка webhook при запуске
WEBHOOK_URL = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook"

@app.before_first_request
def set_webhook():
    bot.set_webhook(url=WEBHOOK_URL)

# Корневой маршрут
@app.route('/')
def home():
    return "👋 Бот работает через Webhook!"

# Запуск сервера
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
