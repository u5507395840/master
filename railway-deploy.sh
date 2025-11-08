#!/bin/bash
echo "🚂 DOGMA 24/7 - Railway Deployment"
echo ""

# Login
echo "🔑 Login a Railway..."
railway login --browserless

# Init proyecto
echo ""
echo "📝 Inicializando proyecto..."
railway init

# Configurar variables
echo ""
echo "🔐 Configurando secrets..."
if [ -f .env.prod ]; then
    while IFS='=' read -r key value; do
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        echo "  Setting $key..."
        railway variables set "$key=$value"
    done < .env.prod
fi

# Deploy
echo ""
echo "🚀 Deployando..."
railway up --detach

echo ""
echo "✅ Deployment completado"
echo ""
echo "Ver logs:"
echo "  railway logs -f"
echo ""
echo "Abrir dashboard:"
echo "  railway open"
