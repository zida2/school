#!/bin/bash

# ========================================
# DÉPLOIEMENT PWA MOBILE - UniERP BF
# ========================================

echo "📱 Déploiement de l'application mobile PWA..."
echo ""

# Se placer dans le dossier mobile
cd mobile

# Déployer avec Vercel
vercel --prod

echo ""
echo "✅ Déploiement terminé!"
echo ""
echo "🔗 URL Mobile:"
echo "- https://school-wheat-six.vercel.app/mobile/"
echo ""
