# 🚀 Guide de Déploiement - ERP Universitaire BF

## 📋 Prérequis

- Compte GitHub (✅ Fait)
- Compte Vercel (gratuit)
- Backend Django hébergé (Railway, Render, ou PythonAnywhere)

## 🌐 Déploiement Frontend sur Vercel

### Étape 1: Connexion à Vercel
1. Aller sur https://vercel.com
2. Se connecter avec GitHub
3. Autoriser Vercel à accéder à vos repositories

### Étape 2: Importer le Projet
1. Cliquer sur "Add New Project"
2. Sélectionner le repository `zida2/school`
3. Cliquer sur "Import"

### Étape 3: Configuration
- **Framework Preset**: Other
- **Root Directory**: ./
- **Build Command**: (laisser vide)
- **Output Directory**: (laisser vide)

### Étape 4: Variables d'Environnement
Ajouter dans les Environment Variables:
```
API_URL=https://votre-backend.railway.app/api
```

### Étape 5: Déployer
1. Cliquer sur "Deploy"
2. Attendre 1-2 minutes
3. Votre site sera disponible sur: `https://school-xxx.vercel.app`

## 🐍 Déploiement Backend sur Railway

### Étape 1: Créer un compte Railway
1. Aller sur https://railway.app
2. Se connecter avec GitHub

### Étape 2: Créer un nouveau projet
1. Cliquer sur "New Project"
2. Sélectionner "Deploy from GitHub repo"
3. Choisir `zida2/school`

### Étape 3: Configuration
1. Ajouter un fichier `Procfile` dans le dossier backend:
```
web: cd backend && python manage.py migrate && gunicorn erp_backend.wsgi
```

2. Ajouter un fichier `runtime.txt`:
```
python-3.11.0
```

3. Ajouter un fichier `requirements.txt`:
```
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### Étape 4: Variables d'Environnement Railway
```
DJANGO_SETTINGS_MODULE=erp_backend.settings
ALLOWED_HOSTS=.railway.app
DEBUG=False
SECRET_KEY=votre-secret-key-super-securisee
```

### Étape 5: Déployer
Railway déploiera automatiquement. URL: `https://school-production-xxx.up.railway.app`

## 🔧 Configuration Post-Déploiement

### 1. Mettre à jour l'URL de l'API dans le Frontend
Dans `js/api.js`, ligne 5:
```javascript
const API_BASE = 'https://school-production-xxx.up.railway.app/api';
```

### 2. Configurer CORS dans Django
Dans `backend/erp_backend/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "https://school-xxx.vercel.app",
    "http://localhost:3000",
]
```

### 3. Créer les données de test
```bash
railway run python backend/setup.py
```

## ✅ Vérification

### Frontend
- ✅ Page de connexion s'affiche
- ✅ Design premium visible
- ✅ Pas d'erreurs dans la console

### Backend
- ✅ API accessible: `https://votre-backend.railway.app/api/`
- ✅ Login fonctionne
- ✅ Données de test créées

### Connexion
- ✅ Se connecter avec `admin@uan.bf` / `admin123`
- ✅ Dashboard s'affiche correctement
- ✅ Navigation fonctionne

## 🎯 Checklist Démonstration Client

### Avant la démo
- [ ] Backend déployé et fonctionnel
- [ ] Frontend déployé sur Vercel
- [ ] Données de test créées
- [ ] Tous les comptes de test fonctionnent
- [ ] Tester sur mobile et desktop

### Comptes de démonstration
```
Admin: admin@uan.bf / admin123
Enseignant: j.ouedraogo@uan.bf / enseignant123
Étudiant: m.diallo@etu.bf / etudiant123
```

### Fonctionnalités à démontrer

#### 1. Espace Admin (5 min)
- ✅ Dashboard avec statistiques
- ✅ Gestion des étudiants (ajouter, modifier)
- ✅ Gestion des enseignants (4 grades)
- ✅ Détails complets d'un étudiant
- ✅ Gestion des filières et matières
- ✅ Suivi des paiements

#### 2. Espace Enseignant (5 min)
- ✅ Dashboard personnalisé
- ✅ Créer une évaluation (devoir, TP, examen)
- ✅ Saisir des notes
- ✅ Gérer les absences
- ✅ Liste des étudiants
- ✅ Publier des supports de cours

#### 3. Espace Étudiant (3 min)
- ✅ Consulter ses notes
- ✅ Voir le bulletin
- ✅ Suivi des paiements
- ✅ Télécharger les supports

### Points forts à mettre en avant
1. 🎨 **Design ultra premium** - Interface moderne et professionnelle
2. 📊 **Statistiques en temps réel** - Tableaux de bord dynamiques
3. 📝 **Système d'évaluations flexible** - Devoirs, TP, projets, examens
4. 💰 **Gestion financière complète** - Suivi des paiements et relances
5. 🔐 **Sécurité** - Authentification JWT, permissions par rôle
6. 📱 **Responsive** - Fonctionne sur tous les appareils
7. ⚡ **Performance** - Chargement rapide, animations fluides

## 🐛 Dépannage

### Erreur CORS
```python
# Dans settings.py
CORS_ALLOW_ALL_ORIGINS = True  # Pour le développement uniquement
```

### Erreur 404 sur l'API
Vérifier que `API_BASE` dans `js/api.js` pointe vers le bon URL

### Base de données vide
```bash
railway run python backend/setup.py
```

### Erreur de migration
```bash
railway run python backend/manage.py migrate
```

## 📞 Support

En cas de problème:
1. Vérifier les logs Railway: `railway logs`
2. Vérifier la console du navigateur (F12)
3. Tester l'API directement: `https://votre-backend.railway.app/api/`

## 🎉 Félicitations!

Votre ERP Universitaire est maintenant déployé et prêt pour la démonstration!

URL Frontend: `https://school-xxx.vercel.app`
URL Backend: `https://school-production-xxx.up.railway.app`

---

**Dernière mise à jour**: Février 2026
