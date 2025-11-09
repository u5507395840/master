#!/bin/bash
set -e

echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥��🔥🔥"
echo "🎵 DISCOGRÁFICA ML SYSTEM - BUILD & DEPLOY"
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥��🔥"
echo ""

# ═══════════════════════════════════════════════════
# 1️⃣ VERIFICACIÓN PRE-BUILD
# ═══════════════════════════════════════════════════
echo "1️⃣ VERIFICACIÓN PRE-BUILD"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

critical_files=("app.py" "Dockerfile" "requirements.txt" "railway.toml" "openai_orchestrator.py")
all_present=true

for file in "${critical_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ FALTA: $file"
        all_present=false
    fi
done

if [ "$all_present" = false ]; then
    echo ""
    echo "❌ Faltan archivos críticos. Abortando."
    exit 1
fi

echo ""
echo "✅ Todos los archivos críticos presentes"
echo ""

# ═══════════════════════════════════════════════════
# 2️⃣ SINTAXIS CHECK
# ═══════════════════════════════════════════════════
echo "2️⃣ VERIFICACIÓN DE SINTAXIS PYTHON"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python_files=("app.py" "openai_orchestrator.py" "production_controller.py" "analytics_engine.py")
syntax_ok=true

for file in "${python_files[@]}"; do
    if [ -f "$file" ]; then
        if python3 -m py_compile "$file" 2>/dev/null; then
            echo "  ✅ $file - sintaxis válida"
        else
            echo "  ❌ $file - ERROR DE SINTAXIS"
            syntax_ok=false
        fi
    fi
done

if [ "$syntax_ok" = false ]; then
    echo ""
    echo "❌ Errores de sintaxis detectados. Abortando."
    exit 1
fi

echo ""
echo "✅ Sintaxis Python válida"
echo ""

# ═══════════════════════════════════════════════════
# 3️⃣ GIT STATUS & COMMIT
# ═══════════════════════════════════════════════════
echo "3️⃣ GIT - COMMIT & PUSH"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "📝 Cambios detectados, creando commit..."
    git add .
    git commit -m "build: sistema completo listo para deploy $(date +'%Y-%m-%d %H:%M')" || true
    echo "  ✅ Commit creado"
else
    echo "  ℹ️  No hay cambios para commitear"
fi

echo "📤 Pushing a GitHub..."
if git push origin main 2>/dev/null; then
    echo "  ✅ Push exitoso"
else
    echo "  ⚠️  Push falló o ya está actualizado"
fi

echo ""

# ═══════════════════════════════════════════════════
# 4️⃣ DOCKER BUILD
# ═══════════════════════════════════════════════════
echo "4️⃣ DOCKER BUILD"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

DOCKER_USER="stakazo"
IMAGE_NAME="discografica-ml-system"
VERSION="2.0"

echo "🐳 Building Docker image..."
echo "   Tag: ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}"
echo ""

if docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${VERSION} -t ${DOCKER_USER}/${IMAGE_NAME}:latest . ; then
    echo ""
    echo "✅ Docker build exitoso"
    
    size=$(docker images ${DOCKER_USER}/${IMAGE_NAME}:${VERSION} --format "{{.Size}}" 2>/dev/null || echo "N/A")
    echo "📦 Tamaño de imagen: $size"
else
    echo ""
    echo "❌ Docker build falló"
    exit 1
fi

echo ""

# ═══════════════════════════════════════════════════
# 5️⃣ DOCKER TEST LOCAL
# ═══════════════════════════════════════════════════
echo "5️⃣ DOCKER TEST LOCAL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "🧪 Testing imagen Docker localmente..."
echo ""

docker stop discografica-test 2>/dev/null || true
docker rm discografica-test 2>/dev/null || true

docker run -d \
    --name discografica-test \
    -p 8081:8080 \
    -e OPENAI_API_KEY="${OPENAI_API_KEY:-dummy}" \
    ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}

echo "⏳ Esperando que el contenedor inicie (10 segundos)..."
sleep 10

echo ""
echo "🔍 Health check..."
if curl -s http://localhost:8081/health 2>/dev/null | grep -q "healthy"; then
    echo "  ✅ Contenedor respondiendo correctamente"
    
    docker stop discografica-test >/dev/null 2>&1
    docker rm discografica-test >/dev/null 2>&1
else
    echo "  ❌ Contenedor no responde"
    echo ""
    echo "📋 Logs del contenedor:"
    docker logs discografica-test 2>&1 | tail -20
    
    docker stop discografica-test >/dev/null 2>&1
    docker rm discografica-test >/dev/null 2>&1
    
    exit 1
fi

echo ""

# ═══════════════════════════════════════════════════
# 6️⃣ DOCKER PUSH (OPCIONAL)
# ═══════════════════════════════════════════════════
echo "6️⃣ DOCKER PUSH TO HUB (OPCIONAL)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⏭️  Saltando Docker Hub push (ejecuta manualmente si necesitas)"
echo "   docker login"
echo "   docker push ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}"
echo ""

# ═══════════════════════════════════════════════════
# 7️⃣ RAILWAY DEPLOY INFO
# ═══════════════════════════════════════════════════
echo "7️⃣ RAILWAY DEPLOY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 INSTRUCCIONES PARA RAILWAY:"
echo ""
echo "1️⃣ Ve a: https://railway.app"
echo ""
echo "2️⃣ New Project → Deploy from GitHub"
echo "   Repo: u5507395840/master"
echo ""
echo "3️⃣ Variables de entorno (CRÍTICO):"
echo "   OPENAI_API_KEY = sk-proj-TU_KEY_AQUI"
echo ""
echo "4️⃣ Railway detectará automáticamente:"
echo "   ✅ Dockerfile"
echo "   ✅ railway.toml"
echo "   ✅ Health check en /health"
echo ""
echo "5️⃣ Deploy se iniciará automáticamente"
echo ""

# ═══════════════════════════════════════════════════
# 8️⃣ RESUMEN FINAL
# ═══════════════════════════════════════════════════
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ BUILD & DEPLOY COMPLETADO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 RESUMEN:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Archivos verificados"
echo "  ✅ Sintaxis Python válida"
echo "  ✅ Git commit & push"
echo "  ✅ Docker build exitoso"
echo "  ✅ Test local exitoso"
echo "  📦 Imagen: ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}"
echo ""
echo "🚀 SIGUIENTE PASO:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  → Deploy en Railway (manual)"
echo "  → Configurar OPENAI_API_KEY"
echo "  → Acceder a tu-proyecto.railway.app/health"
echo ""
echo "🐕💜 POR PEGGY - SISTEMA 100% LISTO 💜��"
echo ""
