
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🚀 Халал-трейдер запущен!")

def stop(update: Update, context: CallbackContext):
    update.message.reply_text("🛑 Бот остановлен.")

def main():
    updater = Updater("PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
