# 🚀 COMMANDES DE DÉPLOIEMENT - Notifications Email

## 📋 ÉTAPES DE DÉPLOIEMENT

### 1️⃣ Connexion à PythonAnywhere
```bash
# Se connecter via SSH ou utiliser la console Bash de PythonAnywhere
```

### 2️⃣ Activer l'environnement virtuel
```bash
cd ~/school/backend
source ~/.virtualenvs/myenv/bin/activate
```

### 3️⃣ Vérifier les fichiers modifiés
```bash
# Vérifier que les fichiers sont bien synchronisés
ls -la api/serializers.py
ls -la api/views.py
ls -la api/urls.py
ls -la api/admin.py
ls -la api/email_service.py
ls -la api/migrations/0010_notification_email.py
```

### 4️⃣ Appliquer les migrations
```bash
python manage.py migrate
```

**Résultat attendu:**
```
Running migrations:
  Applying api.0010_notification_email... OK
```

### 5️⃣ Tester le système de notifications
```bash
python tester_notifications_email.py
```

**Résultat attendu:**
```
🧪 Test du système de notifications email

1️⃣ Vérification des modèles...
   ✅ 0 notifications email dans la base
   ✅ 0 préférences de notification dans la base

2️⃣ Création des préférences par défaut...
   ✅ X nouvelles préférences créées
   ✅ Total: X préférences

3️⃣ Test de création d'une notification...
   ✅ Notification créée: ID=1
   📧 Destinataire: admin@uan.bf
   📝 Sujet: Test de notification

4️⃣ Statistiques:
   📊 Total notifications: 1
   ✉️ Envoyées: 0
   ⏳ En attente: 1
   👥 Utilisateurs avec préférences: X

5️⃣ Types de notifications disponibles:
   • nouvelle_note: Nouvelle note publiée
   • nouvelle_evaluation: Nouvelle évaluation disponible
   • absence: Absence enregistrée
   • nouveau_support: Nouveau support de cours
   • emploi_modifie: Emploi du temps modifié
   • demande_traitee: Demande administrative traitée
   • message_canal: Nouveau message dans un canal
   • annonce_officielle: Nouvelle annonce officielle
   • autre: Autre notification

✅ Test terminé!
```

### 6️⃣ Redémarrer l'application
```bash
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

### 7️⃣ Vérifier les logs
```bash
# Vérifier les logs d'erreur
tail -f /var/log/wendlasida.pythonanywhere.com.error.log

# Vérifier les logs d'accès
tail -f /var/log/wendlasida.pythonanywhere.com.access.log
```

---

## 🧪 TESTS API

### Test 1: Récupérer mes préférences
```bash
curl -X GET https://wendlasida.pythonanywhere.com/api/preferences-notification/mes_preferences/ \
  -H "Authorization: Bearer VOTRE_TOKEN"
```

**Résultat attendu:**
```json
{
  "id": 1,
  "utilisateur": 1,
  "utilisateur_nom": "Admin User",
  "utilisateur_email": "admin@uan.bf",
  "activer_email": true,
  "notif_nouvelle_note": true,
  "notif_nouvelle_evaluation": true,
  "notif_absence": true,
  "notif_nouveau_support": true,
  "notif_emploi_modifie": true,
  "notif_demande_traitee": true,
  "notif_message_canal": true,
  "notif_annonce_officielle": true
}
```

### Test 2: Modifier mes préférences
```bash
curl -X PATCH https://wendlasida.pythonanywhere.com/api/preferences-notification/modifier_preferences/ \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notif_nouvelle_note": false,
    "notif_absence": false
  }'
```

### Test 3: Liste des notifications email
```bash
curl -X GET https://wendlasida.pythonanywhere.com/api/notifications-email/ \
  -H "Authorization: Bearer VOTRE_TOKEN"
```

### Test 4: Notifications non envoyées
```bash
curl -X GET https://wendlasida.pythonanywhere.com/api/notifications-email/non_envoyees/ \
  -H "Authorization: Bearer VOTRE_TOKEN"
```

---

## ⚙️ CONFIGURATION EMAIL (Optionnel)

### Créer un fichier .env
```bash
cd ~/school/backend
nano .env
```

### Ajouter la configuration email
```env
# Configuration Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
DEFAULT_FROM_EMAIL=noreply@uan.bf
```

**Note**: Pour Gmail, vous devez créer un "Mot de passe d'application":
1. Aller sur https://myaccount.google.com/security
2. Activer la validation en 2 étapes
3. Créer un mot de passe d'application
4. Utiliser ce mot de passe dans `EMAIL_HOST_PASSWORD`

### Redémarrer après configuration
```bash
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

