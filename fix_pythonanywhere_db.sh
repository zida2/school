#!/bin/bash

echo "=========================================="
echo "  CORRECTION BASE DE DONNÉES PYTHONANYWHERE"
echo "=========================================="
echo ""

cd ~/school/backend

# Sauvegarder l'ancien .env si existe
if [ -f .env ]; then
    echo "📋 Sauvegarde de .env vers .env.backup"
    cp .env .env.backup
fi

# Créer un nouveau .env sans les variables PostgreSQL
echo "✏️  Création du nouveau .env..."
cat > .env << 'EOF'
# Configuration Email (à configurer)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
DEFAULT_FROM_EMAIL=noreply@unierp.bf

# Frontend URL
FRONTEND_URL=https://school-wheat-six.vercel.app

# Base de données: SQLite (pas de variables DB_* = utilise SQLite automatiquement)
# Ne PAS définir DB_HOST, DB_NAME, etc. pour utiliser SQLite
EOF

echo "✅ Fichier .env mis à jour"
echo ""
echo "📝 Contenu du nouveau .env:"
cat .env
echo ""
echo "=========================================="
echo "  PROCHAINE ÉTAPE"
echo "=========================================="
echo ""
echo "Allez dans l'onglet Web de PythonAnywhere"
echo "et cliquez sur le bouton vert 'Reload'"
echo ""
echo "Puis testez: https://wendlasida.pythonanywhere.com/api/filieres/"
echo ""
