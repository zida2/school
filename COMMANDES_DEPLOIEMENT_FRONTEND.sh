#!/bin/bash

# ========================================
# DÉPLOIEMENT FRONTEND - Système d'Inscription
# Date: 6 mars 2026
# ========================================

echo "🚀 Déploiement du frontend avec système d'inscription..."
echo ""

# 1. Ajouter tous les fichiers modifiés et créés
echo "📦 Ajout des fichiers..."
git add index.html
git add inscription.html
git add FRONTEND_INSCRIPTION_TERMINE.md
git add DEPLOIEMENT_FRONTEND_VERCEL.txt
git add RECAPITULATIF_MODIFICATIONS_FRONTEND.md
git add AVANT_APRES_FRONTEND.md
git add COMMANDES_DEPLOIEMENT_FRONTEND.sh

# 2. Commit avec message descriptif
echo "💾 Création du commit..."
git commit -m "Frontend: Système inscription professionnel + suppression comptes démo

- Suppression section 'Comptes de démonstration' dans index.html
- Suppression légende 'HIÉRARCHIE DES COMPTES'
- Suppression fonction quickLogin()
- Ajout lien 'S'inscrire comme étudiant'
- Création page inscription.html avec formulaire complet
- Intégration API POST /api/demandes-inscription/
- Design responsive et moderne
- Collecte données marketing (lycée, ville)
- Conformité 100% cahier des charges"

# 3. Push vers GitHub
echo "⬆️  Push vers GitHub..."
git push origin main

echo ""
echo "✅ Déploiement terminé!"
echo ""
echo "📋 Vérifications à faire:"
echo "1. Attendre 1-2 minutes pour le déploiement Vercel"
echo "2. Visiter: https://school-wheat-six.vercel.app"
echo "3. Vérifier que les comptes de démo ont disparu"
echo "4. Cliquer sur 'S'inscrire comme étudiant'"
echo "5. Tester le formulaire d'inscription"
echo ""
echo "🔗 URLs:"
echo "- Frontend: https://school-wheat-six.vercel.app"
echo "- Inscription: https://school-wheat-six.vercel.app/inscription.html"
echo "- Backend API: https://wendlasida.pythonanywhere.com/api/demandes-inscription/"
echo ""
