
# --- Dockerfile minimalista para modo dummy ---
FROM python:3.11-slim
WORKDIR /app

# Instala solo dependencias básicas para FastAPI y Streamlit
RUN pip install --no-cache-dir fastapi uvicorn streamlit requests python-multipart

# Copia solo los archivos esenciales para dummy mode
COPY executive_api.py /app/app.py
COPY executive_dashboard.py /app/executive_dashboard.py

# Exponer los puertos para API y dashboard
EXPOSE 8080
EXPOSE 8501

# Entrypoint: arranca API y dashboard en modo dummy
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8080 & streamlit run executive_dashboard.py --server.port 8501 --server.address 0.0.0.0"]
