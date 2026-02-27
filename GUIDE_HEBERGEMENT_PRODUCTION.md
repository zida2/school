# 🌐 GUIDE D'HÉBERGEMENT EN PRODUCTION

Date: 26 février 2026

---

## 🎯 ARCHITECTURE DE DÉPLOIEMENT

```
Frontend (Vercel)  ←→  Backend Django (PythonAnywhere/Railway/Render)
     ↓                           ↓
  HTML/CSS/JS              API REST + Base de données
```

---

## 🚀 OPTIONS D'HÉBERGEMENT BACKEND

### Option 1: PythonAnywhere (RECOMMANDÉ - GRATUIT)

**Avantages:**
- ✅ Gratuit jusqu'à 512 MB
- ✅ Spécialisé pour Django
- ✅ Base de données MySQL incluse
- ✅ Facile à configurer
- ✅ Parfait pour les projets étudiants

**Limites:**
- ⚠️ 100,000 requêtes/jour (gratuit)
- ⚠️ Pas de HTTPS personnalisé (gratuit)

**URL finale:** `https://votre-username.pythonanywhere.com`

---

### Option 2: Railway.app (MODERNE)

**Avantages:**
- ✅ $5 de crédit gratuit/mois
- ✅ Déploiement automatique depuis GitHub
- ✅ Base de données PostgreSQL incluse
- ✅ HTTPS automatique
- ✅ Très moderne et simple

**Limites:**
- ⚠️ Nécessite une carte bancaire (même pour gratuit)
- ⚠️ Crédit limité

**URL finale:** `https://votre-app.up.railway.app`

---

### Option 3: Render.com (POPULAIRE)

**Avantages:**
- ✅ Plan gratuit disponible
- ✅ Déploiement automatique depuis GitHub
- ✅ Base de données PostgreSQL incluse
- ✅ HTTPS automatique
- ✅ Très fiable

**Limites:**
- ⚠️ Le service gratuit s'endort après 15 min d'inactivité
- ⚠️ Redémarrage lent (30-60 secondes)

**URL finale:** `https://votre-app.onrender.com`

---

### Option 4: Heroku (CLASSIQUE - PAYANT)

**Avantages:**
- ✅ Très populaire
- ✅ Documentation excellente
- ✅ Addons nombreux

**Limites:**
- ❌ Plus de plan gratuit depuis 2022
- ❌ $7/mois minimum

---

## 📋 GUIDE DÉTAILLÉ: PYTHONANYWHERE (GRATUIT)

### Étape 1: Créer un Compte

1. Aller sur: https://www.pythonanywhere.com/
2. Cliquer sur "Start running Python online in less than a minute!"
3. Créer un compte gratuit (Beginner)

---

### Étape 2: Préparer le Backend

**Créer un fichier `requirements.txt` dans le dossier `backend`:**

```txt
Django==6.0.2
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
django-filter==23.5
Pillow==10.2.0
python-decouple==3.8
```

**Créer un fichier `.env` pour les variables d'environnement:**

```env
SECRET_KEY=votre-secret-key-super-securisee
DEBUG=False
ALLOWED_HOSTS=votre-username.pythonanywhere.com,localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

---

### Étape 3: Modifier `settings.py`

**Ajouter en haut du fichier:**

```python
from decouple import config
import os

# Security
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

---

### Étape 4: Déployer sur PythonAnywhere

**Dans le terminal PythonAnywhere (Bash console):**

```bash
# 1. Cloner votre repo
git clone https://github.com/votre-username/school.git
cd school/backend

# 2. Créer un environnement virtuel
mkvirtualenv --python=/usr/bin/python3.10 myenv

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 5. Appliquer les migrations
python manage.py migrate

# 6. Créer un superuser
python manage.py createsuperuser
```

---

### Étape 5: Configurer l'Application Web

1. Aller dans l'onglet "Web"
2. Cliquer sur "Add a new web app"
3. Choisir "Manual configuration"
4. Choisir "Python 3.10"

**Configurer le WSGI file:**

```python
import os
import sys

# Ajouter le chemin de votre projet
path = '/home/votre-username/school/backend'
if path not in sys.path:
    sys.path.append(path)

# Configurer Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_backend.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Configurer les fichiers statiques:**

- URL: `/static/`
- Directory: `/home/votre-username/school/backend/staticfiles/`

**Configurer les fichiers media:**

- URL: `/media/`
- Directory: `/home/votre-username/school/backend/media/`

---

### Étape 6: Configurer CORS

**Dans `backend/erp_backend/settings.py`:**

```python
CORS_ALLOWED_ORIGINS = [
    'https://votre-app.vercel.app',
    'http://localhost:8080',
    'http://127.0.0.1:8080',
]

CORS_ALLOW_CREDENTIALS = True
```

---

### Étape 7: Recharger l'Application

Dans l'onglet "Web", cliquer sur le bouton vert "Reload".

**Votre backend est maintenant en ligne!** 🎉

URL: `https://votre-username.pythonanywhere.com`

---

## 🌐 DÉPLOYER LE FRONTEND SUR VERCEL

### Étape 1: Préparer le Frontend

**Modifier `js/api.js` pour utiliser l'URL de production:**

```javascript
// Configuration de l'API
const API_BASE = process.env.NODE_ENV === 'production' 
    ? 'https://votre-username.pythonanywhere.com/api'
    : 'http://localhost:8000/api';
```

**Ou créer un fichier `config.js`:**

```javascript
const CONFIG = {
    API_URL: 'https://votre-username.pythonanywhere.com/api'
};
```

Et modifier `api.js`:

```javascript
const API_BASE = CONFIG.API_URL || 'http://localhost:8000/api';
```

---

