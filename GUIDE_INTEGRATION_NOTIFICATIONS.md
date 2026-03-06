# 📧 GUIDE D'INTÉGRATION DES NOTIFICATIONS

## 🎯 OBJECTIF

Intégrer les appels de notification dans les ViewSets existants pour envoyer automatiquement des emails aux utilisateurs lors des actions importantes.

---

## 📋 LISTE DES INTÉGRATIONS À FAIRE

### 1. Nouvelle Note Publiée
**Fichier**: `backend/api/views.py`  
**ViewSet**: `NoteViewSet`  
**Action**: `publier()`  
**Ligne**: ~520

```python
@action(detail=False, methods=['post'])
def publier(self, request):
    """Publier les notes d'une matière et notifier les étudiants"""
    matiere_id = request.data.get('matiere_id')
    annee_id = request.data.get('annee_academique_id')
    
    # ... code existant ...
    
    count = 0
    for note in notes:
        note.publie = True
        note.statut = 'publie'
        note.save()
        count += 1
        
        # ✅ AJOUTER ICI: Notifier l'étudiant
        from .email_service import notifier_nouvelle_note
        try:
            notifier_nouvelle_note(note.id)
        except Exception as e:
            print(f"Erreur notification note {note.id}: {e}")
        
        # Créer notification pour l'étudiant (code existant)
        if hasattr(note.etudiant, 'utilisateur') and note.etudiant.utilisateur:
            Notification.objects.create(...)
    
    # ... reste du code ...
```

### 2. Nouvelle Évaluation Créée
**Fichier**: `backend/api/views.py`  
**ViewSet**: `EvaluationViewSet`  
**Action**: `create()`  
**Ligne**: ~850

```python
def perform_create(self, serializer):
    """Créer une évaluation et notifier les étudiants"""
    evaluation = serializer.save()
    
    # ✅ AJOUTER ICI: Notifier les étudiants de la filière
    from .email_service import notifier_nouvelle_evaluation
    try:
        notifier_nouvelle_evaluation(evaluation.id)
    except Exception as e:
        print(f"Erreur notification évaluation {evaluation.id}: {e}")
```

### 3. Absence Enregistrée
**Fichier**: `backend/api/views.py`  
**ViewSet**: `PresenceViewSet`  
**Action**: `perform_create()` ou `enregistrer_session()`  
**Ligne**: ~650

```python
def perform_create(self, serializer):
    """Enregistrer une présence et notifier si absence"""
    presence = serializer.save(enregistre_par=self.request.user)
    
    # ✅ AJOUTER ICI: Notifier si absence
    if not presence.present and not presence.justifie:
        from .email_service import notifier_absence
        try:
            notifier_absence(presence.id)
        except Exception as e:
            print(f"Erreur notification absence {presence.id}: {e}")
```

### 4. Nouveau Support de Cours
**Fichier**: `backend/api/views.py`  
**ViewSet**: `SupportCoursViewSet`  
**Action**: `perform_create()`  
**Ligne**: ~680

```python
def perform_create(self, serializer):
    """Créer un support de cours et notifier les étudiants"""
    support = serializer.save()
    
    # ✅ AJOUTER ICI: Notifier les étudiants de la filière
    from .email_service import notifier_nouveau_support
    try:
        notifier_nouveau_support(support.id)
    except Exception as e:
        print(f"Erreur notification support {support.id}: {e}")
```

### 5. Emploi du Temps Modifié
**Fichier**: `backend/api/views.py`  
**ViewSet**: `EmploiDuTempsViewSet`  
**Action**: `perform_update()`  
**Ligne**: ~620

```python
def perform_update(self, serializer):
    """Mettre à jour un emploi du temps et notifier les étudiants"""
    emploi = serializer.save()
    
    # ✅ AJOUTER ICI: Notifier les étudiants de la filière
    from .email_service import notifier_emploi_modifie
    try:
        notifier_emploi_modifie(emploi.id)
    except Exception as e:
        print(f"Erreur notification emploi {emploi.id}: {e}")
```

### 6. Demande Administrative Traitée
**Fichier**: `backend/api/views.py`  
**ViewSet**: `DemandeAdministrativeViewSet`  
**Action**: `traiter()` et `repondre()`  
**Ligne**: ~1450

