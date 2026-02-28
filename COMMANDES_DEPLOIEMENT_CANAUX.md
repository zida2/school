# Commandes de déploiement - Canaux de Communication

## Erreur rencontrée
```
django.db.utils.OperationalError: no such table: api_canal
```

## Cause
Le script `creer_canaux_defaut.py` a été exécuté AVANT d'appliquer la migration.

## Solution: Ordre correct des commandes

### Sur PythonAnywhere

```bash
# 1. Aller dans le répertoire backend
cd ~/school/backend

# 2. Activer l'environnement virtuel (si pas déjà fait)
source ~/.virtualenvs/myenv/bin/activate

# 3. Vérifier les migrations en attente
python manage.py showmigrations api

# 4. Appliquer TOUTES les migrations
python manage.py migrate

# 5. Vérifier que la migration 0008 est appliquée
python manage.py showmigrations api | grep 0008

# 6. MAINTENANT créer les canaux
python creer_canaux_defaut.py

# 7. Recharger l'application web
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

## Vérification étape par étape

### Étape 3: Vérifier les migrations
Sortie attendue:
```
api
 [X] 0001_initial
 [X] 0002_reclamationnote
 [X] 0003_evaluation_noteevaluation
 [X] 0004_note_statut
 [X] 0005_questionsondage_alter_utilisateur_role_and_more
 [X] 0006_classe_lettrerappel_enseignementmatiere_and_more
 [X] 0007_merge_20260228_1937
 [ ] 0008_canal_message  <-- Pas encore appliquée
```

### Étape 4: Appliquer les migrations
Sortie attendue:
```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, sessions
Running migrations:
  Applying api.0008_canal_message... OK
```

### Étape 5: Vérifier la migration 0008
Sortie attendue:
```
 [X] 0008_canal_message
```

### Étape 6: Créer les canaux
Sortie attendue:
```
🔧 Création des canaux de communication...
  ✅ Canal créé: Annonces Officielles (Canal Officiel)
  ✅ Canal créé: Informations Académiques (Canal Officiel)
  ✅ Canal créé: Discussion Générale (Canal Étudiants)
  ✅ Canal créé: Entraide Étudiants (Canal Étudiants)

📊 Total: 4 canaux
  - Canaux officiels: 2
  - Canaux étudiants: 2
```

## Si la migration échoue

### Erreur: "Conflicting migrations"
```bash
# Fusionner les migrations
python manage.py makemigrations --merge

# Appliquer
python manage.py migrate
```

### Erreur: "Migration already applied"
```bash
# Vérifier l'état
python manage.py showmigrations api

# Si 0008 est déjà cochée [X], passer directement à la création des canaux
python creer_canaux_defaut.py
```

### Erreur: "Table already exists"
Si la table existe déjà mais la migration n'est pas marquée comme appliquée:
```bash
# Marquer la migration comme appliquée sans l'exécuter
python manage.py migrate api 0008 --fake
```

## Vérification finale

### Via le shell Django
```bash
python manage.py shell
```

```python
from api.models import Canal, Message

# Vérifier les canaux
print(f"Nombre de canaux: {Canal.objects.count()}")
for canal in Canal.objects.all():
    print(f"  - {canal.nom} ({canal.get_type_canal_display()})")

# Quitter
exit()
```

### Via l'API
```bash
# Tester l'endpoint (remplacer TOKEN par un vrai token)
curl -H "Authorization: Bearer TOKEN" \
  https://wendlasida.pythonanywhere.com/api/canaux/
```

## Recharger l'application

### Option 1: Via le dashboard (recommandé)
1. Aller sur https://www.pythonanywhere.com
2. Onglet "Web"
3. Cliquer sur "Reload" (bouton vert)

### Option 2: Via le terminal
```bash
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

## Résumé des commandes (copier-coller)

```bash
cd ~/school/backend
source ~/.virtualenvs/myenv/bin/activate
python manage.py migrate
python creer_canaux_defaut.py
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

## Test rapide

Après le déploiement, tester avec curl:
```bash
# Récupérer un token (remplacer les identifiants)
TOKEN=$(curl -X POST https://wendlasida.pythonanywhere.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@uan.bf","password":"admin123"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access'])")

# Tester l'endpoint canaux
curl -H "Authorization: Bearer $TOKEN" \
  https://wendlasida.pythonanywhere.com/api/canaux/
```

## Notes importantes

1. **Toujours appliquer les migrations AVANT de créer des données**
2. **Vérifier que la migration est appliquée avec `showmigrations`**
3. **Recharger l'application après les changements**
4. **Tester l'API pour confirmer que tout fonctionne**

## En cas de problème persistant

1. Vérifier les logs:
```bash
tail -f /var/log/wendlasida.pythonanywhere.com.error.log
```

2. Vérifier la base de données:
```bash
python manage.py dbshell
.tables  # Lister les tables
.schema api_canal  # Voir la structure de la table
.quit
```

3. Réinitialiser la migration (ATTENTION: perte de données):
```bash
# Supprimer la table
python manage.py dbshell
DROP TABLE IF EXISTS api_canal;
DROP TABLE IF EXISTS api_message;
DROP TABLE IF EXISTS api_lecturemessage;
.quit

# Réappliquer la migration
python manage.py migrate api 0008
```
