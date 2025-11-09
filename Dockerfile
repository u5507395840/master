FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV DUMMY_MODE=true

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p logs output/clips tools/verification/reports

# Exponer puertos
EXPOSE 8080 7860 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Script de inicio
CMD ["bash", "-c", "python3 app.py & python3 production_controller.py & streamlit run analytics_engine.py --server.port 8501 --server.address 0.0.0.0 & wait"]
