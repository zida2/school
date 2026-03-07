#!/bin/bash

# ========================================
# DÉPLOIEMENT FRONTEND - UniERP BF
# ========================================

echo "🚀 Déploiement du frontend sur Vercel..."
echo ""

# Se placer dans le dossier frontend
cd frontend

# Déployer avec Vercel
vercel --prod

echo ""
echo "✅ Déploiement terminé!"
echo ""
echo "🔗 URLs:"
echo "- Frontend: https://school-wheat-six.vercel.app"
echo "- Mobile: https://school-wheat-six.vercel.app/mobile/"
echo ""
