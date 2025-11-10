#!/bin/bash
# Arranca el backend y el dashboard ejecutivo en terminales separadas

# Arranca el backend en background
nohup uvicorn executive_api:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend iniciado con PID $BACKEND_PID (log: backend.log)"

# Espera a que el backend esté disponible
until curl -s http://localhost:8000/status > /dev/null; do
  echo "Esperando a que el backend esté disponible..."
  sleep 2
done

echo "Backend disponible. Arrancando dashboard..."

# Arranca el dashboard en background
nohup streamlit run executive_dashboard.py > dashboard.log 2>&1 &
DASHBOARD_PID=$!
echo "Dashboard iniciado con PID $DASHBOARD_PID (log: dashboard.log)"

echo "Accede al dashboard en http://localhost:8501"
