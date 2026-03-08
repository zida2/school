# 📅 Emploi du Temps Visuel - Guide Rapide

## ✅ Statut: 100% TERMINÉ

## 🚀 Déploiement Rapide

### Option 1: Script Automatique
```bash
bash DEPLOYER_EMPLOI_DU_TEMPS.sh
```

### Option 2: Manuel

#### 1. Push Git
```bash
git add .
git commit -F COMMIT_MESSAGE.txt
git push origin main
```

#### 2. PythonAnywhere
```bash
cd ~/wendlasida.pythonanywhere.com
git pull origin main
source .venv/bin/activate
python manage.py migrate
# Recharger l'app web
```

#### 3. Vercel
Déploiement automatique ✅

## 📦 Fichiers Créés

### Frontend
- `frontend/css/emploi-temps-grid.css`
- `frontend/js/emploi-temps-grid.js`
- `frontend/dashboard-admin.html` (modifié)

### Backend
- `backend/api/views_emploi_temps.py`
- `backend/api/models.py` (modifié)
- `backend/api/serializers.py` (modifié)
- `backend/api/urls.py` (modifié)
- `backend/api/migrations/0017_*.py`

## 🎯 Fonctionnalités

✅ Grille visuelle Lundi-Dimanche 8h-18h  
✅ CRUD complet (Créer/Modifier/Supprimer)  
✅ Types de cours (CM/TD/TP) avec couleurs  
✅ Vérification automatique des conflits  
✅ Envoi automatique d'emails  
✅ Design responsive  

## 🧪 Test Rapide

1. Connexion: admin@unierp.bf / Admin2026
2. Menu: Emploi du temps
3. Sélectionner une classe
4. Cliquer sur une cellule
5. Créer un cours
6. Envoyer les emails

## 📚 Documentation Complète

- `EMPLOI_DU_TEMPS_COMPLET_FINAL.md` - Documentation complète
- `DEPLOIEMENT_EMPLOI_DU_TEMPS.md` - Guide de déploiement
- `SPECIFICATION_EMPLOI_DU_TEMPS_VISUEL.md` - Spécifications

## 🆘 Support

En cas de problème:
1. Vérifier la console navigateur (F12)
2. Vérifier les logs PythonAnywhere
3. Consulter `DEPLOIEMENT_EMPLOI_DU_TEMPS.md`

## ✨ Résultat

Interface moderne permettant de créer et gérer les emplois du temps visuellement, avec vérification des conflits et envoi automatique d'emails aux professeurs et étudiants.

---

**Prêt pour production** 🚀
