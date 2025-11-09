#!/bin/bash

echo "🔍 VERIFICACIÓN DE PERMISOS"
echo "=========================="
echo ""

echo "📁 Directorios:"
for dir in logs data config backups; do
    if [ -d "$dir" ]; then
        perms=$(stat -c '%a' "$dir" 2>/dev/null || stat -f '%A' "$dir" 2>/dev/null)
        echo "  $dir: $perms $([ "$perms" = "755" ] && echo '✅' || echo '⚠️')"
    fi
done

echo ""
echo "🐍 Scripts ejecutables:"
for script in start.sh deploy.sh railway-deploy.sh; do
    if [ -f "$script" ]; then
        [ -x "$script" ] && echo "  ✅ $script" || echo "  ❌ $script (no ejecutable)"
    fi
done

echo ""
echo "📝 Archivos Python:"
py_files=$(find . -maxdepth 1 -name "*.py" -type f | wc -l)
echo "  Total: $py_files archivos"
echo "  Permisos esperados: 644"

echo ""
echo "✅ Verificación completa"
