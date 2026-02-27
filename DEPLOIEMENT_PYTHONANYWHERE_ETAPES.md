# 🚀 DÉPLOIEMENT SUR PYTHONANYWHERE - ÉTAPES DÉTAILLÉES

Date: 26 février 2026

---

## ✅ VOUS AVEZ CRÉÉ VOTRE COMPTE - PARFAIT!

Maintenant suivez ces étapes exactement:

---

## 📋 ÉTAPE 1: OUVRIR UNE CONSOLE BASH

1. **Sur le dashboard PythonAnywhere**, cliquez sur l'onglet **"Consoles"**
2. Cliquez sur **"Bash"** (sous "Start a new console")
3. Une console noire va s'ouvrir

---

## 📋 ÉTAPE 2: CLONER VOTRE PROJET GITHUB

**Dans la console Bash, tapez ces commandes une par une:**

```bash
# 1. Cloner votre repo
git clone https://github.com/zida2/school.git

# 2. Aller dans le dossier backend
cd school/backend

# 3. Vérifier que vous êtes au bon endroit
ls
```

**Vous devriez voir:** `manage.py`, `api/`, `erp_backend/`, etc.

---

## 📋 ÉTAPE 3: CRÉER UN ENVIRONNEMENT VIRTUEL

**Toujours dans la console Bash:**

```bash
# 1. Créer l'environnement virtuel
mkvirtualenv --python=/usr/bin/python3.10 myenv

# 2. Vérifier qu'il est activé (vous devriez voir (myenv) au début de la ligne)
```

---

## 📋 ÉTAPE 4: INSTALLER LES DÉPENDANCES

```bash
# Installer toutes les dépendances
pip install -r requirements.txt
```

**Attendez que tout s'installe** (2-3 minutes)

---

## 📋 ÉTAPE 5: CONFIGURER LA BASE DE DONNÉES

```bash
# 1. Appliquer les migrations
python manage.py migrate

# 2. Créer un superuser (admin)
python manage.py createsuperuser
```

**Pour le superuser, entrez:**
- Username: `admin`
- Email: `admin@uan.bf`
- Password: `admin123` (tapez 2 fois)
- Confirmez avec `y` si demandé

---

## 📋 ÉTAPE 6: COLLECTER LES FICHIERS STATIQUES

```bash
python manage.py collectstatic --noinput
```

---

## 📋 ÉTAPE 7: CRÉER LES DONNÉES DE TEST

```bash
# Créer les données de test (étudiants, enseignants, etc.)
python creer_donnees_moussa.py
```

---

## 📋 ÉTAPE 8: CONFIGURER L'APPLICATION WEB

1. **Retournez au dashboard PythonAnywhere**
2. Cliquez sur l'onglet **"Web"**
3. Cliquez sur **"Add a new web app"**
4. Cliquez sur **"Next"**
5. Choisissez **"Manual configuration"**
6. Choisissez **"Python 3.10"**
7. Cliquez sur **"Next"**

---

## 📋 ÉTAPE 9: CONFIGURER LE FICHIER WSGI

1. **Sur la page Web**, trouvez la section **"Code"**
2. Cliquez sur le lien **"WSGI configuration file"** (quelque chose comme `/var/www/votre_username_pythonanywhere_com_wsgi.py`)
3. **Supprimez TOUT le contenu** du fichier
4. **Copiez-collez ce code:**

```python
import os
import sys

# Ajouter le chemin de votre projet
path = '/home/VOTRE_USERNAME/school/backend'
if path not in sys.path:
    sys.path.append(path)

# Configurer Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_backend.settings'

# Activer l'environnement virtuel
activate_this = '/home/VOTRE_USERNAME/.virtualenvs/myenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ IMPORTANT:** Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur PythonAnywhere (2 fois!)

5. Cliquez sur **"Save"** (en haut à droite)

---

## 📋 ÉTAPE 10: CONFIGURER L'ENVIRONNEMENT VIRTUEL

1. **Retournez à l'onglet "Web"**
2. Trouvez la section **"Virtualenv"**
3. Cliquez sur **"Enter path to a virtualenv"**
4. Entrez: `/home/VOTRE_USERNAME/.virtualenvs/myenv`
5. Cliquez sur la coche ✓

---

## 📋 ÉTAPE 11: CONFIGURER LES FICHIERS STATIQUES

1. **Toujours sur l'onglet "Web"**
2. Trouvez la section **"Static files"**
3. Ajoutez ces 2 entrées:

**Entrée 1:**
- URL: `/static/`
- Directory: `/home/VOTRE_USERNAME/school/backend/staticfiles/`

**Entrée 2:**
- URL: `/media/`
- Directory: `/home/VOTRE_USERNAME/school/backend/media/`

---

## 📋 ÉTAPE 12: CONFIGURER ALLOWED_HOSTS

1. **Retournez à la console Bash**
2. Tapez:

```bash
cd ~/school/backend/erp_backend
nano settings.py
```

3. **Trouvez la ligne** `ALLOWED_HOSTS = [...]`
4. **Modifiez-la** pour:

```python
ALLOWED_HOSTS = ['VOTRE_USERNAME.pythonanywhere.com', 'localhost', '127.0.0.1']
```

5. **Sauvegardez:**
   - Appuyez sur `CTRL + X`
   - Tapez `Y`
   - Appuyez sur `Entrée`

---

## 📋 ÉTAPE 13: RECHARGER L'APPLICATION

1. **Retournez à l'onglet "Web"**
2. Cliquez sur le gros bouton vert **"Reload VOTRE_USERNAME.pythonanywhere.com"**
3. **Attendez 5-10 secondes**

---

## 📋 ÉTAPE 14: TESTER VOTRE BACKEND

**Ouvrez dans votre navigateur:**

```
https://VOTRE_USERNAME.pythonanywhere.com/api/auth/me/
```

**Vous devriez voir:**
```json
{"detail": "Authentication credentials were not provided."}
```

✅ **Si vous voyez ce message, BRAVO! Votre backend fonctionne!**

---

## 📋 ÉTAPE 15: TESTER L'ADMIN DJANGO

**Ouvrez:**

```
https://VOTRE_USERNAME.pythonanywhere.com/admin/
```

**Connectez-vous avec:**
- Username: `admin`
- Password: `admin123`

✅ **Si vous pouvez vous connecter, PARFAIT!**

---

## 📋 ÉTAPE 16: CONFIGURER LE FRONTEND

**Maintenant, modifiez `js/config.js` sur votre ordinateur:**

```javascript
API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api'
    : 'https://VOTRE_USERNAME.pythonanywhere.com/api',
