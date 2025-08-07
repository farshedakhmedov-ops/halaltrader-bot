# Используем Python 3.11.6
FROM python:3.11.6

# Создаём рабочую директорию
WORKDIR /app

# Копируем все файлы в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем Telegram-бота
CMD ["python", "halal_trader_bot.py"]
