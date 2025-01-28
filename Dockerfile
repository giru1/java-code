# Dockerfile
FROM python:3.9-slim

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы зависимостей
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте код приложения
COPY . .

# Укажите команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]