```python
@action(detail=True, methods=['post'])
def traiter(self, request, pk=None):
    """Traiter une demande et notifier l'étudiant"""
    demande = self.get_object()
    
    # ... code existant ...
    
    demande.statut = statut
    demande.commentaire_admin = commentaire
    demande.traite_par = request.user
    demande.date_traitement = timezone.now()
    demande.save()
    
    # ✅ AJOUTER ICI: Notifier l'étudiant
    from .email_service import notifier_demande_traitee
    try:
        notifier_demande_traitee(demande.id)
    except Exception as e:
        print(f"Erreur notification demande {demande.id}: {e}")
    
    return Response({...})
```

### 7. Nouveau Message dans un Canal
**Fichier**: `backend/api/views.py`  
**ViewSet**: `MessageViewSet`  
**Action**: `perform_create()`  
**Ligne**: ~1900

```python
def perform_create(self, serializer):
    """Créer un message et notifier selon le type de canal"""
    canal = serializer.validated_data['canal']
    user = self.request.user
    
    # Vérifier les permissions d'écriture (code existant)
    if canal.type_canal == 'officiel':
        if user.role not in ['admin', 'superadmin', 'bureau_executif']:
            raise PermissionDenied(...)
    elif canal.type_canal == 'etudiant':
        if user.role != 'etudiant':
            raise PermissionDenied(...)
    
    message = serializer.save()
    
    # ✅ AJOUTER ICI: Notifier selon le type de canal
    from .email_service import notifier_message_canal, notifier_annonce_officielle
    try:
        if canal.type_canal == 'officiel':
            # Annonce officielle
            notifier_annonce_officielle(message.id)
        else:
            # Message dans un canal étudiant
            notifier_message_canal(message.id)
    except Exception as e:
        print(f"Erreur notification message {message.id}: {e}")
```

---

## 🔧 EXEMPLE COMPLET D'INTÉGRATION

### Avant (sans notification)
```python
@action(detail=False, methods=['post'])
def publier(self, request):
    matiere_id = request.data.get('matiere_id')
    annee_id = request.data.get('annee_academique_id')
    
    notes = Note.objects.filter(
        matiere_id=matiere_id,
        annee_academique_id=annee_id,
        publie=False
    )
    
    count = 0
    for note in notes:
        note.publie = True
        note.statut = 'publie'
        note.save()
        count += 1
    
    return Response({'detail': f'{count} note(s) publiée(s)'})
```

### Après (avec notification)
```python
@action(detail=False, methods=['post'])
def publier(self, request):
    matiere_id = request.data.get('matiere_id')
    annee_id = request.data.get('annee_academique_id')
    
    notes = Note.objects.filter(
        matiere_id=matiere_id,
        annee_academique_id=annee_id,
        publie=False
    )
    
    count = 0
    notif_count = 0
    for note in notes:
        note.publie = True
        note.statut = 'publie'
        note.save()
        count += 1
        
        # ✅ NOUVEAU: Notifier l'étudiant par email
        from .email_service import notifier_nouvelle_note
        try:
            notifier_nouvelle_note(note.id)
            notif_count += 1
        except Exception as e:
            print(f"Erreur notification note {note.id}: {e}")
    
    return Response({
        'detail': f'{count} note(s) publiée(s)',
        'notifications_envoyees': notif_count
    })
```

---

## 📝 BONNES PRATIQUES

### 1. Toujours utiliser try/except
```python
try:
    notifier_nouvelle_note(note.id)
except Exception as e:
    print(f"Erreur notification: {e}")
    # Ne pas bloquer l'action principale si la notification échoue
```

### 2. Importer au moment de l'utilisation
```python
# ✅ BON: Import local
def perform_create(self, serializer):
    from .email_service import notifier_nouvelle_note
    notifier_nouvelle_note(note.id)

# ❌ MAUVAIS: Import global (peut causer des imports circulaires)
from .email_service import notifier_nouvelle_note

class NoteViewSet(viewsets.ModelViewSet):
    ...
```

