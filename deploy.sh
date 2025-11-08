#!/bin/bash
set -e

echo "🚀 Deploying DOGMA 24/7 to PRODUCTION..."

if [ ! -f .env.prod ]; then
    echo "❌ .env.prod not found!"
    exit 1
fi

docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d --remove-orphans

echo "⏳ Waiting for services..."
sleep 30

docker-compose -f docker-compose.prod.yml ps

echo "✅ DOGMA deployed!"
echo "🌐 URLs:"
echo "  HTTP:  http://localhost"
echo "  HTTPS: https://localhost (self-signed cert)"
echo "  Grafana: http://localhost:3000"
echo "  Prometheus: http://localhost:9090"
echo "  AlertManager: http://localhost:9093"
