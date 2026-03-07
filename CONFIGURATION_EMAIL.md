# 📧 Configuration Email - UniERP BF

## 🎯 Objectif

Configurer l'envoi automatique d'emails pour:
- ✅ Envoi des identifiants aux nouveaux utilisateurs (étudiants, professeurs, services)
- ✅ Notifications système
- ✅ Emploi du temps aux professeurs

## 📋 Étape 1: Créer un compte Gmail dédié (Recommandé)

### Option A: Utiliser un compte Gmail existant
Si vous avez déjà un compte Gmail pour l'université, passez à l'étape 2.

### Option B: Créer un nouveau compte Gmail
1. Aller sur https://accounts.google.com/signup
2. Créer un compte avec un email professionnel:
   - Exemple: `unierp.notifications@gmail.com`
   - Ou: `noreply@votre-universite.bf` (si domaine configuré)

## 🔐 Étape 2: Générer un mot de passe d'application Gmail

### ⚠️ IMPORTANT: Ne PAS utiliser votre mot de passe Gmail normal!

1. **Activer la validation en 2 étapes**
   - Aller sur: https://myaccount.google.com/security
   - Cliquer sur "Validation en 2 étapes"
   - Suivre les instructions pour l'activer

2. **Générer un mot de passe d'application**
   - Aller sur: https://myaccount.google.com/apppasswords
   - Sélectionner "Mail" comme application
   - Sélectionner "Autre" comme appareil
   - Nommer: "UniERP Backend"
   - Cliquer sur "Générer"
   - **Copier le mot de passe de 16 caractères** (format: xxxx xxxx xxxx xxxx)

## ⚙️ Étape 3: Configurer le backend

### Fichier: `backend/.env`

```env
# ===== CONFIGURATION EMAIL =====
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=unierp.notifications@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
DEFAULT_FROM_EMAIL=noreply@unierp.bf
FRONTEND_URL=https://school-wheat-six.vercel.app
```

### Remplacer:
- `EMAIL_HOST_USER`: Votre email Gmail complet
- `EMAIL_HOST_PASSWORD`: Le mot de passe d'application de 16 caractères (avec ou sans espaces)
- `DEFAULT_FROM_EMAIL`: L'email qui apparaîtra comme expéditeur
- `FRONTEND_URL`: L'URL de votre frontend

## 🧪 Étape 4: Tester l'envoi d'emails

### Test 1: Via le shell Django

```bash
cd backend
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

# Test simple
send_mail(
    subject='Test UniERP',
    message='Ceci est un email de test du système UniERP.',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['votre-email-test@gmail.com'],
    fail_silently=False,
)

print("✅ Email envoyé avec succès!")
```

### Test 2: Via une inscription professeur

1. Aller sur: `frontend/inscription-professeur.html`
2. Remplir le formulaire avec votre email
3. Se connecter en tant qu'admin
4. Valider la demande
5. Vérifier la réception de l'email avec les identifiants

## 🔧 Étape 5: Configuration PythonAnywhere (Production)

### Fichier: `backend/.env` sur PythonAnywhere

```bash
# Se connecter à PythonAnywhere
ssh username@ssh.pythonanywhere.com

# Éditer le fichier .env
cd ~/school/backend
nano .env
```

Ajouter les mêmes variables:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=unierp.notifications@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
DEFAULT_FROM_EMAIL=noreply@unierp.bf
FRONTEND_URL=https://school-wheat-six.vercel.app
```

Redémarrer l'application:
```bash
# Via le dashboard PythonAnywhere
# Aller dans l'onglet "Web"
# Cliquer sur "Reload"
```

## 🐳 Étape 6: Configuration Docker

### Fichier: `.env` (racine du projet)

```env
# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=unierp.notifications@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
DEFAULT_FROM_EMAIL=noreply@unierp.bf
FRONTEND_URL=http://localhost
```

Redémarrer Docker:
```bash
docker compose down
docker compose up -d
```

## 📧 Format des emails envoyés

### Email de validation professeur
```
De: noreply@unierp.bf
À: professeur@email.com
Sujet: Inscription validée - Accès Professeur UniERP