### 3. Logger les erreurs
```python
import logging
logger = logging.getLogger(__name__)

try:
    notifier_nouvelle_note(note.id)
except Exception as e:
    logger.error(f"Erreur notification note {note.id}: {e}")
```

### 4. Vérifier les préférences (déjà fait dans le service)
Le service `email_service.py` vérifie automatiquement:
- Si l'utilisateur a activé les notifications email
- Si le type de notification est activé
- Si l'utilisateur a une adresse email valide

Pas besoin de vérifier manuellement dans les ViewSets.

---

## 🧪 TESTS

### Test 1: Publier une note
```bash
# 1. Créer une note non publiée
curl -X POST https://wendlasida.pythonanywhere.com/api/notes/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "etudiant": 1,
    "matiere": 1,
    "note_cc": 15,
    "note_examen": 16,
    "publie": false
  }'

# 2. Publier la note
curl -X POST https://wendlasida.pythonanywhere.com/api/notes/publier/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "matiere_id": 1,
    "annee_academique_id": 1
  }'

# 3. Vérifier les notifications créées
curl -X GET https://wendlasida.pythonanywhere.com/api/notifications-email/ \
  -H "Authorization: Bearer TOKEN"
```

### Test 2: Créer une évaluation
```bash
curl -X POST https://wendlasida.pythonanywhere.com/api/evaluations/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "matiere": 1,
    "titre": "Examen Final",
    "date_evaluation": "2026-03-15",
    "actif": true
  }'

# Vérifier les notifications
curl -X GET https://wendlasida.pythonanywhere.com/api/notifications-email/non_envoyees/ \
  -H "Authorization: Bearer TOKEN"
```

---

## 🔍 VÉRIFICATION

### Vérifier qu'une notification a été créée
```bash
python manage.py shell
```

```python
from api.models import NotificationEmail

# Dernières notifications créées
notifications = NotificationEmail.objects.order_by('-date_creation')[:5]
for notif in notifications:
    print(f"ID: {notif.id}")
    print(f"Destinataire: {notif.destinataire.email}")
    print(f"Sujet: {notif.sujet}")
    print(f"Type: {notif.type_notification}")
    print(f"Envoyé: {notif.envoye}")
    print("---")
```

### Vérifier les préférences d'un utilisateur
```python
from api.models import PreferenceNotification, Utilisateur

user = Utilisateur.objects.get(email='m.diallo@etu.bf')
prefs = PreferenceNotification.objects.get(utilisateur=user)

print(f"Email activé: {prefs.activer_email}")
print(f"Notif notes: {prefs.notif_nouvelle_note}")
print(f"Notif évaluations: {prefs.notif_nouvelle_evaluation}")
```

---

## ⏱️ TEMPS ESTIMÉ

- **Intégration dans NoteViewSet**: 5 min
- **Intégration dans EvaluationViewSet**: 5 min
- **Intégration dans PresenceViewSet**: 5 min
- **Intégration dans SupportCoursViewSet**: 5 min
- **Intégration dans EmploiDuTempsViewSet**: 5 min
- **Intégration dans DemandeAdministrativeViewSet**: 5 min
- **Intégration dans MessageViewSet**: 10 min
- **Tests**: 10 min

**Total**: ~50 minutes

---

## ✅ CHECKLIST

- [ ] Intégrer notification dans `NoteViewSet.publier()`
- [ ] Intégrer notification dans `EvaluationViewSet.perform_create()`
- [ ] Intégrer notification dans `PresenceViewSet.perform_create()`
- [ ] Intégrer notification dans `SupportCoursViewSet.perform_create()`
- [ ] Intégrer notification dans `EmploiDuTempsViewSet.perform_update()`
- [ ] Intégrer notification dans `DemandeAdministrativeViewSet.traiter()`
- [ ] Intégrer notification dans `MessageViewSet.perform_create()`
- [ ] Tester chaque intégration
- [ ] Vérifier les logs d'erreur
- [ ] Vérifier que les notifications sont créées
- [ ] Vérifier que les emails sont envoyés (si SMTP configuré)

---

**Date**: 6 mars 2026  
**Temps estimé**: 50 minutes  
**Difficulté**: Facile
