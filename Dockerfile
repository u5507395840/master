# ════════════════════════════════════════════════════
# DISCOGRÁFICA ML SYSTEM - DOCKERFILE INTEGRADO
# Merge: Esqueleto base + Funcionalidades ML
# ════════════════════════════════════════════════════

FROM python:3.11-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV GRADIO_PORT=7860
ENV STREAMLIT_PORT=8501

# Metadata
LABEL maintainer="Alberto <alberto@discografica-ml.com>"
LABEL description="Sistema integral de automatización musical con IA"
LABEL version="2.0.0-integrated"

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    git \
    ffmpeg \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar solo requirements primero (cache de Docker)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código del proyecto
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/videos data/campaigns data/metrics logs config && \
    chmod -R 755 data logs config

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Exponer puertos
EXPOSE 8080 7860 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Comando de inicio
# Por defecto solo Flask API (esqueleto base)
# Para dashboards: usar docker-compose o Railway configurado
CMD ["python", "app.py"]
