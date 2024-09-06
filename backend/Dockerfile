FROM python:3.10-slim

WORKDIR /backend

COPY . /backend

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем приложение FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]