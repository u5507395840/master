#!/bin/bash
set -e

echo "🚀 Optimizando DOGMA Monorepo..."
echo ""

# 1. Crear Dockerfiles especializados
echo "📦 [1/5] Creando Dockerfiles especializados..."

cat > Dockerfile.api << 'DAPI'
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY requirements-api.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY executive_api.py main.py api_controller.py ./
COPY core/ ./core/
COPY security/ ./security/
COPY compliance/ ./compliance/
COPY campaign_manager/ ./campaign_manager/
RUN echo '#!/bin/bash\nuvicorn executive_api:app --host 0.0.0.0 --port 8000' > start.sh && chmod +x start.sh
EXPOSE 8000
CMD ["./start.sh"]
DAPI

cat > Dockerfile.dashboard << 'DDASH'
FROM python:3.11-slim
WORKDIR /app
COPY requirements-dashboard.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY executive_dashboard.py ./
ENV BACKEND_URL=http://localhost:8000
EXPOSE 8501
CMD ["streamlit", "run", "executive_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
DDASH

cat > Dockerfile.ml << 'DML'
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 ffmpeg curl && rm -rf /var/lib/apt/lists/*
COPY requirements-ml.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ml_engine/ ./ml_engine/
COPY video_generator/ ./video_generator/
COPY analytics_engine.py openai_orchestrator.py openai_client.py ./
EXPOSE 8001
CMD ["uvicorn", "analytics_engine:app", "--host", "0.0.0.0", "--port", "8001"]
DML

cat > Dockerfile.workers << 'DWORK'
FROM python:3.11-slim
WORKDIR /app
COPY requirements-workers.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY uploaders/ ./uploaders/
COPY telegram_bot/ ./telegram_bot/
COPY tools/ ./tools/
CMD ["python", "-m", "telegram_bot.bot"]
DWORK

echo "✅ Dockerfiles creados"

# 2. Dividir requirements
echo "📝 [2/5] Dividiendo requirements..."

cat > requirements-api.txt << 'RAPI'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
python-dotenv==1.0.0
python-multipart==0.0.6
requests==2.31.0
RAPI

cat > requirements-dashboard.txt << 'RDASH'
streamlit==1.29.0
requests==2.31.0
plotly==5.18.0
pandas==2.1.3
python-dotenv==1.0.0
RDASH

cat > requirements-ml.txt << 'RML'
fastapi==0.104.1
uvicorn==0.24.0
ultralytics==8.0.220
opencv-python-headless==4.8.1.78
torch==2.1.1
torchvision==0.16.1
Pillow==10.1.0
moviepy==1.0.3
numpy==1.26.2
scikit-learn==1.3.2
supabase==2.0.3
openai==1.3.0
python-dotenv==1.0.0
RML

cat > requirements-workers.txt << 'RWORK'
google-api-python-client==2.108.0
python-telegram-bot==20.7
requests==2.31.0
python-dotenv==1.0.0
psutil==5.9.6
RWORK

echo "✅ Requirements divididos"

# 3. Crear railway.toml
echo "🚂 [3/5] Configurando Railway..."

cat > railway.toml << 'RAIL'
[build]
builder = "DOCKERFILE"

[deploy]
startCommand = ""
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
RAIL

echo "✅ railway.toml creado"

# 4. Crear start scripts optimizados
echo "⚡ [4/5] Creando scripts de inicio..."

cat > start-api.sh << 'SAPI'
#!/bin/bash
echo "🚀 Starting DOGMA API..."
uvicorn executive_api:app --host 0.0.0.0 --port ${PORT:-8000}
SAPI
chmod +x start-api.sh

cat > start-dashboard.sh << 'SDASH'
#!/bin/bash
echo "🎨 Starting DOGMA Dashboard..."
streamlit run executive_dashboard.py --server.port ${PORT:-8501} --server.address 0.0.0.0
SDASH
chmod +x start-dashboard.sh

cat > start-ml.sh << 'SML'
#!/bin/bash
echo "🧠 Starting ML Engine..."
uvicorn analytics_engine:app --host 0.0.0.0 --port ${PORT:-8001}
SML
chmod +x start-ml.sh

echo "✅ Scripts de inicio creados"

# 5. Actualizar .dockerignore
echo "🚫 [5/5] Optimizando .dockerignore..."

cat > .dockerignore << 'DIGN'
# Git
.git
.gitignore

# Python
__pycache__
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Secrets
.env
*.secret
secrets/*.json
secrets/*.secret

# IDE
.vscode/
.idea/
*.swp

# Docs y tests
docs/
tests/
*.md
README.md

# Build artifacts
*.backup
*.bak
*.log

# Deploy scripts
*.sh
*.bat
docker-compose*.yml
prometheus.yml
grafana/
ssl/
alertmanager.yml
alerts.yml
loki-config.yml
promtail-config.yml

# Otros repos
longcat-repo/
n8n_workflows/

# OS
.DS_Store
Thumbs.db
DIGN

echo "✅ .dockerignore optimizado"

# 6. Actualizar executive_dashboard.py para usar variable de entorno
echo "🔧 Actualizando dashboard para usar BACKEND_URL..."

if [ -f executive_dashboard.py ]; then
    sed -i.bak 's|localhost:8080|localhost:8000|g' executive_dashboard.py
    sed -i.bak 's|127.0.0.1:8080|localhost:8000|g' executive_dashboard.py
    
    # Agregar soporte para variable de entorno si no existe
    if ! grep -q "BACKEND_URL" executive_dashboard.py; then
        sed -i.bak '1i import os' executive_dashboard.py
    fi
fi

# 7. Crear README con instrucciones
cat > DEPLOY.md << 'README'
# 🚀 DOGMA - Guía de Deploy

## Arquitectura Monorepo Optimizada

Este repo contiene 4 servicios independientes con Dockerfiles especializados:

### 1. **API Core** (Dockerfile.api)
```bash
railway up --dockerfile Dockerfile.api
```
- Puerto: 8000
- Variables: `META_API_TOKEN`, `YOUTUBE_API_KEY`

### 2. **Dashboard** (Dockerfile.dashboard)
```bash
railway up --dockerfile Dockerfile.dashboard
```
- Puerto: 8501
- Variables: `BACKEND_URL=https://tu-api.railway.app`

### 3. **ML Engine** (Dockerfile.ml)
```bash
railway up --dockerfile Dockerfile.ml
```
- Puerto: 8001
- Requiere: Plan Pro (RAM alta para PyTorch)

### 4. **Workers** (Dockerfile.workers)
```bash
railway up --dockerfile Dockerfile.workers
```
- Sin puerto (background worker)
- Variables: `TELEGRAM_BOT_TOKEN`

## Deploy Rápido

### Opción A: Railway CLI (4 servicios en un repo)
```bash
# Crear 4 servicios desde el mismo repo
railway link
railway service create api
railway service create dashboard
railway service create ml-engine
railway service create workers

# Deploy cada uno
railway up --service api --dockerfile Dockerfile.api
railway up --service dashboard --dockerfile Dockerfile.dashboard
railway up --service ml-engine --dockerfile Dockerfile.ml
railway up --service workers --dockerfile Dockerfile.workers
```

### Opción B: Railway Dashboard
1. Crea 4 servicios en Railway
2. Conecta todos al MISMO repo
3. En cada servicio, configura:
   - **API**: Root Directory: `/`, Dockerfile Path: `Dockerfile.api`
   - **Dashboard**: Root Directory: `/`, Dockerfile Path: `Dockerfile.dashboard`
   - **ML Engine**: Root Directory: `/`, Dockerfile Path: `Dockerfile.ml`
   - **Workers**: Root Directory: `/`, Dockerfile Path: `Dockerfile.workers`

## Tamaños de Build

- API: ~100MB
- Dashboard: ~50MB  
- ML Engine: ~800MB (PyTorch + YOLO)
- Workers: ~80MB

## Variables de Entorno

### API Service
```
META_API_TOKEN=xxx
YOUTUBE_API_KEY=xxx
PORT=8000
```

### Dashboard Service
```
BACKEND_URL=https://dogma-api.railway.app
PORT=8501
```

### ML Engine Service
```
OPENAI_API_KEY=xxx
PORT=8001
```

### Workers Service
```
TELEGRAM_BOT_TOKEN=xxx
META_API_TOKEN=xxx
YOUTUBE_API_KEY=xxx
```

## Desarrollo Local
```bash
# API
docker build -f Dockerfile.api -t dogma-api .
docker run -p 8000:8000 dogma-api

# Dashboard
docker build -f Dockerfile.dashboard -t dogma-dashboard .
docker run -p 8501:8501 -e BACKEND_URL=http://localhost:8000 dogma-dashboard

# ML Engine
docker build -f Dockerfile.ml -t dogma-ml .
docker run -p 8001:8001 dogma-ml

# Workers
docker build -f Dockerfile.workers -t dogma-workers .
docker run dogma-workers
```
README

echo ""
echo "=================================="
echo "✅ OPTIMIZACIÓN COMPLETADA"
echo "=================================="
echo ""
echo "📦 Archivos creados:"
echo "  ✓ Dockerfile.api"
echo "  ✓ Dockerfile.dashboard"
echo "  ✓ Dockerfile.ml"
echo "  ✓ Dockerfile.workers"
echo "  ✓ requirements-api.txt"
echo "  ✓ requirements-dashboard.txt"
echo "  ✓ requirements-ml.txt"
echo "  ✓ requirements-workers.txt"
echo "  ✓ railway.toml"
echo "  ✓ DEPLOY.md"
echo ""
echo "📊 Tamaño estimado de builds:"
echo "  • API: ~100MB"
echo "  • Dashboard: ~50MB"
echo "  • ML Engine: ~800MB"
echo "  • Workers: ~80MB"
echo ""
echo "🚀 Próximos pasos:"
echo ""
echo "1. Commit y push:"
echo "   git add -A"
echo "   git commit -m 'refactor: optimize monorepo with multi-dockerfile architecture'"
echo "   git push"
echo ""
echo "2. Deploy en Railway (lee DEPLOY.md para detalles):"
echo "   railway link"
echo "   railway up --dockerfile Dockerfile.api"
echo ""
echo "3. Configura variables de entorno en Railway dashboard"
echo ""
