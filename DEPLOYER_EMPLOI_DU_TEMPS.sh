#!/bin/bash

# Script de déploiement de l'emploi du temps visuel
# Date: 7 mars 2026

echo "🚀 DÉPLOIEMENT EMPLOI DU TEMPS VISUEL"
echo "======================================"
echo ""

# Étape 1: Vérifier les fichiers modifiés
echo "📋 Étape 1: Vérification des fichiers..."
git status
echo ""

# Étape 2: Ajouter tous les fichiers
echo "➕ Étape 2: Ajout des fichiers au commit..."
git add frontend/css/emploi-temps-grid.css
git add frontend/js/emploi-temps-grid.js
git add frontend/dashboard-admin.html
git add backend/api/models.py
git add backend/api/serializers.py
git add backend/api/urls.py
git add backend/api/views_emploi_temps.py
git add backend/api/migrations/0017_emploidutemps_classe_emploidutemps_type_cours.py
git add SPECIFICATION_EMPLOI_DU_TEMPS_VISUEL.md
git add PLAN_DEVELOPPEMENT_EDT_VISUEL.md
git add INTEGRATION_EMPLOI_DU_TEMPS_VISUEL.md
git add DEPLOIEMENT_EMPLOI_DU_TEMPS.md
git add RESUME_SESSION_EMPLOI_DU_TEMPS.md
git add EMPLOI_DU_TEMPS_COMPLET_FINAL.md
git add COMMIT_MESSAGE.txt
git add DEPLOYER_EMPLOI_DU_TEMPS.sh
echo "✅ Fichiers ajoutés"
echo ""

# Étape 3: Commit
echo "💾 Étape 3: Création du commit..."
git commit -F COMMIT_MESSAGE.txt
echo "✅ Commit créé"
echo ""

# Étape 4: Push
echo "📤 Étape 4: Push vers GitHub..."
read -p "Voulez-vous pusher maintenant? (o/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Oo]$ ]]
then
    git push origin main
    echo "✅ Push effectué"
else
    echo "⏸️  Push annulé. Vous pouvez le faire manuellement avec: git push origin main"
fi
echo ""

# Étape 5: Instructions pour PythonAnywhere
echo "📝 Étape 5: Instructions pour PythonAnywhere"
echo "============================================"
echo ""
echo "Connectez-vous à PythonAnywhere et exécutez:"
echo ""
echo "  cd ~/wendlasida.pythonanywhere.com"
echo "  git pull origin main"
echo "  source .venv/bin/activate"
echo "  python manage.py migrate"
echo ""
echo "Puis rechargez l'application web depuis l'onglet Web."
echo ""

# Étape 6: Vérification Vercel
echo "🌐 Étape 6: Vérification Vercel"
echo "==============================="
echo ""
echo "Vercel déploiera automatiquement le frontend."
echo "URL: https://school-wheat-six.vercel.app"
echo ""

echo "✅ DÉPLOIEMENT TERMINÉ!"
echo ""
echo "📋 Checklist finale:"
echo "  [ ] Backend déployé sur PythonAnywhere"
echo "  [ ] Migration appliquée"
echo "  [ ] Application rechargée"
echo "  [ ] Frontend vérifié sur Vercel"
echo "  [ ] Tests effectués"
echo ""
echo "🎉 Bon déploiement!"
