# Déploiement: Canaux de Communication 💬📢

## Problème résolu
Conflit de migrations détecté:
- Migration existante: `0007_merge_20260228_1937`
- Nouvelle migration: `0007_canal_message` (conflit!)
- Solution: Renommée en `0008_canal_message`

## Déploiement sur PythonAnywhere

### 1. Se connecter à PythonAnywhere
- URL: https://www.pythonanywhere.com
- Compte: `wendlasida`
- Ouvrir un terminal Bash

### 2. Mettre à jour le code
```bash
cd ~/school/backend
git pull origin main
```

### 3. Appliquer les migrations
```bash
python manage.py migrate
```

Sortie attendue:
```
Running migrations:
  Applying api.0008_canal_message... OK
```

### 4. Créer les canaux par défaut
```bash
python creer_canaux_defaut.py
```

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

### 5. Recharger l'application web
Deux options:

#### Option A: Via le dashboard (recommandé)
1. Aller dans l'onglet "Web"
2. Trouver l'application `wendlasida.pythonanywhere.com`
3. Cliquer sur le bouton vert "Reload"

#### Option B: Via le terminal
```bash
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

### 6. Vérifier l'API
```bash
# Tester l'endpoint canaux
curl https://wendlasida.pythonanywhere.com/api/canaux/
```

Ou via le navigateur:
1. Aller sur https://school-wheat-six.vercel.app
2. Se connecter avec n'importe quel compte
3. Ouvrir la console développeur (F12)
4. Taper: `await API.get('/canaux/')`
5. Vérifier que les 4 canaux sont retournés

## Test des permissions

### Test 1: Admin peut créer un canal
```bash
# Se connecter en tant qu'admin
# Créer un canal
curl -X POST https://wendlasida.pythonanywhere.com/api/canaux/ \
  -H "Authorization: Bearer <TOKEN_ADMIN>" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Test Canal",
    "description": "Canal de test",
    "type_canal": "officiel"
  }'
```

### Test 2: Admin peut écrire dans canal officiel
```bash
curl -X POST https://wendlasida.pythonanywhere.com/api/messages/ \
  -H "Authorization: Bearer <TOKEN_ADMIN>" \
  -H "Content-Type: application/json" \
  -d '{
    "canal": 1,
    "contenu": "Annonce importante"
  }'
```

### Test 3: Étudiant ne peut PAS écrire dans canal officiel
```bash
curl -X POST https://wendlasida.pythonanywhere.com/api/messages/ \
  -H "Authorization: Bearer <TOKEN_ETUDIANT>" \
  -H "Content-Type: application/json" \
  -d '{
    "canal": 1,
    "contenu": "Test"
  }'
# Devrait retourner 403 Forbidden
```

### Test 4: Étudiant peut écrire dans canal étudiant
```bash
curl -X POST https://wendlasida.pythonanywhere.com/api/messages/ \
  -H "Authorization: Bearer <TOKEN_ETUDIANT>" \
  -H "Content-Type: application/json" \
  -d '{
    "canal": 3,
    "contenu": "Salut tout le monde!"
  }'
# Devrait retourner 201 Created
```

## Vérification de la base de données

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

# Vérifier les messages
print(f"\nNombre de messages: {Message.objects.count()}")
for msg in Message.objects.all():
    print(f"  - {msg.expediteur.get_full_name()} dans {msg.canal.nom}")
```

## Résolution des problèmes

### Erreur: "No such table: api_canal"
```bash
# Vérifier que la migration a été appliquée
python manage.py showmigrations api

# Si 0008_canal_message n'est pas coché, appliquer:
python manage.py migrate api 0008
```

### Erreur: "Conflicting migrations"
```bash
# Fusionner les migrations
python manage.py makemigrations --merge

# Appliquer
python manage.py migrate
```

### Erreur: "Permission denied"
Vérifier que l'utilisateur a les bonnes permissions:
```python
from api.models import Utilisateur

user = Utilisateur.objects.get(email='admin@uan.bf')
print(f"Rôle: {user.role}")  # Devrait être 'admin' ou 'superadmin'
```

## Endpoints disponibles

### Canaux
- `GET /api/canaux/`: Liste des canaux
- `POST /api/canaux/`: Créer un canal (admins uniquement)
- `GET /api/canaux/{id}/`: Détails d'un canal
- `PUT /api/canaux/{id}/`: Modifier un canal
- `DELETE /api/canaux/{id}/`: Supprimer un canal

### Messages
- `GET /api/messages/`: Liste des messages
- `POST /api/messages/`: Envoyer un message
- `GET /api/messages/{id}/`: Détails d'un message
- `PUT /api/messages/{id}/`: Modifier un message
- `DELETE /api/messages/{id}/`: Supprimer un message
- `POST /api/messages/{id}/marquer_lu/`: Marquer comme lu
- `GET /api/messages/non_lus/`: Messages non lus

### Paramètres de requête
- `?canal=1`: Filtrer par canal
- `?search=mot`: Rechercher dans le contenu

## Prochaines étapes

1. ✅ Backend déployé
2. ✅ Canaux créés
3. ⏳ Frontend à implémenter
4. ⏳ Tests des permissions
5. ⏳ Notifications en temps réel (optionnel)

## Fichiers modifiés

### Backend
- `backend/api/models.py`: +55 lignes (Canal, Message, LectureMessage)
- `backend/api/serializers.py`: +60 lignes
- `backend/api/views.py`: +142 lignes
- `backend/api/urls.py`: +6 lignes
- `backend/api/admin.py`: +25 lignes
- `backend/api/migrations/0008_canal_message.py`: Nouvelle migration
- `backend/creer_canaux_defaut.py`: Script de création

### Documentation
- `IMPLEMENTATION_CANAUX_COMMUNICATION.md`: Documentation complète
- `DEPLOIEMENT_CANAUX_COMMUNICATION.md`: Ce fichier

## Commit
`5498c68` - Feat: Système de canaux de communication (Admin→Étudiants + Étudiants) 💬📢

## Notes importantes

### Permissions
- Canaux officiels: Lecture pour tous, écriture pour admins/bureau uniquement
- Canaux étudiants: Lecture et écriture pour étudiants uniquement

### Sécurité
- Validation du contenu (max 5000 caractères recommandé)
- Vérification des permissions avant chaque action
- Rate limiting à implémenter pour éviter le spam

### Performance
- Index sur `canal` et `date_envoi` pour les requêtes
- Pagination recommandée pour les listes de messages
- Cache pour les canaux (changent rarement)

## Support

En cas de problème:
1. Vérifier les logs: `/var/log/wendlasida.pythonanywhere.com.error.log`
2. Vérifier les migrations: `python manage.py showmigrations`
3. Vérifier les permissions dans le code
4. Tester avec curl ou Postman
