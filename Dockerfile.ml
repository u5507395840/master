FROM python:3.11-slim

WORKDIR /app

# Fix para repositorios apt
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-ml.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ml_engine/ ./ml_engine/
COPY video_generator/ ./video_generator/
COPY analytics_engine.py ./

EXPOSE 8001

CMD ["uvicorn", "analytics_engine:app", "--host", "0.0.0.0", "--port", "8001"]