---

## 🔍 VÉRIFICATIONS

### Vérifier que les modèles sont créés
```bash
python manage.py shell
```

```python
from api.models import NotificationEmail, PreferenceNotification

# Compter les notifications
print(f"Notifications: {NotificationEmail.objects.count()}")

# Compter les préférences
print(f"Préférences: {PreferenceNotification.objects.count()}")

# Créer une notification de test
from api.email_service import creer_notification_email
from api.models import Utilisateur

admin = Utilisateur.objects.filter(role='admin').first()
if admin:
    notif = creer_notification_email(
        destinataire=admin,
        sujet="Test",
        contenu="Test de notification",
        type_notification='autre'
    )
    print(f"Notification créée: {notif.id}")

exit()
```

### Vérifier les routes
```bash
python manage.py show_urls | grep notification
```

**Résultat attendu:**
```
/api/notifications-email/
/api/notifications-email/<pk>/
/api/notifications-email/non_envoyees/
/api/notifications-email/<pk>/renvoyer/
/api/preferences-notification/
/api/preferences-notification/<pk>/
/api/preferences-notification/mes_preferences/
/api/preferences-notification/modifier_preferences/
```

---

## ❌ DÉPANNAGE

### Erreur: "No module named 'api.email_service'"
```bash
# Vérifier que le fichier existe
ls -la api/email_service.py

# Si le fichier n'existe pas, le créer à partir du code source
```

### Erreur: "Table 'api_notificationemail' doesn't exist"
```bash
# Appliquer les migrations
python manage.py migrate

# Si ça ne fonctionne pas, créer la migration manuellement
python manage.py makemigrations api
python manage.py migrate
```

### Erreur: "SMTPAuthenticationError"
```bash
# Vérifier la configuration email dans .env
# Vérifier que le mot de passe d'application est correct
# Vérifier que la validation en 2 étapes est activée sur Gmail
```

### Les notifications ne s'envoient pas
```bash
# Vérifier le backend email
python manage.py shell
```

```python
from django.conf import settings
print(settings.EMAIL_BACKEND)
# Si c'est 'console', les emails s'affichent dans la console
# Si c'est 'smtp', les emails sont envoyés par SMTP
```

---

## 📊 COMMANDES UTILES

### Créer des préférences pour tous les utilisateurs
```bash
python manage.py shell
```

```python
from api.models import Utilisateur, PreferenceNotification

for user in Utilisateur.objects.all():
    PreferenceNotification.objects.get_or_create(
        utilisateur=user,
        defaults={
            'activer_email': True,
            'notif_nouvelle_note': True,
            'notif_nouvelle_evaluation': True,
            'notif_absence': True,
            'notif_nouveau_support': True,
            'notif_emploi_modifie': True,
            'notif_demande_traitee': True,
            'notif_message_canal': True,
            'notif_annonce_officielle': True
        }
    )

print(f"Préférences créées: {PreferenceNotification.objects.count()}")
exit()
```

### Envoyer toutes les notifications en attente
```bash
python manage.py shell
```

```python
from api.models import NotificationEmail
from api.email_service import envoyer_notification_email

notifications = NotificationEmail.objects.filter(envoye=False)
print(f"Notifications à envoyer: {notifications.count()}")

for notif in notifications:
    try:
        envoyer_notification_email(notif.id)
        print(f"✅ Notification {notif.id} envoyée")
    except Exception as e:
        print(f"❌ Erreur notification {notif.id}: {e}")

exit()
```

### Supprimer toutes les notifications de test
```bash
python manage.py shell
```

```python
from api.models import NotificationEmail

# Supprimer les notifications de test
NotificationEmail.objects.filter(type_notification='autre').delete()

# Ou supprimer toutes les notifications
# NotificationEmail.objects.all().delete()

exit()
```

---

## ✅ CHECKLIST DE DÉPLOIEMENT

- [ ] Connexion à PythonAnywhere
- [ ] Activation de l'environnement virtuel
- [ ] Vérification des fichiers synchronisés
- [ ] Application des migrations
- [ ] Test du système de notifications
- [ ] Redémarrage de l'application
- [ ] Vérification des logs
- [ ] Test des endpoints API
- [ ] Configuration email (optionnel)
- [ ] Création des préférences pour tous les utilisateurs
- [ ] Vérification finale

---

**Date**: 6 mars 2026  
**Backend**: https://wendlasida.pythonanywhere.com  
**Frontend**: https://school-wheat-six.vercel.app
