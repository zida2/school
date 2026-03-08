# Guide de Vérification Backend PythonAnywhere

## 🔍 DIAGNOSTIC

### 1. Vérifier que l'application web est active

1. Va sur https://www.pythonanywhere.com/
2. Connecte-toi avec ton compte
3. Va dans l'onglet **"Web"**
4. Cherche ton application: **wendlasida.pythonanywhere.com**
5. Vérifie que le statut est **"Enabled"** (vert)
6. Si c'est **"Disabled"** (rouge), clique sur **"Enable"**

### 2. Vérifier les logs d'erreur

Dans l'onglet **"Web"**, section **"Log files"**:

1. **Error log**: Clique sur le lien pour voir les erreurs
2. **Server log**: Clique pour voir les requêtes
3. **Access log**: Clique pour voir les accès

Cherche des erreurs récentes (dernières lignes du fichier).

### 3. Redémarrer l'application

Dans l'onglet **"Web"**:
1. Clique sur le gros bouton vert **"Reload wendlasida.pythonanywhere.com"**
2. Attends 10-20 secondes
3. Teste l'URL: https://wendlasida.pythonanywhere.com/api/

## 🔧 PROBLÈMES COURANTS

### Problème 1: Application désactivée
**Symptôme**: Site inaccessible
**Solution**: Clique sur "Enable" dans l'onglet Web

### Problème 2: Erreur de base de données
**Symptôme**: Erreur 500, logs montrent "database locked" ou "no such table"
**Solution**: 
```bash
# Dans la console Bash PythonAnywhere
cd ~/wendlasida.pythonanywhere.com
source venv/bin/activate
python manage.py migrate
```

### Problème 3: Dépendances manquantes
**Symptôme**: ImportError dans les logs
**Solution**:
```bash
cd ~/wendlasida.pythonanywhere.com
source venv/bin/activate
pip install -r requirements.txt
```

### Problème 4: Fichier WSGI incorrect
**Symptôme**: Application ne démarre pas
**Solution**: Vérifier le fichier WSGI dans l'onglet Web → "Code" → "WSGI configuration file"

Contenu attendu:
```python
import os
import sys

path = '/home/wendlasida/wendlasida.pythonanywhere.com'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_backend.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Problème 5: Variables d'environnement manquantes
**Symptôme**: Erreur de configuration
**Solution**: Créer/vérifier le fichier `.env` dans le dossier du projet

Contenu minimal:
```
SECRET_KEY=votre-cle-secrete-django
DEBUG=True
ALLOWED_HOSTS=wendlasida.pythonanywhere.com
```

## 🧪 TESTER L'API

### Test 1: Page d'accueil API
Ouvre dans le navigateur:
```
https://wendlasida.pythonanywhere.com/api/
```
**Attendu**: Page JSON avec liste des endpoints

### Test 2: Endpoint de login
Ouvre dans le navigateur:
```
https://wendlasida.pythonanywhere.com/api/auth/login/
```
**Attendu**: Page de formulaire ou erreur 405 (Method Not Allowed) - c'est normal, ça veut dire que l'endpoint existe

### Test 3: Test avec curl (dans la console PythonAnywhere)
```bash
curl https://wendlasida.pythonanywhere.com/api/
```
**Attendu**: Réponse JSON

## 📝 CHECKLIST DE VÉRIFICATION

- [ ] Application web "Enabled" dans l'onglet Web
- [ ] Pas d'erreurs dans Error log
- [ ] URL https://wendlasida.pythonanywhere.com/api/ accessible
- [ ] Base de données existe (db.sqlite3 dans le dossier)
- [ ] Migrations appliquées
- [ ] Dépendances installées (requirements.txt)
- [ ] Fichier WSGI correct
- [ ] Variables d'environnement configurées

## 🚀 PROCÉDURE DE REDÉMARRAGE COMPLÈTE

Si rien ne fonctionne, procédure complète:

### 1. Console Bash PythonAnywhere
```bash
# Aller dans le dossier
cd ~/wendlasida.pythonanywhere.com

# Activer l'environnement virtuel
source venv/bin/activate

# Vérifier les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un superuser si nécessaire
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
```

### 2. Onglet Web
- Clique sur **"Reload wendlasida.pythonanywhere.com"**

### 3. Tester
- Ouvre https://wendlasida.pythonanywhere.com/api/

## 📞 SI ÇA NE MARCHE TOUJOURS PAS

### Vérifier la structure des dossiers
```bash
cd ~/wendlasida.pythonanywhere.com
ls -la
```

Doit contenir:
- `manage.py`
- `erp_backend/` (dossier)
- `api/` (dossier)
- `db.sqlite3` (fichier)
- `venv/` (dossier)
- `requirements.txt`

### Vérifier que Django fonctionne
```bash
cd ~/wendlasida.pythonanywhere.com
source venv/bin/activate
python manage.py check
```

Doit afficher: "System check identified no issues"

### Tester le serveur localement
```bash
python manage.py runserver
```

Si ça fonctionne localement mais pas sur le web, c'est un problème de configuration WSGI.

## 🔗 LIENS UTILES

- Dashboard PythonAnywhere: https://www.pythonanywhere.com/user/wendlasida/
- Documentation PythonAnywhere Django: https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
- Forum PythonAnywhere: https://www.pythonanywhere.com/forums/

## 📧 SUPPORT

Si le problème persiste:
1. Copie les dernières lignes du Error log
2. Copie le résultat de `python manage.py check`
3. Vérifie que l'URL du backend dans le frontend est correcte: `https://wendlasida.pythonanywhere.com/api`
