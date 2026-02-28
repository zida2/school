# 🔧 Résolution du Conflit de Migrations

## ❌ Problème

```
CommandError: Conflicting migrations detected; multiple leaf nodes in the migration graph: 
(0006_classe_enseignementmatiere_inscription, 0006_classe_lettrerappel_enseignementmatiere_and_more in api).
To fix them run 'python manage.py makemigrations --merge'
```

## 📋 Explication

Il y a deux migrations "0006" différentes:
1. **Sur PythonAnywhere**: `0006_classe_enseignementmatiere_inscription` (créée avant)
2. **En local**: `0006_classe_lettrerappel_enseignementmatiere_and_more` (créée aujourd'hui)

Django ne sait pas laquelle appliquer en premier.

## ✅ Solution

### Étape 1: Fusionner les Migrations

Sur PythonAnywhere, dans le dossier `~/school/backend`:

```bash
python manage.py makemigrations --merge
```

Django va vous demander de confirmer:
```
Merging will only work if the operations printed above do not conflict
with each other (working on different fields or models)
Do you want to merge these migration branches? [y/N]
```

Tapez **y** et appuyez sur Entrée.

### Étape 2: Appliquer les Migrations

```bash
python manage.py migrate
```

### Étape 3: Recharger l'Application

- Allez dans l'onglet **"Web"**
- Cliquez sur le bouton **"Reload"**

## 🎯 Commandes Complètes

Copiez-collez ces commandes une par une:

```bash
# 1. Aller dans le dossier backend
cd ~/school/backend

# 2. Fusionner les migrations
python manage.py makemigrations --merge
# Tapez 'y' quand demandé

# 3. Appliquer les migrations
python manage.py migrate

# 4. Vérifier que tout est OK
python manage.py showmigrations api
```

## 📊 Résultat Attendu

Après `python manage.py showmigrations api`, vous devriez voir:

```
api
 [X] 0001_initial
 [X] 0002_reclamationnote
 [X] 0003_evaluation_noteevaluation
 [X] 0004_note_statut
 [X] 0005_questionsondage_alter_utilisateur_role_and_more
 [X] 0006_classe_enseignementmatiere_inscription
 [X] 0006_classe_lettrerappel_enseignementmatiere_and_more
 [X] 0007_merge_XXXXXX (la migration de fusion)
```

## ⚠️ Si Ça Ne Marche Pas

### Option Alternative: Supprimer et Recréer

Si la fusion échoue, vous pouvez:

```bash
# 1. Supprimer la migration locale conflictuelle
rm backend/api/migrations/0006_classe_lettrerappel_enseignementmatiere_and_more.py

# 2. Recréer les migrations
python manage.py makemigrations

# 3. Appliquer
python manage.py migrate
```

## 🔍 Vérification

Pour vérifier que les nouveaux modèles sont bien créés:

```bash
python manage.py shell
```

Puis dans le shell Python:

```python
from api.models import RappelPaiement, LettreRappel, HistoriqueNote
print("✅ Modèles importés avec succès!")

# Vérifier les tables
from django.db import connection
tables = connection.introspection.table_names()
print("Tables RappelPaiement:", 'api_rappelpaiement' in tables)
print("Tables LettreRappel:", 'api_lettrerappel' in tables)
print("Tables HistoriqueNote:", 'api_historiquenote' in tables)
```

Tapez `exit()` pour quitter le shell.

## ✅ Checklist

- [ ] `cd ~/school/backend`
- [ ] `python manage.py makemigrations --merge` (répondre 'y')
- [ ] `python manage.py migrate`
- [ ] Recharger l'application (onglet Web → Reload)
- [ ] Vérifier avec `python manage.py showmigrations api`
- [ ] Tester un endpoint: `/api/finances/statistiques/`

## 🎉 Une Fois Résolu

Les nouveaux endpoints seront disponibles:
- `/api/finances/statistiques/`
- `/api/finances/liste_impayes/`
- `/api/finances/{id}/envoyer_rappel/`
- `/api/finances/{id}/generer_lettre/`

---

**C'est un problème courant et facile à résoudre! 🚀**
