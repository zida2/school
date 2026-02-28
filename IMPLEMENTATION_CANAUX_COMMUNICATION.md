# Implémentation: Canaux de Communication 💬📢

## Vue d'ensemble

Système de communication avec deux types de canaux:
1. **Canaux Officiels** (Administration → Étudiants): Annonces officielles
2. **Canaux Étudiants** (Étudiants uniquement): Discussions entre étudiants

## Architecture

### Modèles

#### 1. Canal
```python
class Canal(models.Model):
    TYPES = [
        ('officiel', 'Canal Officiel'),
        ('etudiant', 'Canal Étudiants'),
    ]
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type_canal = models.CharField(max_length=20, choices=TYPES)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
```

#### 2. Message
```python
class Message(models.Model):
    canal = models.ForeignKey(Canal, on_delete=models.CASCADE)
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    modifie = models.BooleanField(default=False)
    date_modification = models.DateTimeField(null=True, blank=True)
```

#### 3. LectureMessage
```python
class LectureMessage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_lecture = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['message', 'utilisateur']
```

## Permissions

### Canaux Officiels
- **Lecture**: Tous (admins, bureau, enseignants, étudiants)
- **Écriture**: Admins et bureau uniquement
- **Modification/Suppression**: Expéditeur ou admins

### Canaux Étudiants
- **Lecture**: Étudiants uniquement
- **Écriture**: Étudiants uniquement
- **Modification/Suppression**: Expéditeur ou admins

## API Endpoints

### Canaux
- `GET /api/canaux/`: Liste des canaux (filtrée par rôle)
- `POST /api/canaux/`: Créer un canal (admins uniquement)
- `GET /api/canaux/{id}/`: Détails d'un canal
- `PUT /api/canaux/{id}/`: Modifier un canal (admins uniquement)
- `DELETE /api/canaux/{id}/`: Supprimer un canal (admins uniquement)

### Messages
- `GET /api/messages/`: Liste des messages (filtrée par rôle et canal)
- `POST /api/messages/`: Envoyer un message
- `GET /api/messages/{id}/`: Détails d'un message
- `PUT /api/messages/{id}/`: Modifier un message (expéditeur ou admins)
- `DELETE /api/messages/{id}/`: Supprimer un message (expéditeur ou admins)
- `POST /api/messages/{id}/marquer_lu/`: Marquer un message comme lu
- `GET /api/messages/non_lus/`: Messages non lus

### Paramètres de requête
- `canal`: Filtrer par canal (ex: `/api/messages/?canal=1`)
- `search`: Rechercher dans le contenu et les noms

## Canaux par défaut

### Canaux Officiels
1. **Annonces Officielles**
   - Description: Canal officiel pour les annonces de l'administration
   - Type: officiel

2. **Informations Académiques**
   - Description: Informations sur les cours, examens et emplois du temps
   - Type: officiel

### Canaux Étudiants
3. **Discussion Générale**
   - Description: Canal de discussion pour tous les étudiants
   - Type: etudiant

4. **Entraide Étudiants**
   - Description: Canal d'entraide et de partage entre étudiants
   - Type: etudiant

## Installation

### 1. Appliquer les migrations
```bash
cd ~/school/backend
python manage.py makemigrations
python manage.py migrate
```

### 2. Créer les canaux par défaut
```bash
python creer_canaux_defaut.py
```

## Utilisation

### Envoyer un message (Admin/Bureau)
```javascript
// Dans un canal officiel
const message = await API.post('/messages/', {
    canal: 1,  // ID du canal "Annonces Officielles"
    contenu: 'Les examens du semestre 1 auront lieu du 15 au 20 mars.'
});
```

### Envoyer un message (Étudiant)
```javascript
// Dans un canal étudiant
const message = await API.post('/messages/', {
    canal: 3,  // ID du canal "Discussion Générale"
    contenu: 'Quelqu\'un a des notes de cours de mathématiques?'
});
```

### Récupérer les messages d'un canal
```javascript
const messages = await API.get('/messages/?canal=1');
```

### Marquer un message comme lu
```javascript
await API.post(`/messages/${messageId}/marquer_lu/`);
```

### Récupérer les messages non lus
```javascript
const nonLus = await API.get('/messages/non_lus/?canal=1');
```

## Frontend (À implémenter)

### Structure suggérée

#### Page Communication (tous les rôles)
```html
<div class="page-ultra" id="page-communication">
    <!-- Liste des canaux -->
    <div class="canaux-list">
        <div class="canal-item" onclick="ouvrirCanal(1)">
            <h3>📢 Annonces Officielles</h3>
            <span class="badge-ultra">3 nouveaux</span>
        </div>
        <!-- ... autres canaux -->
    </div>
    
    <!-- Zone de messages -->
    <div class="messages-container">
        <div class="message-item">
            <div class="message-header">
                <strong>Admin UAN</strong>
                <span>15/03/2026 10:30</span>
            </div>
            <div class="message-content">
                Les examens du semestre 1 auront lieu du 15 au 20 mars.
            </div>
        </div>
        <!-- ... autres messages -->
    </div>
    
    <!-- Formulaire d'envoi (si autorisé) -->
    <div class="message-form">
        <textarea placeholder="Votre message..."></textarea>
        <button onclick="envoyerMessage()">Envoyer</button>
    </div>
</div>
```

