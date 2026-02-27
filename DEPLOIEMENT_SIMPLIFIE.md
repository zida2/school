# 🚀 DÉPLOIEMENT PYTHONANYWHERE - VERSION SIMPLIFIÉE

**Date:** 27 février 2026

---

## ✅ ÉTAPE 1: CONSOLE BASH (5 minutes)

1. **Ouvre ton dashboard PythonAnywhere**
2. **Clique sur "Consoles"** → **"Bash"**
3. **Copie-colle ces commandes UNE PAR UNE:**

```bash
# 1. Cloner le projet
git clone https://github.com/zida2/school.git

# 2. Aller dans le dossier backend
cd school/backend

# 3. Créer l'environnement virtuel
mkvirtualenv --python=/usr/bin/python3.10 myenv

# 4. Installer les dépendances (attendre 2-3 minutes)
pip install -r requirements.txt

# 5. Configurer la base de données
python manage.py migrate

# 6. Créer le compte admin
python manage.py createsuperuser
```

**Pour le superuser, entre:**
- Username: `admin`
- Email: `admin@uan.bf`
- Password: `admin123` (tape 2 fois)
- Si demandé, tape `y` pour confirmer

```bash
# 7. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 8. Créer les données de test
python creer_donnees_moussa.py
```

✅ **Si tout s'est bien passé, continue à l'étape 2!**

---

## ✅ ÉTAPE 2: CRÉER L'APPLICATION WEB (2 minutes)

1. **Retourne au dashboard PythonAnywhere**
2. **Clique sur "Web"**
3. **Clique sur "Add a new web app"**
4. **Clique sur "Next"**
5. **Choisis "Manual configuration"**
6. **Choisis "Python 3.10"**
7. **Clique sur "Next"**

✅ **Ton application web est créée!**

---

## ✅ ÉTAPE 3: CONFIGURER LE FICHIER WSGI (3 minutes)

1. **Sur la page Web**, trouve la section **"Code"**
2. **Clique sur le lien "WSGI configuration file"**
3. **SUPPRIME TOUT le contenu du fichier**
4. **Copie-colle ce code:**

