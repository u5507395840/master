#!/bin/bash

echo "════════════════════════════════════════════════════════════════"
echo "🚀 INICIANDO DISCOGRÁFICA ML SYSTEM COMPLETO"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado"
    exit 1
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip3 install -r requirements.txt --quiet

# Iniciar Flask API
echo ""
echo "🌐 Iniciando Flask API (Puerto 8080)..."
python3 app.py &
APP_PID=$!

sleep 3

# Iniciar Production Controller
echo ""
echo "🎮 Iniciando Production Controller (Puerto 7860)..."
python3 production_controller.py &
CONTROLLER_PID=$!

sleep 3

# Iniciar Analytics Engine
echo ""
echo "📊 Iniciando Analytics Engine (Puerto 8501)..."
streamlit run analytics_engine.py --server.port 8501 --server.address 0.0.0.0 &
ANALYTICS_PID=$!

sleep 3

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ SISTEMA COMPLETO INICIADO"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📍 URLs Disponibles:"
echo ""
echo "   Flask API:              http://localhost:8080"
echo "   Production Controller:  http://localhost:7860"
echo "   Analytics Engine:       http://localhost:8501"
echo ""
echo "🛑 Para detener todo, ejecuta:"
echo "   kill $APP_PID $CONTROLLER_PID $ANALYTICS_PID"
echo ""
echo "💜 Sistema operativo - ¡Listo para lanzar campañas virales!"
echo ""

# Mantener script activo
wait
