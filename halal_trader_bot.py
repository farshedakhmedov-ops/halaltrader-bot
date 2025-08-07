import os
import logging
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from pybit.unified_trading import HTTP

# Логирование
logging.basicConfig(level=logging.INFO)

# Получаем токены из переменных среды
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
BYBIT_API_KEY = os.environ.get("BYBIT_API_KEY")
BYBIT_API_SECRET = os.environ.get("BYBIT_API_SECRET")

# Подключение к Bybit (UNIFIED аккаунт)
session = HTTP(
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🚀 Халал-трейдер запущен!")

# Команда /stop
def stop(update: Update, context: CallbackContext):
    update.message.reply_text("⛔️ Бот остановлен.")

# Команда /balance
def balance(update: Update, context: CallbackContext):
    try:
        result = session.get_wallet_balance(accountType="UNIFIED")
        usdt_balance = result["result"]["list"][0]["totalWalletBalance"]
        update.message.reply_text(f"💰 Баланс: {usdt_balance} USDT")
    except Exception as e:
        update.message.reply_text(f"❌ Ошибка получения баланса:\n{e}")

# Главная функция
def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("balance", balance))

    updater.start_polling()
    updater.idle()

if name == '__main__':
    main()
