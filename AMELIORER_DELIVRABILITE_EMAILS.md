# 📧 Améliorer la Délivrabilité des Emails

## ✅ Situation Actuelle
Les emails sont envoyés avec succès mais arrivent parfois dans les spams. C'est normal pour un nouveau domaine d'envoi.

## 🎯 Solutions Immédiates (Déjà Appliquées)

### 1. Amélioration du Contenu
- ✅ Sujet clair et professionnel
- ✅ Contenu structuré avec séparateurs
- ✅ Signature complète avec nom de l'institution
- ✅ Disclaimer en bas de l'email
- ✅ Éviter les mots "spam" (gratuit, urgent, cliquez ici, etc.)

### 2. Configuration Gmail
- ✅ Utilisation d'un mot de passe d'application
- ✅ SMTP Gmail configuré correctement
- ✅ TLS activé

## 🚀 Solutions à Moyen Terme

### 1. Configurer SPF, DKIM et DMARC
Si vous avez un nom de domaine (ex: unierp.bf), configurez ces enregistrements DNS:

**SPF (Sender Policy Framework)**
```
Type: TXT
Nom: @
Valeur: v=spf1 include:_spf.google.com ~all
```

**DKIM (DomainKeys Identified Mail)**
- Activez DKIM dans Google Workspace ou Gmail
- Ajoutez l'enregistrement TXT fourni par Google

**DMARC (Domain-based Message Authentication)**
```
Type: TXT
Nom: _dmarc
Valeur: v=DMARC1; p=quarantine; rua=mailto:admin@unierp.bf
```

### 2. Utiliser un Service d'Envoi Professionnel
Pour une meilleure délivrabilité, considérez:

**SendGrid** (Gratuit jusqu'à 100 emails/jour)
```python
# settings.py
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = 'votre_cle_api'
```

**Mailgun** (Gratuit jusqu'à 5000 emails/mois)
```python
# settings.py
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
ANYMAIL = {
    "MAILGUN_API_KEY": "votre_cle_api",
    "MAILGUN_SENDER_DOMAIN": "mg.unierp.bf",
}
```

**Amazon SES** (Très économique)
```python
# settings.py
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'votre_cle'
AWS_SECRET_ACCESS_KEY = 'votre_secret'
AWS_SES_REGION_NAME = 'us-east-1'
```

### 3. Améliorer la Réputation de l'Expéditeur
- Commencez par envoyer peu d'emails (warm-up)
- Augmentez progressivement le volume
- Surveillez le taux de rebond et de plaintes
- Nettoyez régulièrement votre liste d'emails

## 📝 Recommandations aux Utilisateurs

### Pour les Nouveaux Inscrits
Ajoutez ces instructions dans l'email:

```
📌 POUR RECEVOIR NOS EMAILS DANS VOTRE BOÎTE DE RÉCEPTION :

1. Vérifiez votre dossier SPAM/COURRIER INDÉSIRABLE
2. Marquez cet email comme "PAS UN SPAM"
3. Ajoutez noreply@unierp.bf à vos contacts
4. Déplacez cet email vers votre boîte de réception

Cela permettra de recevoir tous nos futurs emails directement.
```

## 🔍 Surveillance

### Vérifier la Délivrabilité
- **Mail-Tester**: https://www.mail-tester.com
  - Envoyez un email de test
  - Obtenez un score sur 10
  - Suivez les recommandations

- **Google Postmaster Tools**: https://postmaster.google.com
  - Surveillez la réputation de votre domaine
  - Analysez les taux de spam

## 💡 Bonnes Pratiques

### Contenu des Emails
- ✅ Ratio texte/HTML équilibré
- ✅ Pas trop d'images
- ✅ Liens HTTPS uniquement
- ✅ Pas de pièces jointes suspectes
- ✅ Signature professionnelle

### Technique
- ✅ Authentification SMTP
- ✅ Connexion TLS/SSL
- ✅ Adresse d'expéditeur cohérente
- ✅ En-têtes corrects

## 🎓 Pour l'Université

### Solution Idéale à Long Terme
1. **Obtenir un domaine professionnel** (ex: unierp.bf)
2. **Configurer Google Workspace** ou **Microsoft 365**
3. **Configurer SPF, DKIM, DMARC**
4. **Utiliser un service d'envoi transactionnel** (SendGrid, Mailgun, SES)

### Budget Estimé
- Domaine: ~15€/an
- Google Workspace: ~6€/utilisateur/mois
- SendGrid/Mailgun: Gratuit jusqu'à 5000-10000 emails/mois

## 📊 Statistiques Actuelles

### Configuration Actuelle
- **Service**: Gmail SMTP
- **Email**: zidadesire20@gmail.com
- **Port**: 587 (TLS)
- **Statut**: ✅ Fonctionnel

### Taux de Délivrabilité Attendu
- Boîte de réception: ~60-70%
- Spam: ~30-40%
- Rebond: <5%

Avec les améliorations proposées, on peut atteindre:
- Boîte de réception: ~95%
- Spam: ~5%
- Rebond: <1%

## 🔧 Actions Immédiates

1. ✅ **Améliorer le contenu des emails** (FAIT)
2. 📝 **Demander aux utilisateurs d'ajouter l'email aux contacts**
3. 📧 **Envoyer un email de test à mail-tester.com**
4. 📊 **Surveiller les retours utilisateurs**

## 📞 Support

Si les emails continuent d'arriver dans les spams:
1. Vérifiez que l'utilisateur a bien reçu l'email (même dans spam)
2. Demandez-lui de marquer comme "Pas un spam"
3. Demandez-lui d'ajouter l'adresse aux contacts
4. Les prochains emails arriveront dans la boîte de réception

---

**Date**: 7 mars 2026
**Statut**: En amélioration continue
