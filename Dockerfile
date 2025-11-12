
# --- Dockerfile minimalista para modo dummy ---
FROM python:3.11-slim
WORKDIR /app


# Instala todas las dependencias del proyecto
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


# Copia los archivos esenciales y los secretos necesarios
COPY executive_api.py /app/app.py
COPY executive_dashboard.py /app/executive_dashboard.py
COPY secrets/meta_ads.secret /app/secrets/meta_ads.secret
COPY secrets/youtubeanalyticsonly-1dbb0d479a13.json /app/secrets/youtubeanalyticsonly-1dbb0d479a13.json

# Exponer los puertos para API y dashboard
EXPOSE 80
ENV PORT=80

EXPOSE 8080
EXPOSE 8501

# Entrypoint: arranca API y dashboard en modo dummy
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8080 & streamlit run executive_dashboard.py --server.port 8501 --server.address 0.0.0.0"]
