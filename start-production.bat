@echo off
echo ========================================
echo DOGMA 24/7 Production Starter (Windows)
echo ========================================

docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker not found! Install Docker Desktop first.
    pause
    exit /b 1
)

echo Building DOGMA containers...
docker-compose build --no-cache

echo Starting DOGMA 24/7 services...
docker-compose up -d

echo Service Status:
docker-compose ps

echo.
echo DOGMA 24/7 Production Started!
echo Main App: http://localhost:8000
echo Grafana: http://localhost:3000 (admin/admin123)
echo Prometheus: http://localhost:9090
echo.
pause
