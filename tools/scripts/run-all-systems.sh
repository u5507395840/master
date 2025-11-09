#!/bin/bash
set -e

echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "🎵 STAKAS AUTOMATION SYSTEM - FULL STACK"
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo ""

# Verificar variables
echo "1️⃣ Verificando configuración..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️ OPENAI_API_KEY not set (funcionará en modo básico)"
else
    echo "✅ OPENAI_API_KEY configurado"
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️ TELEGRAM_BOT_TOKEN not set (bot no iniciará)"
else
    echo "✅ TELEGRAM_BOT_TOKEN configurado"
fi

echo ""
echo "2️⃣ Iniciando módulos..."

# Flask API
echo "🌐 Iniciando Flask API..."
python3 app.py &
API_PID=$!
sleep 3

# System Monitor
echo "📊 Iniciando System Monitor..."
python3 tools/monitoring/system_monitor.py &
MON_PID=$!

# Telegram Bot (solo si hay token)
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo "🤖 Iniciando Telegram Bot..."
    python3 telegram_bot/bot.py &
    BOT_PID=$!
else
    echo "⏭️ Telegram Bot omitido (no hay token)"
    BOT_PID=""
fi

echo ""
echo "✅ Sistema iniciado"
echo ""
echo "PIDs:"
echo "  Flask API: $API_PID"
echo "  Monitor: $MON_PID"
[ -n "$BOT_PID" ] && echo "  Telegram Bot: $BOT_PID"
echo ""
echo "Logs en tiempo real:"
echo "  tail -f logs/*.log"
echo ""
echo "Para detener:"
echo "  kill $API_PID $MON_PID $BOT_PID"
echo ""
echo "🐕💜 SISTEMA 100% OPERATIVO 💜🐕"
echo ""

# Mantener script vivo
wait
