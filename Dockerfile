FROM python:3.11-slim

WORKDIR /app

COPY . .  # Сначала копируем всё
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "halaltrader_bot.py"]
