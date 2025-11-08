FROM python:3.11-slim

WORKDIR /app

# Instalar curl para healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt* ./
RUN pip3 install --no-cache-dir -r requirements.txt 2>/dev/null || \
    pip3 install --no-cache-dir flask redis prometheus-client

# Copiar código
COPY . .

# Health check endpoint
RUN echo 'from flask import Flask; app = Flask(__name__); @app.route("/health"); def health(): return "OK", 200; app.run(host="0.0.0.0", port=8000)' > app.py

EXPOSE 8000

CMD ["python3", "app.py"]
