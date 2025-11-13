FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY executive_api.py /app/executive_api.py
COPY executive_dashboard.py /app/executive_dashboard.py
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
EXPOSE 8000 8501
CMD ["/app/start.sh"]