### Étape 2: Créer un fichier `vercel.json`

**À la racine du projet:**

```json
{
  "version": 2,
  "builds": [
    {
      "src": "*.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
```

---

### Étape 3: Déployer sur Vercel

**Méthode 1: Via le site web**

1. Aller sur: https://vercel.com/
2. Se connecter avec GitHub
3. Cliquer sur "New Project"
4. Sélectionner votre repo `school`
5. Configurer:
   - Framework Preset: Other
   - Root Directory: `./` (racine)
   - Build Command: (laisser vide)
   - Output Directory: `./` (racine)
6. Cliquer sur "Deploy"

**Méthode 2: Via CLI**

```bash
# Installer Vercel CLI
npm install -g vercel

# Se connecter
vercel login

# Déployer
vercel
```

---

## 🔗 CONNECTER FRONTEND ET BACKEND

### Étape 1: Mettre à Jour l'URL de l'API

**Dans `js/api.js`:**

```javascript
const API_BASE = 'https://votre-username.pythonanywhere.com/api';
```

---

### Étape 2: Configurer CORS sur le Backend

**Dans `backend/erp_backend/settings.py`:**

```python
CORS_ALLOWED_ORIGINS = [
    'https://votre-app.vercel.app',
    'https://votre-app-git-main-username.vercel.app',
    'http://localhost:8080',
]
```

---

### Étape 3: Tester la Connexion

1. Ouvrir: `https://votre-app.vercel.app`
2. Essayer de se connecter
3. Vérifier dans la console (F12) qu'il n'y a pas d'erreur CORS

---

## 📋 GUIDE RAPIDE: RAILWAY.APP

### Étape 1: Créer un Compte

1. Aller sur: https://railway.app/
2. Se connecter avec GitHub

---

### Étape 2: Créer un Nouveau Projet

1. Cliquer sur "New Project"
2. Choisir "Deploy from GitHub repo"
3. Sélectionner votre repo `school`

---

### Étape 3: Configurer le Service

**Ajouter les variables d'environnement:**

```
SECRET_KEY=votre-secret-key
DEBUG=False
ALLOWED_HOSTS=*.up.railway.app
DATABASE_URL=postgresql://... (fourni automatiquement)
```

**Ajouter un fichier `railway.json` dans `backend`:**

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
  },
  "deploy": {
    "startCommand": "gunicorn erp_backend.wsgi:application --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Ajouter `gunicorn` dans `requirements.txt`:**

```txt
gunicorn==21.2.0
```

---

### Étape 4: Déployer

Railway déploie automatiquement à chaque push sur GitHub!

**URL finale:** `https://votre-app.up.railway.app`

---

## 🎯 RÉSUMÉ DES COÛTS

| Service | Plan Gratuit | Limites | Recommandation |
|---------|--------------|---------|----------------|
| **PythonAnywhere** | ✅ Oui | 512 MB, 100k req/jour | ⭐ Meilleur pour débuter |
| **Railway** | ✅ $5/mois | Crédit limité | ⭐ Meilleur pour production |
| **Render** | ✅ Oui | S'endort après 15 min | ⭐ Bon compromis |
| **Heroku** | ❌ Non | $7/mois minimum | ⚠️ Payant uniquement |
| **Vercel** (Frontend) | ✅ Oui | Illimité | ⭐ Parfait pour frontend |

---

## 🔧 CHECKLIST DE DÉPLOIEMENT

### Backend

- [ ] Créer `requirements.txt`
- [ ] Configurer les variables d'environnement
- [ ] Modifier `settings.py` pour la production
- [ ] Configurer CORS avec l'URL Vercel
- [ ] Collecter les fichiers statiques
- [ ] Appliquer les migrations
- [ ] Créer un superuser
- [ ] Tester l'API en production

### Frontend

- [ ] Mettre à jour l'URL de l'API dans `api.js`
- [ ] Créer `vercel.json`
- [ ] Tester en local avec l'API de production
- [ ] Déployer sur Vercel
- [ ] Tester la connexion en production

---

## 💡 CONSEILS

### Pour le Développement

Utilisez des variables d'environnement pour basculer entre dev et prod:

```javascript
const API_BASE = window.location.hostname === 'localhost'
    ? 'http://localhost:8000/api'
    : 'https://votre-username.pythonanywhere.com/api';
```

---

### Pour la Sécurité

1. **Ne jamais commiter** les secrets (SECRET_KEY, mots de passe)
2. **Utiliser HTTPS** en production
3. **Configurer CORS** correctement
4. **Désactiver DEBUG** en production
5. **Utiliser des mots de passe forts**

---

### Pour la Performance

1. **Activer le cache** Django
2. **Optimiser les requêtes** SQL
3. **Compresser les fichiers** statiques
4. **Utiliser un CDN** pour les assets

---

## 📚 RESSOURCES

### Documentation

- **PythonAnywhere:** https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
- **Railway:** https://docs.railway.app/
- **Render:** https://render.com/docs/deploy-django
- **Vercel:** https://vercel.com/docs

### Tutoriels

- **Django Deployment Checklist:** https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
- **CORS Configuration:** https://github.com/adamchainz/django-cors-headers

---

## 🎉 RÉSULTAT FINAL

Après le déploiement:

- **Frontend:** `https://votre-app.vercel.app`
- **Backend:** `https://votre-username.pythonanywhere.com`
- **Admin Django:** `https://votre-username.pythonanywhere.com/admin/`

**Votre application est maintenant accessible partout dans le monde!** 🌍

---

Date: 26 février 2026
Version: 1.0
Statut: ✅ GUIDE COMPLET

**Recommandation: Commencez avec PythonAnywhere (gratuit) pour le backend et Vercel pour le frontend!** 🚀

