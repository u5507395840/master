FROM python:3.11-slim

WORKDIR /app

# Copiar requirements si existe
COPY requirements.txt* ./
RUN pip3 install --no-cache-dir -r requirements.txt 2>/dev/null || echo "No requirements.txt"

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando por defecto (ajusta según tu app)
CMD ["python3", "-m", "http.server", "8000"]
