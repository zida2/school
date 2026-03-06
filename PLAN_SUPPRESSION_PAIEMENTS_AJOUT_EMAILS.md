# Plan: Suppression Paiements + Ajout Notifications Email 📧

## Objectif
L'école veut un système centré sur l'académique uniquement:
- ✅ Programme/Emploi du temps
- ✅ Cours et supports
- ✅ Notes et évaluations
- ✅ Présences/Absences
- ✅ Communication (canaux)
- ✅ Demandes administratives
- ❌ SUPPRIMER: Tout ce qui concerne les paiements
- ➕ AJOUTER: Notifications par email

## Phase 1: Suppression des paiements

### Backend - Fichiers à supprimer
1. `backend/api/views_finances.py` - ViewSets finances
2. `backend/ajouter_paiements_test.py` - Script de test
3. Migrations liées aux paiements (à identifier)

### Backend - Modèles à supprimer
Dans `backend/api/models.py`:
- `Paiement`
- `RappelPaiement`
- `LettreRappel`

### Backend - Serializers à supprimer
Dans `backend/api/serializers.py`:
- `PaiementSerializer`
- `RappelPaiementSerializer`
- `LettreRappelSerializer`

### Backend - ViewSets à supprimer
Dans `backend/api/views.py`:
- `PaiementViewSet`
- `GestionFinanciereViewSet`
- `RappelPaiementViewSet`
- `LettreRappelViewSet`

### Backend - URLs à supprimer
Dans `backend/api/urls.py`:
- `/api/paiements/`
- `/api/finances/`
- `/api/rappels-paiement/`
- `/api/lettres-rappel/`

### Backend - Admin à supprimer
Dans `backend/api/admin.py`:
- `PaiementAdmin`
- `RappelPaiementAdmin`
- `LettreRappelAdmin`

### Frontend - Sections à supprimer
Dans tous les dashboards:
- Sections "Paiements"
- Sections "Finances"
- Cartes de statistiques financières
- Fonctions JavaScript liées aux paiements

### Documentation à nettoyer
- `IMPLEMENTATION_FINANCES_COMPLETE.md`
- Références dans autres docs

## Phase 2: Ajout des notifications par email

### Backend - Nouveau modèle
```python
class NotificationEmail(models.Model):
    TYPES = [
        ('nouvelle_note', 'Nouvelle note publiée'),
        ('modification_note', 'Note modifiée'),
        ('nouvelle_evaluation', 'Nouvelle évaluation programmée'),
        ('absence_signale', 'Absence signalée'),
        ('support_cours', 'Nouveau support de cours'),
        ('emploi_modifie', 'Emploi du temps modifié'),
        ('demande_traitee', 'Demande administrative traitée'),
        ('message_canal', 'Nouveau message dans un canal'),
        ('annonce_officielle', 'Annonce officielle'),
    ]
    
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    type_notification = models.CharField(max_length=30, choices=TYPES)
    sujet = models.CharField(max_length=200)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    envoye = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)
    lien = models.CharField(max_length=500, blank=True)
```

### Backend - Service d'envoi d'emails
```python
# backend/api/email_service.py
from django.core.mail import send_mail
from django.conf import settings

def envoyer_notification_email(destinataire, sujet, contenu, lien=None):
    """
    Envoyer une notification par email
    """
    message = f"{contenu}\n\n"
    if lien:
        message += f"Lien: {settings.FRONTEND_URL}{lien}\n\n"
    message += "---\nCeci est un email automatique, merci de ne pas répondre."
    
    send_mail(
        subject=sujet,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[destinataire.email],
        fail_silently=False,
    )
```

### Backend - Triggers automatiques
Envoyer des emails automatiquement quand:
1. Une nouvelle note est publiée → Email à l'étudiant
2. Une évaluation est programmée → Email aux étudiants concernés
3. Un support de cours est ajouté → Email aux étudiants de la classe
4. Une absence est signalée → Email à l'étudiant
5. Une demande est traitée → Email au demandeur
6. Un message officiel est publié → Email à tous les étudiants
7. L'emploi du temps change → Email aux étudiants concernés

### Frontend - Préférences de notification
Ajouter dans les paramètres utilisateur:
- Activer/désactiver les notifications par email
- Choisir les types de notifications à recevoir
- Fréquence (immédiat, quotidien, hebdomadaire)

## Phase 3: Configuration email

### Settings Django
```python
# backend/erp_backend/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # ou autre
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@uan.bf'
EMAIL_HOST_PASSWORD = 'mot_de_passe'
DEFAULT_FROM_EMAIL = 'UAN - Système de Gestion <noreply@uan.bf>'
FRONTEND_URL = 'https://school-wheat-six.vercel.app'
```

## Ordre d'exécution

### Étape 1: Suppression backend
1. Supprimer les fichiers
2. Supprimer les imports
3. Supprimer les routes
4. Créer une migration pour supprimer les tables
5. Tester que l'API fonctionne sans erreurs

### Étape 2: Suppression frontend
1. Supprimer les sections paiements des dashboards
2. Supprimer les fonctions JavaScript
3. Nettoyer les CSS
4. Tester tous les dashboards

### Étape 3: Ajout notifications
1. Créer le modèle NotificationEmail
2. Créer le service d'envoi
3. Ajouter les triggers
4. Créer l'interface de préférences
5. Tester l'envoi d'emails

### Étape 4: Documentation
1. Mettre à jour la documentation
2. Créer un guide d'utilisation des notifications
3. Documenter la configuration email

## Risques et précautions

### Données existantes
- ⚠️ Les paiements existants seront perdus
- Solution: Exporter les données avant suppression si nécessaire

### Dépendances
- Vérifier qu'aucun autre modèle ne dépend de Paiement
- Vérifier les ForeignKey et relations

### Tests
- Tester chaque dashboard après suppression
- Tester l'envoi d'emails en environnement de test
- Vérifier que toutes les fonctionnalités académiques fonctionnent

## Commandes de déploiement

```bash
# Backend
cd ~/school/backend
git pull origin main
python manage.py makemigrations
python manage.py migrate
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py

# Vérifier
python manage.py shell
>>> from api.models import Paiement
>>> # Devrait donner une erreur (modèle n'existe plus)
```

## Estimation du temps
- Phase 1 (Suppression): 2-3 heures
- Phase 2 (Notifications): 3-4 heures
- Phase 3 (Configuration): 1 heure
- Tests: 1-2 heures
- **Total: 7-10 heures**

## Voulez-vous que je commence?
1. Commencer par la suppression des paiements
2. Puis ajouter les notifications par email
3. Ou faire les deux en parallèle?
