import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from pybit.unified_trading import HTTP

# Настройки логов
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Переменные окружения
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://your-app-name.onrender.com/webhook

# Инициализация бота и Bybit API
bot = Bot(token=BOT_TOKEN)
bybit = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)
app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

# Команды
def start(update, context):
    update.message.reply_text("🤖 Бот запущен! Начинаю торговлю.")
    # Пример тестовой торговли (внимание: добавьте свою стратегию!)
    try:
        balance = bybit.get_wallet_balance(accountType="UNIFIED")['result']['list'][0]['coin'][0]['walletBalance']
        update.message.reply_text(f"💰 Баланс: {balance} USDT")
    except Exception as e:
        update.message.reply_text(f"Ошибка при получении баланса: {e}")

dispatcher.add_handler(CommandHandler("start", start))

# Flask маршрут для Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "🤖 Бот работает!"

if __name__ == "__main__":
    bot.setWebhook(f"{WEBHOOK_URL}/webhook")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