```python
import os
import sys

# ⚠️ REMPLACE "VOTRE_USERNAME" par ton nom d'utilisateur PythonAnywhere
path = '/home/VOTRE_USERNAME/school/backend'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_backend.settings'

# ⚠️ REMPLACE "VOTRE_USERNAME" ici aussi
activate_this = '/home/VOTRE_USERNAME/.virtualenvs/myenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. **Clique sur "Save"**

---

## ✅ ÉTAPE 4: CONFIGURER L'ENVIRONNEMENT VIRTUEL (1 minute)

1. **Retourne à l'onglet "Web"**
2. **Trouve la section "Virtualenv"**
3. **Clique sur "Enter path to a virtualenv"**
4. **Entre:** `/home/VOTRE_USERNAME/.virtualenvs/myenv`
5. **Clique sur la coche ✓**

---

## ✅ ÉTAPE 5: CONFIGURER LES FICHIERS STATIQUES (2 minutes)

1. **Trouve la section "Static files"**
2. **Ajoute ces 2 entrées:**

**Entrée 1:**
- URL: `/static/`
- Directory: `/home/VOTRE_USERNAME/school/backend/staticfiles/`

**Entrée 2:**
- URL: `/media/`
- Directory: `/home/VOTRE_USERNAME/school/backend/media/`

---

## ✅ ÉTAPE 6: CONFIGURER ALLOWED_HOSTS (2 minutes)

1. **Retourne à la console Bash**
2. **Copie-colle ces commandes:**

```bash
cd ~/school/backend/erp_backend
nano settings.py
```

3. **Trouve la ligne** `ALLOWED_HOSTS = [...]` (utilise les flèches pour descendre)
4. **Modifie-la pour:**

```python
ALLOWED_HOSTS = ['VOTRE_USERNAME.pythonanywhere.com', 'localhost', '127.0.0.1']
```

5. **Sauvegarde:**
   - Appuie sur `CTRL + X`
   - Tape `Y`
   - Appuie sur `Entrée`

---

## ✅ ÉTAPE 7: RECHARGER L'APPLICATION (30 secondes)

1. **Retourne à l'onglet "Web"**
2. **Clique sur le gros bouton vert "Reload"**
3. **Attends 10 secondes**

---

## ✅ ÉTAPE 8: TESTER TON BACKEND (1 minute)

**Ouvre dans ton navigateur:**

```
https://VOTRE_USERNAME.pythonanywhere.com/api/auth/me/
```

**Tu devrais voir:**
```json
{"detail": "Authentication credentials were not provided."}
```

✅ **Si tu vois ce message, TON BACKEND FONCTIONNE!** 🎉

**Teste aussi l'admin:**

```
https://VOTRE_USERNAME.pythonanywhere.com/admin/
```

**Connecte-toi avec:**
- Username: `admin`
- Password: `admin123`

✅ **Si tu peux te connecter, PARFAIT!**

---

## ✅ ÉTAPE 9: CONFIGURER LE FRONTEND (2 minutes)

**Sur ton ordinateur, ouvre le fichier `js/config.js` et modifie:**

```javascript
const CONFIG = {
    // Remplace VOTRE_USERNAME par ton nom d'utilisateur PythonAnywhere
    API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000/api'
        : 'https://VOTRE_USERNAME.pythonanywhere.com/api',
    
    USE_MOCK: false
};
```

**Sauvegarde le fichier!**

---

## ✅ ÉTAPE 10: DÉPLOYER SUR VERCEL (3 minutes)

1. **Va sur:** https://vercel.com/
2. **Connecte-toi avec GitHub**
3. **Clique sur "New Project"**
4. **Sélectionne ton repo "school"**
5. **Configure:**
   - Framework Preset: **Other**
   - Root Directory: `./`
   - Build Command: (laisse vide)
   - Output Directory: `./`
6. **Clique sur "Deploy"**
7. **Attends 1-2 minutes**

✅ **Ton frontend est en ligne!**

---

## ✅ ÉTAPE 11: CONFIGURER CORS (2 minutes)

1. **Retourne à la console Bash PythonAnywhere**
2. **Copie-colle:**

```bash
cd ~/school/backend/erp_backend
nano settings.py
```

3. **Trouve** `CORS_ALLOWED_ORIGINS` (descends avec les flèches)
4. **Modifie pour:**

```python
CORS_ALLOWED_ORIGINS = [
    'https://votre-app.vercel.app',  # Remplace par ton URL Vercel
    'http://localhost:8080',
    'http://127.0.0.1:8080',
]
```

5. **Sauvegarde** (CTRL+X, Y, Entrée)

6. **Retourne à l'onglet "Web"**
7. **Clique sur "Reload"**

---

## ✅ ÉTAPE 12: TESTER EN PRODUCTION (1 minute)

**Ouvre ton app Vercel:**

```
https://votre-app.vercel.app
```

**Connecte-toi avec:**
- Email: `m.diallo@etu.bf`
- Password: `etudiant123`

✅ **SI ÇA FONCTIONNE, FÉLICITATIONS! TON APP EST EN LIGNE!** 🎉🎉🎉

---

## 🐛 PROBLÈMES?

### Le backend ne fonctionne pas

1. **Vérifie les logs:**
   - Onglet "Web" → "Error log"
2. **Recharge l'application:**
   - Bouton vert "Reload"

### Erreur CORS

1. **Vérifie** `CORS_ALLOWED_ORIGINS` dans `settings.py`
2. **Ajoute** ton URL Vercel
3. **Recharge** l'application

### Page blanche sur Vercel

1. **Vérifie** que `js/config.js` a la bonne URL PythonAnywhere
2. **Redéploie** sur Vercel

---

## 📞 AIDE RAPIDE

**N'oublie pas de remplacer `VOTRE_USERNAME` partout par ton vrai nom d'utilisateur PythonAnywhere!**

**Temps total estimé: 20-25 minutes**

---

Date: 27 février 2026
Version: 2.0 - SIMPLIFIÉE
Statut: ✅ PRÊT À DÉPLOYER
