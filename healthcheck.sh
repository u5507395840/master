#!/bin/bash

echo "🏥 DOGMA Health Check"
echo "===================="

check_service() {
    if curl -sf "$1" > /dev/null 2>&1; then
        echo "✅ $2: UP"
    else
        echo "❌ $2: DOWN"
    fi
}

check_service "http://localhost/health" "NGINX"
check_service "http://localhost:9090/-/healthy" "Prometheus"
check_service "http://localhost:3000/api/health" "Grafana"
check_service "http://localhost:9093/-/healthy" "AlertManager"

echo ""
docker-compose -f docker-compose.prod.yml ps
