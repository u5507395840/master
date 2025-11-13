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
