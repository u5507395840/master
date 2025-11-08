#!/bin/bash
set -e

echo "🔓 DESENCRIPTANDO SECRETS..."

# Verificar que git-crypt esté instalado
if ! command -v git-crypt &> /dev/null; then
    echo "❌ git-crypt no está instalado"
    echo "   Instala: sudo apt-get install git-crypt"
    exit 1
fi

# Verificar que git-crypt esté desbloqueado
if git-crypt status 2>/dev/null | grep -q "not encrypted"; then
    echo "⚠️  git-crypt está bloqueado"
    echo ""
    echo "Para desbloquear:"
    echo "  git-crypt unlock dogma-git-crypt.key"
    echo ""
    echo "Si no tienes la llave, solicítala al equipo"
    exit 1
fi

# Verificar que .env.encrypted exista
if [ ! -f .env.encrypted ]; then
    echo "❌ .env.encrypted no existe"
    exit 1
fi

# Copiar secrets desencriptados a .env.prod
cp .env.encrypted .env.prod

echo "✅ Secrets desencriptados correctamente"
echo "✅ .env.prod generado"
echo ""
echo "🔒 RECUERDA:"
echo "  - .env.prod es LOCAL y NO se commitea"
echo "  - Está protegido por .gitignore"
echo "  - Solo existe en tu máquina"
echo ""
echo "🚀 Ahora puedes deployar:"
echo "   ./deploy.sh"
