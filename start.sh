#!/bin/bash

echo "🎵 INICIANDO DISCOGRÁFICA ML SYSTEM"
echo "===================================="
echo ""

# Verificar OpenAI API Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY no configurada"
    echo "Configura con: export OPENAI_API_KEY=sk-..."
    echo ""
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip3 install -r requirements.txt --quiet

echo ""
echo "🚀 Iniciando servicios..."
echo ""

# Iniciar Flask API
echo "🌐 Iniciando Flask API (Puerto 8080)..."
python3 app.py &
FLASK_PID=$!

# Esperar a que Flask arranque
sleep 3

# Iniciar Production Controller
echo "🎮 Iniciando Production Controller (Puerto 7860)..."
python3 production_controller.py &
GRADIO_PID=$!

# Iniciar Analytics Engine
echo "📊 Iniciando Analytics Engine (Puerto 8501)..."
streamlit run analytics_engine.py --server.port 8501 --server.address 0.0.0.0 &
STREAMLIT_PID=$!

echo ""
echo "✅ SISTEMA INICIADO"
echo "==================="
echo ""
echo "📡 ENDPOINTS DISPONIBLES:"
echo "  �� Flask API:              http://localhost:8080"
echo "  🎮 Production Controller:  http://localhost:7860"
echo "  📊 Analytics Engine:       http://localhost:8501"
echo ""
echo "💡 Para detener: kill $FLASK_PID $GRADIO_PID $STREAMLIT_PID"
echo ""
echo "🔥 ¡Sistema operativo! Abre los dashboards en tu navegador."
echo ""

# Mantener el script corriendo
wait
