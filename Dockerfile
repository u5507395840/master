# Dockerfile para DOGMA - Sistema de Marketing Viral AI
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app
ENV USE_ENCRYPTED_VAULT=true

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p logs data/processed security/keys

ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["python", "run.py", "--production"]