Bonjour [Prénom] [Nom],

Votre demande d'inscription en tant qu'enseignant a été validée !

Voici vos identifiants de connexion :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email : professeur@email.com
🔑 Mot de passe : prof12345678
🎓 Spécialité : Mathématiques
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANT : Veuillez changer votre mot de passe lors de votre première connexion.

Vous pouvez vous connecter à votre espace enseignant :
👉 https://school-wheat-six.vercel.app/frontend/connexion-professeur.html

Bienvenue dans l'équipe pédagogique !

Cordialement,
L'équipe UniERP BF
```

### Email de validation étudiant
```
De: noreply@unierp.bf
À: etudiant@email.com
Sujet: Inscription validée - Vos identifiants UniERP

Bonjour [Prénom] [Nom],

Votre demande d'inscription a été approuvée avec succès !

Voici vos identifiants de connexion :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email : etudiant@email.com
🔑 Mot de passe : etudiant2026
🎓 Matricule : 2026INFO0001
🏫 Filière : Licence Informatique
📚 Niveau : L1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANT : Pour votre sécurité, veuillez changer votre mot de passe lors de votre première connexion.

Vous pouvez vous connecter à votre espace étudiant via l'application mobile :
👉 https://school-wheat-six.vercel.app/mobile/

Bienvenue à l'université !

Cordialement,
L'équipe UniERP BF
```

## 🐛 Dépannage

### Erreur: "SMTPAuthenticationError"
- ✅ Vérifier que la validation en 2 étapes est activée
- ✅ Générer un nouveau mot de passe d'application
- ✅ Copier le mot de passe sans espaces ou avec espaces (les deux fonctionnent)

### Erreur: "SMTPException: STARTTLS extension not supported"
- ✅ Vérifier `EMAIL_USE_TLS=True`
- ✅ Vérifier `EMAIL_PORT=587`

### Les emails ne sont pas reçus
- ✅ Vérifier le dossier spam
- ✅ Vérifier que l'email destinataire est correct
- ✅ Tester avec un autre email
- ✅ Vérifier les logs: `docker compose logs backend` ou logs PythonAnywhere

### Erreur: "Connection refused"
- ✅ Vérifier la connexion internet du serveur
- ✅ Vérifier que le port 587 n'est pas bloqué par le pare-feu

## 🔒 Sécurité

### ⚠️ NE JAMAIS:
- ❌ Commiter le fichier `.env` avec les vrais identifiants
- ❌ Partager le mot de passe d'application
- ❌ Utiliser le mot de passe Gmail normal

### ✅ TOUJOURS:
- ✅ Utiliser un mot de passe d'application Gmail
- ✅ Garder `.env` dans `.gitignore`
- ✅ Utiliser des variables d'environnement en production
- ✅ Changer le mot de passe si compromis

## 📊 Alternatives à Gmail

### Option 1: SendGrid (Recommandé pour production)
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=votre-api-key-sendgrid
```

### Option 2: Mailgun
```env
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=postmaster@votre-domaine.mailgun.org
EMAIL_HOST_PASSWORD=votre-mot-de-passe-mailgun
```

### Option 3: Serveur SMTP de l'université
Si votre université a son propre serveur SMTP:
```env
EMAIL_HOST=smtp.universite.bf
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@universite.bf
EMAIL_HOST_PASSWORD=mot-de-passe-fourni
```

## ✅ Checklist finale

- [ ] Compte Gmail créé ou existant
- [ ] Validation en 2 étapes activée
- [ ] Mot de passe d'application généré
- [ ] Fichier `.env` configuré
- [ ] Test d'envoi réussi
- [ ] Configuration production (PythonAnywhere/Docker)
- [ ] Emails reçus correctement
- [ ] Pas de spam

---

**Configuration terminée!** 🎉

Les emails seront maintenant envoyés automatiquement lors de:
- Validation d'inscription étudiant
- Validation d'inscription professeur
- Validation d'inscription services administratifs
- Envoi d'emploi du temps aux professeurs
