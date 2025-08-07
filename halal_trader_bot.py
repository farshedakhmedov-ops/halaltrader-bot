from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Dispatcher
from flask import Flask, request
import threading
from pybit.unified_trading import HTTP
import os

# === Настройки ===
TELEGRAM_BOT_TOKEN = "8218238899:AAGs5gZWMJFDEaLlTNgZG_m-EMSNx0eh3T4"
BYBIT_API_KEY = "cm5EBNWS1ykAH2scMg"
BYBIT_API_SECRET = "OCxoLWKBbcKXuTJfwBnMmtq4tcwNkQVtYkkC"

app = Flask(__name__)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

session = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🚀 Халал-трейдер запущен!")

# Команда /balance
def balance(update: Update, context: CallbackContext):
    try:
        result = session.get_wallet_balance(accountType="UNIFIED")
        usdt_balance = result["result"]["list"][0]["totalWalletBalance"]
        update.message.reply_text(f"💰 Баланс: {usdt_balance} USDT")
    except Exception as e:
        update.message.reply_text(f"❌ Ошибка получения баланса:\n{e}")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("balance", balance))

# Webhook endpoint
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Запуск Flask-сервера
def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# Установка Webhook
def set_webhook():
    url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{TELEGRAM_BOT_TOKEN}"
    bot.set_webhook(url)

if __name__ == "__main__":
    threading.Thread(target=run).start()
    set_webhook()
