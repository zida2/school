# 🚀 Instructions de Déploiement Backend (PythonAnywhere)

## 📝 Changements à Déployer
- Amélioration du contenu des emails pour professeurs
- Meilleure structure et présentation
- Ajout du matricule dans l'email

## 🔧 Commandes à Exécuter sur PythonAnywhere

### 1. Se connecter à PythonAnywhere
```bash
# Aller sur: https://www.pythonanywhere.com
# Se connecter avec le compte: Wendlasida
```

### 2. Ouvrir un Bash Console
```bash
# Cliquer sur "Consoles" → "Bash"
```

### 3. Mettre à Jour le Code
```bash
cd ~/school/backend
git pull origin main
```

### 4. Recharger l'Application
```bash
# Option 1: Via le bouton "Reload" sur la page Web
# Aller sur: https://www.pythonanywhere.com/user/Wendlasida/webapps/
# Cliquer sur le bouton vert "Reload wendlasida.pythonanywhere.com"

# Option 2: Via la commande
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

## ✅ Vérification

### Tester l'API
```bash
curl https://wendlasida.pythonanywhere.com/api/
```

### Tester une Validation
1. Aller sur: https://school-wheat-six.vercel.app/frontend/connexion-admin.html
2. Se connecter avec: admin@unierp.bf / Admin2026
3. Valider une demande d'inscription professeur
4. Vérifier que l'email reçu a le nouveau format

## 📧 Nouveau Format d'Email

L'email envoyé aux professeurs aura maintenant ce format:

```
Sujet: Bienvenue - Vos identifiants d'accès UniERP BF

Bonjour [Prénom] [Nom],

Félicitations ! Votre candidature en tant qu'enseignant a été acceptée.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VOS IDENTIFIANTS DE CONNEXION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 Email : [email]
🔑 Mot de passe : [password]
🎓 Spécialité : [spécialité]
👤 Matricule : [matricule]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACCÉDER À VOTRE ESPACE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Connectez-vous dès maintenant :
🔗 https://school-wheat-six.vercel.app/frontend/connexion-professeur.html

⚠️ SÉCURITÉ : Changez votre mot de passe dès votre première connexion.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bienvenue dans notre équipe pédagogique !

Cordialement,
L'Administration UniERP BF
Université Aube Nouvelle

---
Cet email a été envoyé automatiquement. Si vous n'êtes pas concerné, veuillez ignorer ce message.
```

## 💡 Conseils pour les Utilisateurs

### Si l'Email Arrive dans les Spams
Demandez aux utilisateurs de:
1. Vérifier le dossier SPAM/COURRIER INDÉSIRABLE
2. Marquer l'email comme "PAS UN SPAM"
3. Ajouter noreply@unierp.bf aux contacts
4. Déplacer l'email vers la boîte de réception

### Améliorer la Délivrabilité
Consultez le fichier `AMELIORER_DELIVRABILITE_EMAILS.md` pour des solutions à long terme.

---

**Date**: 7 mars 2026
**Statut**: Prêt à déployer
