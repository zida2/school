# 🔧 Correction des Imports - PythonAnywhere

**Date**: 28 février 2026  
**Problème**: `NameError: name 'Classe' is not defined`

---

## ❌ Erreur Rencontrée

```python
File "/home/Wendlasida/school/backend/api/serializers.py", line 615, in Meta
    model = Classe
NameError: name 'Classe' is not defined
```

---

## ✅ Correction Appliquée

Les modèles `Classe`, `Inscription` et `EnseignementMatiere` n'étaient pas importés dans `serializers.py` et `views.py`.

**Fichiers modifiés**:
1. `backend/api/serializers.py` - Ajout des imports
2. `backend/api/views.py` - Ajout des imports

---

## 🚀 Actions à Effectuer sur PythonAnywhere

### Étape 1: Récupérer les Corrections

```bash
cd ~/school/backend
git pull origin main
```

### Étape 2: Résoudre le Conflit de Migrations

```bash
python manage.py makemigrations --merge
# Tapez 'y' quand demandé
```

### Étape 3: Appliquer les Migrations

```bash
python manage.py migrate
```

### Étape 4: Vérifier les Migrations

```bash
python manage.py showmigrations api
```

Vous devriez voir toutes les migrations avec [X], y compris la migration de fusion.

### Étape 5: Recharger l'Application

1. Allez dans l'onglet **"Web"** de PythonAnywhere
2. Cliquez sur le bouton **"Reload wendlasida.pythonanywhere.com"**
3. Attendez quelques secondes

---

## ✅ Vérification

### Test 1: Vérifier que l'application démarre

Ouvrez dans votre navigateur:
```
https://wendlasida.pythonanywhere.com/api/
```

Vous devriez voir la page d'accueil de l'API sans erreur.

### Test 2: Tester les Nouveaux Endpoints

**Classes**:
```
https://wendlasida.pythonanywhere.com/api/classes/
```

**Enseignements**:
```
https://wendlasida.pythonanywhere.com/api/enseignements/
```

**Enseignements par Enseignant**:
```
https://wendlasida.pythonanywhere.com/api/enseignements/par_enseignant/
```

**Finances**:
```
https://wendlasida.pythonanywhere.com/api/finances/statistiques/
```

---

## 📋 Commandes Complètes (Copier-Coller)

```bash
# 1. Aller dans le dossier backend
cd ~/school/backend

# 2. Récupérer les dernières modifications
git pull origin main

# 3. Fusionner les migrations
python manage.py makemigrations --merge
# Tapez 'y'

# 4. Appliquer les migrations
python manage.py migrate

# 5. Vérifier
python manage.py showmigrations api

# 6. Tester l'import des modèles
python manage.py shell
```

Dans le shell Python:
```python
from api.models import Classe, Inscription, EnseignementMatiere
print("✅ Imports OK!")

# Vérifier les tables
from django.db import connection
tables = connection.introspection.table_names()
print("Table Classe:", 'api_classe' in tables)
print("Table Inscription:", 'api_inscription' in tables)
print("Table EnseignementMatiere:", 'api_enseignementmatiere' in tables)

exit()
```

---

## 🎯 Résultat Attendu

Après ces étapes:
- ✅ L'application démarre sans erreur
- ✅ Les nouveaux endpoints sont accessibles
- ✅ Les modèles sont importés correctement
- ✅ Les tables sont créées dans la base de données

---

## ⚠️ En Cas de Problème

### Si git pull échoue

```bash
# Vérifier l'état
git status

# Si des fichiers sont modifiés localement
git stash
git pull origin main
git stash pop
```

### Si les migrations échouent

```bash
# Voir les migrations en conflit
python manage.py showmigrations api

# Supprimer la migration locale conflictuelle si nécessaire
# (Seulement si la fusion ne fonctionne pas)
rm api/migrations/0006_classe_lettrerappel_enseignementmatiere_and_more.py
python manage.py makemigrations
python manage.py migrate
```

### Si l'application ne se recharge pas

```bash
# Redémarrer manuellement
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

---

## 📊 Checklist

- [ ] `cd ~/school/backend`
- [ ] `git pull origin main`
- [ ] `python manage.py makemigrations --merge` (répondre 'y')
- [ ] `python manage.py migrate`
- [ ] `python manage.py showmigrations api`
- [ ] Tester l'import dans le shell
- [ ] Recharger l'application (onglet Web → Reload)
- [ ] Tester `/api/classes/`
- [ ] Tester `/api/enseignements/`
- [ ] Tester `/api/finances/statistiques/`

---

## 🎉 Une Fois Terminé

Tous les nouveaux endpoints seront disponibles:

**Classes et Enseignements**:
- `/api/classes/` - Gestion des classes
- `/api/inscriptions/` - Inscription des étudiants
- `/api/enseignements/` - Assignation enseignant-matière-classe
- `/api/enseignements/par_enseignant/` - Vue groupée

**Finances**:
- `/api/finances/statistiques/` - Statistiques globales
- `/api/finances/liste_impayes/` - Liste des impayés
- `/api/finances/{id}/envoyer_rappel/` - Envoyer rappel
- `/api/finances/{id}/generer_lettre/` - Générer lettre

**Emploi du Temps** (déjà existant):
- `/api/emplois-du-temps/` - Gestion des emplois du temps

---

**Commit**: `8dd28da` - Fix: Ajouter imports manquants Classe, Inscription, EnseignementMatiere 🔧

**Tout est prêt pour le déploiement!** 🚀
