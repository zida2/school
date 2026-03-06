#!/bin/bash

# Script de déploiement automatique pour PythonAnywhere
# À exécuter dans le bash console de PythonAnywhere

echo "========================================="
echo "DÉPLOIEMENT URGENT - RESTAURATION PAIEMENTS"
echo "========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Aller dans le dossier
echo -e "${YELLOW}[1/6] Navigation vers le dossier du projet...${NC}"
cd ~/school || { echo -e "${RED}Erreur: Impossible d'accéder au dossier ~/school${NC}"; exit 1; }
echo -e "${GREEN}✓ Dossier trouvé${NC}"
echo ""

# 2. Activer l'environnement virtuel
echo -e "${YELLOW}[2/6] Activation de l'environnement virtuel...${NC}"
source ~/.virtualenvs/myenv/bin/activate || { echo -e "${RED}Erreur: Impossible d'activer l'environnement virtuel${NC}"; exit 1; }
echo -e "${GREEN}✓ Environnement virtuel activé${NC}"
echo ""

# 3. Récupérer les modifications
echo -e "${YELLOW}[3/6] Récupération des dernières modifications depuis GitHub...${NC}"
git pull origin main || { echo -e "${RED}Erreur: Impossible de récupérer les modifications${NC}"; exit 1; }
echo -e "${GREEN}✓ Code mis à jour${NC}"
echo ""

# 4. Appliquer les migrations
echo -e "${YELLOW}[4/6] Application des migrations de base de données...${NC}"
cd backend
python manage.py migrate || { echo -e "${RED}Erreur: Échec des migrations${NC}"; exit 1; }
echo -e "${GREEN}✓ Migrations appliquées${NC}"
echo ""

# 5. Vérifier le système
echo -e "${YELLOW}[5/6] Vérification du système...${NC}"
python manage.py check || { echo -e "${RED}Erreur: Le système a des problèmes${NC}"; exit 1; }
echo -e "${GREEN}✓ Système OK${NC}"
echo ""

# 6. Redémarrer l'application
echo -e "${YELLOW}[6/6] Redémarrage de l'application...${NC}"
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
echo -e "${GREEN}✓ Application redémarrée${NC}"
echo ""

echo "========================================="
echo -e "${GREEN}DÉPLOIEMENT TERMINÉ AVEC SUCCÈS!${NC}"
echo "========================================="
echo ""
echo "Testez maintenant:"
echo "  - https://wendlasida.pythonanywhere.com/api/paiements/"
echo "  - https://wendlasida.pythonanywhere.com/api/finances/statistiques/"
echo ""
