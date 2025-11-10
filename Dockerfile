# --- Etapa 1: Build ---
# Usar una imagen oficial de Python como base
FROM python:3.11-slim AS builder

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar solo el archivo de requerimientos para aprovechar el cache de Docker
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# --- Etapa 2: Producción ---
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar las dependencias instaladas desde la etapa de 'builder'
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto en el que corre la aplicación
EXPOSE 8080

# Variable de entorno para asegurar que estamos en modo producción
ENV DUMMY_MODE="false"
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación cuando el contenedor se inicie
# Usamos gunicorn para un servidor de producción más robusto que el de desarrollo de Flask
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "app:app"]
