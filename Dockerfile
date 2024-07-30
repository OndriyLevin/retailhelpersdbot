# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY .env .
COPY functions.py .
COPY lestat.gif.mp4 .
COPY main.py .
COPY quote.json .
COPY ufo.jpg .
COPY today.json .
COPY DB.py .
COPY env_utils.py .
COPY UserModel.py .

# Определяем команду для запуска вашего бота
CMD ["python", "main.py"]
