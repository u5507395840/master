#!/bin/bash
set -e

echo "🔐 SETUP DE SECRETS CON GIT-CRYPT"
echo "=================================="

# Instalar git-crypt si no está
if ! command -v git-crypt &> /dev/null; then
    echo "📦 Instalando git-crypt..."
    sudo apt-get update -qq
    sudo apt-get install -y git-crypt
fi

# Inicializar git-crypt
if [ ! -d .git-crypt ]; then
    echo "�� Inicializando git-crypt..."
    git-crypt init
fi

# Exportar llave
KEY_FILE="dogma-git-crypt.key"
if [ ! -f "$KEY_FILE" ]; then
    echo "🔑 Exportando llave..."
    git-crypt export-key "$KEY_FILE"
    echo ""
    echo "✅ Llave exportada: $KEY_FILE"
    echo ""
    echo "🚨 IMPORTANTE:"
    echo "  1. Guarda esta llave en un lugar SEGURO"
    echo "  2. NO la commitees (está en .gitignore)"
    echo "  3. Compártela solo con tu equipo mediante canal seguro"
    echo "  4. Guárdala en: 1Password, LastPass, AWS Secrets, etc."
fi

echo ""
echo "✅ Setup completado"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "  1. Edita .env.encrypted con valores reales"
echo "  2. git add .env.encrypted secrets/"
echo "  3. git commit -m 'Add encrypted secrets'"
echo "  4. git push"
echo ""
echo "🔓 EN OTRA MÁQUINA:"
echo "  git clone <repo>"
echo "  git-crypt unlock dogma-git-crypt.key"
echo "  ./decrypt-secrets.sh"