### Fonctions JavaScript suggérées
```javascript
async function chargerCanaux() {
    const canaux = await API.get('/canaux/');
    // Afficher les canaux avec badges de messages non lus
}

async function ouvrirCanal(canalId) {
    const messages = await API.get(`/messages/?canal=${canalId}`);
    // Afficher les messages
    // Marquer les messages comme lus
}

async function envoyerMessage(canalId, contenu) {
    await API.post('/messages/', {
        canal: canalId,
        contenu: contenu
    });
    // Recharger les messages
}

async function chargerMessagesNonLus() {
    const nonLus = await API.get('/messages/non_lus/');
    // Afficher le nombre de messages non lus
}
```

## Fonctionnalités avancées (optionnelles)

### 1. Notifications en temps réel
- Utiliser WebSockets ou Server-Sent Events
- Notifier les utilisateurs des nouveaux messages

### 2. Réactions aux messages
- Ajouter un modèle `ReactionMessage`
- Permettre les émojis (👍, ❤️, 😂, etc.)

### 3. Pièces jointes
- Ajouter un champ `fichier` au modèle `Message`
- Gérer l'upload de fichiers

### 4. Mentions
- Permettre de mentionner des utilisateurs (@nom)
- Envoyer une notification à l'utilisateur mentionné

### 5. Recherche avancée
- Recherche par date
- Recherche par expéditeur
- Recherche par canal

## Sécurité

### Validation
- Contenu des messages: max 5000 caractères
- Vérification des permissions avant chaque action
- Validation du type de canal

### Rate Limiting (à implémenter)
- Limiter le nombre de messages par minute
- Prévenir le spam

### Modération (à implémenter)
- Signalement de messages inappropriés
- Suppression par les admins
- Bannissement temporaire

## Tests

### Test des permissions
```python
# Test: Étudiant ne peut pas écrire dans canal officiel
response = client.post('/api/messages/', {
    'canal': 1,  # Canal officiel
    'contenu': 'Test'
}, headers={'Authorization': f'Bearer {token_etudiant}'})
assert response.status_code == 403

# Test: Admin peut écrire dans canal officiel
response = client.post('/api/messages/', {
    'canal': 1,
    'contenu': 'Annonce importante'
}, headers={'Authorization': f'Bearer {token_admin}'})
assert response.status_code == 201
```

## Migration des données

Si vous avez déjà des données dans `MessageBureau`, vous pouvez les migrer:

```python
from api.models import MessageBureau, Canal, Message

# Créer un canal pour les messages bureau
canal_bureau = Canal.objects.create(
    nom='Messages Bureau',
    type_canal='officiel',
    description='Ancien système de messages bureau'
)

# Migrer les messages
for msg in MessageBureau.objects.all():
    Message.objects.create(
        canal=canal_bureau,
        expediteur=msg.expediteur,
        contenu=msg.contenu,
        date_envoi=msg.date_envoi
    )
```

## Déploiement

### Backend (PythonAnywhere)
```bash
cd ~/school/backend
git pull origin main
python manage.py makemigrations
python manage.py migrate
python creer_canaux_defaut.py
# Recharger l'app web
```

### Frontend (Vercel)
- Déploiement automatique après push
- Vider le cache: `Ctrl + Shift + R`

## Fichiers créés/modifiés

### Backend
- `backend/api/models.py`: Ajout des modèles Canal, Message, LectureMessage
- `backend/api/serializers.py`: Ajout des serializers
- `backend/api/views.py`: Ajout des ViewSets
- `backend/api/urls.py`: Ajout des routes
- `backend/api/admin.py`: Ajout de l'admin
- `backend/api/migrations/0007_canal_message.py`: Migration
- `backend/creer_canaux_defaut.py`: Script de création des canaux

### Documentation
- `IMPLEMENTATION_CANAUX_COMMUNICATION.md`: Ce fichier

## Prochaines étapes

1. Appliquer les migrations sur PythonAnywhere
2. Créer les canaux par défaut
3. Implémenter le frontend (page Communication)
4. Tester les permissions
5. Ajouter les notifications de nouveaux messages
6. (Optionnel) Implémenter les fonctionnalités avancées

## Support

Pour toute question ou problème:
1. Vérifier les logs Django: `/var/log/wendlasida.pythonanywhere.com.error.log`
2. Vérifier les permissions dans le code
3. Tester les endpoints avec Postman ou curl