```

**Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur PythonAnywhere!**

---

## 📋 ÉTAPE 17: DÉPLOYER LE FRONTEND SUR VERCEL

1. **Allez sur:** https://vercel.com/
2. **Connectez-vous** avec GitHub
3. **Cliquez sur** "New Project"
4. **Sélectionnez** votre repo `school`
5. **Configurez:**
   - Framework Preset: **Other**
   - Root Directory: `./` (racine)
   - Build Command: (laisser vide)
   - Output Directory: `./` (racine)
6. **Cliquez sur** "Deploy"
7. **Attendez** 1-2 minutes

---

## 📋 ÉTAPE 18: CONFIGURER CORS

**Retournez à la console Bash PythonAnywhere:**

```bash
cd ~/school/backend/erp_backend
nano settings.py
```

**Trouvez** `CORS_ALLOWED_ORIGINS` et **modifiez:**

```python
CORS_ALLOWED_ORIGINS = [
    'https://votre-app.vercel.app',  # Remplacez par votre URL Vercel
    'http://localhost:8080',
    'http://127.0.0.1:8080',
]
```

**Sauvegardez** (CTRL+X, Y, Entrée)

**Rechargez l'application** (bouton vert sur l'onglet Web)

---

## 📋 ÉTAPE 19: TESTER EN PRODUCTION

**Ouvrez votre app Vercel:**

```
https://votre-app.vercel.app
```

**Essayez de vous connecter avec:**
- Email: `m.diallo@etu.bf`
- Password: `etudiant123`

✅ **Si ça fonctionne, FÉLICITATIONS! Votre app est en ligne!** 🎉

---

## 🐛 PROBLÈMES COURANTS

### Problème 1: "ImportError: No module named..."

**Solution:**
```bash
workon myenv
pip install -r requirements.txt
```

---

### Problème 2: "DisallowedHost"

**Solution:** Vérifiez `ALLOWED_HOSTS` dans `settings.py`

---

### Problème 3: "CORS error"

**Solution:** Vérifiez `CORS_ALLOWED_ORIGINS` dans `settings.py`

---

### Problème 4: Page blanche

**Solution:** 
1. Vérifiez les logs dans l'onglet "Web" → "Error log"
2. Rechargez l'application (bouton vert)

---

## 📞 AIDE RAPIDE

**Si vous êtes bloqué, vérifiez:**

1. **Console Bash:** Les commandes se sont-elles exécutées sans erreur?
2. **Onglet Web:** L'application est-elle rechargée?
3. **Error log:** Y a-t-il des erreurs? (onglet Web → Error log)
4. **WSGI file:** Avez-vous bien remplacé `VOTRE_USERNAME`?

---

## ✅ CHECKLIST COMPLÈTE

- [ ] Compte PythonAnywhere créé
- [ ] Console Bash ouverte
- [ ] Projet cloné depuis GitHub
- [ ] Environnement virtuel créé
- [ ] Dépendances installées
- [ ] Migrations appliquées
- [ ] Superuser créé
- [ ] Fichiers statiques collectés
- [ ] Données de test créées
- [ ] Application web créée
- [ ] Fichier WSGI configuré
- [ ] Environnement virtuel configuré
- [ ] Fichiers statiques configurés
- [ ] ALLOWED_HOSTS configuré
- [ ] Application rechargée
- [ ] Backend testé (API fonctionne)
- [ ] Admin Django testé
- [ ] Frontend configuré (config.js)
- [ ] Frontend déployé sur Vercel
- [ ] CORS configuré
- [ ] Application testée en production

---

Date: 26 février 2026
Version: 1.0
Statut: ✅ GUIDE COMPLET ÉTAPE PAR ÉTAPE

**Suivez ces étapes dans l'ordre et votre application sera en ligne!** 🚀

