# 🚀 Instructions de Déploiement Complet

## ✅ Ce qui est déjà fait
- Code sur GitHub: https://github.com/zida2/school
- Configuration Vercel prête
- Fichiers de déploiement créés

## 📝 À FAIRE MAINTENANT

### ÉTAPE 1: Déployer le Backend (15 min)

#### Option A: PythonAnywhere (RECOMMANDÉ - Gratuit)

1. Créer un compte sur https://www.pythonanywhere.com
2. Ouvrir une console Bash
3. Exécuter:
```bash
git clone https://github.com/zida2/school.git
cd school/backend
pip3 install --user django djangorestframework django-cors-headers
python3 manage.py migrate
python3 setup.py
```

4. Créer une Web App:
   - Web → Add new web app
   - Manual configuration → Python 3.10
   - Source code: `/home/VOTRENOM/school/backend`
   
5. Éditer le fichier WSGI (lien dans Web tab):
```python
import sys
import os

path = '/home/VOTRENOM/school/backend'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_backend.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. Dans settings.py, ajouter:
```python
ALLOWED_HOSTS = ['VOTRENOM.pythonanywhere.com', 'localhost']
CORS_ALLOWED_ORIGINS = [
    'https://school-xxx.vercel.app',
    'http://localhost:3000',
]
```

7. Recharger l'app (bouton vert "Reload")

**URL Backend**: `https://VOTRENOM.pythonanywhere.com`

#### Option B: Railway (Nécessite carte bancaire)

1. Aller sur https://railway.app
2. Se connecter avec GitHub
3. New Project → Deploy from GitHub
4. Sélectionner zida2/school
5. Ajouter variables d'environnement
6. Railway déploie automatiquement

### ÉTAPE 2: Mettre à jour l'URL de l'API

Dans `js/api.js`, ligne 5, remplacer:
```javascript
const API_BASE = 'https://VOTRENOM.pythonanywhere.com/api';
```

Puis:
```bash
git add js/api.js
git commit -m "Update: API URL production"
git push origin main
```

### ÉTAPE 3: Déployer le Frontend sur Vercel (5 min)

1. Aller sur https://vercel.com
2. Se connecter avec GitHub
3. Import Project → zida2/school
4. Deploy (laisser les paramètres par défaut)

**URL Frontend**: `https://school-xxx.vercel.app`

### ÉTAPE 4: Tester

1. Ouvrir l'URL Vercel
2. Se connecter avec admin@uan.bf / admin123
3. Vérifier que tout fonctionne

## 🎯 Pour la Démonstration

### Comptes à utiliser:
- **Admin**: admin@uan.bf / admin123
- **Enseignant**: j.ouedraogo@uan.bf / enseignant123  
- **Étudiant**: m.diallo@etu.bf / etudiant123

### Fonctionnalités à montrer:

**Espace Admin (5 min)**:
1. Dashboard avec statistiques
2. Gestion étudiants → Voir détails d'un étudiant
3. Gestion enseignants → Montrer les 4 grades
4. Gestion filières et matières

**Espace Enseignant (5 min)**:
1. Dashboard
2. Saisie des notes → Sélectionner une matière
3. Créer une évaluation (devoir, TP, examen)
4. Saisir des notes
5. Liste des étudiants

**Espace Étudiant (3 min)**:
1. Dashboard
2. Consulter les notes
3. Voir les paiements

## ⚠️ En cas de problème

### Backend ne répond pas
- Vérifier que l'app PythonAnywhere est "Reload"
- Vérifier les logs dans PythonAnywhere
- Tester l'URL directement: `https://VOTRENOM.pythonanywhere.com/api/`

### Frontend ne se connecte pas
- Ouvrir la console (F12)
- Vérifier l'URL de l'API dans js/api.js
- Vérifier CORS dans Django settings.py

### Données manquantes
```bash
# Dans PythonAnywhere console
cd school/backend
python3 setup.py
```

## 📞 Contact

Si problème, contacter: [VOTRE CONTACT]

## ✅ Checklist Finale

- [ ] Backend déployé et accessible
- [ ] Frontend déployé sur Vercel
- [ ] URL API mise à jour dans js/api.js
- [ ] Données de test créées
- [ ] Test de connexion réussi
- [ ] Les 3 espaces fonctionnent

---

**Temps total estimé**: 20-30 minutes
**Prêt pour la démo!** 🎉
