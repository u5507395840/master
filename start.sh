#!/bin/bash

echo "🚀 Iniciando FastAPI en puerto 8000..."
uvicorn executive_api:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "⏳ Esperando backend (15s)..."
sleep 15

echo "🔍 Verificando que backend responda..."
for i in {1..10}; do
  if curl -f http://localhost:8000/health 2>/dev/null; then
    echo "✅ Backend operativo!"
    break
  fi
  echo "Intento $i/10..."
  sleep 2
done

echo "🎨 Iniciando Streamlit en puerto ${PORT:-8501}..."
streamlit run executive_dashboard.py --server.port ${PORT:-8501} --server.address 0.0.0.0

# Cleanup
kill $BACKEND_PID 2>/dev/null
