# --- Etapa 1: Build ---
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# --- Etapa 2: Producción ---
FROM python:3.11-slim
WORKDIR /app

# Copiar dependencias
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar el código fuente de la aplicación
COPY src/ .

# Exponer el puerto
EXPOSE 8080

# Variables de entorno
ENV DUMMY_MODE="false"
ENV PYTHONUNBUFFERED=1
# Añadir el directorio src al PYTHONPATH para que las importaciones funcionen
ENV PYTHONPATH=/app

# Comando para ejecutar la API
# El punto de entrada ahora es 'discografica_automator.api.app:app'
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "discografica_automator.api.app:app"]
