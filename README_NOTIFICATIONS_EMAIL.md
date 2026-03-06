# 📧 SYSTÈME DE NOTIFICATIONS EMAIL

## 🎯 DESCRIPTION

Système complet de notifications par email pour informer les utilisateurs de toutes les actions académiques importantes.

---

## ✨ FONCTIONNALITÉS

### Types de Notifications
1. **Nouvelle note publiée** - L'étudiant reçoit un email quand ses notes sont publiées
2. **Nouvelle évaluation** - Les étudiants sont notifiés des nouvelles évaluations
3. **Absence enregistrée** - L'étudiant est notifié de son absence
4. **Nouveau support de cours** - Les étudiants reçoivent les nouveaux supports
5. **Emploi du temps modifié** - Notification des changements d'emploi du temps
6. **Demande traitée** - L'étudiant est notifié du traitement de sa demande
7. **Message dans un canal** - Notification des nouveaux messages
8. **Annonce officielle** - Notification des annonces importantes

### Préférences Utilisateur
- Chaque utilisateur peut activer/désactiver les notifications par type
- Activation/désactivation globale des notifications email
- Préférences sauvegardées et persistantes

---

## 🚀 UTILISATION

### Pour les Utilisateurs

#### Consulter mes préférences
```
GET /api/preferences-notification/mes_preferences/
```

#### Modifier mes préférences
```
PATCH /api/preferences-notification/modifier_preferences/
{
  "notif_nouvelle_note": false,
  "notif_absence": false
}
```

#### Consulter mes notifications
```
GET /api/notifications-email/
```

### Pour les Administrateurs

#### Liste de toutes les notifications
```
GET /api/notifications-email/
```

#### Notifications non envoyées
```
GET /api/notifications-email/non_envoyees/
```

#### Renvoyer une notification
```
POST /api/notifications-email/{id}/renvoyer/
```

---

## 🔧 CONFIGURATION

### Configuration Email (Optionnel)

Par défaut, les emails sont affichés dans la console. Pour envoyer de vrais emails:

1. Créer un fichier `.env` dans `backend/`:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
DEFAULT_FROM_EMAIL=noreply@uan.bf
```

2. Pour Gmail, créer un "Mot de passe d'application":
   - Aller sur https://myaccount.google.com/security
   - Activer la validation en 2 étapes
   - Créer un mot de passe d'application
   - Utiliser ce mot de passe dans `EMAIL_HOST_PASSWORD`

3. Redémarrer l'application

---

## 📊 MODÈLES DE DONNÉES

### NotificationEmail
```python
{
  "id": 1,
  "destinataire": 1,                    # ID de l'utilisateur
  "sujet": "Nouvelle note publiée",
  "contenu": "Votre note en Mathématiques est disponible...",
  "type_notification": "nouvelle_note",
  "envoye": false,
  "date_creation": "2026-03-06T10:00:00Z",
  "date_envoi": null
}
```

### PreferenceNotification
```python
{
  "id": 1,
  "utilisateur": 1,
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

---

## 🔐 PERMISSIONS

### NotificationEmail
- **Liste/Détail**: Utilisateur authentifié (voit uniquement ses notifications)
- **Création/Modification/Suppression**: Admin uniquement
- **Actions spéciales**: Admin uniquement

### PreferenceNotification
- **Liste/Détail**: Utilisateur authentifié (voit uniquement ses préférences)
- **Création/Modification**: Utilisateur authentifié (modifie uniquement ses préférences)
- **Suppression**: Admin uniquement

---

## 📝 EXEMPLES D'UTILISATION

### Exemple 1: Récupérer mes préférences
```javascript
fetch('https://wendlasida.pythonanywhere.com/api/preferences-notification/mes_preferences/', {
  headers: {
    'Authorization': 'Bearer ' + token
  }
})
.then(response => response.json())
.then(data => {
  console.log('Mes préférences:', data);
});
```

### Exemple 2: Désactiver les notifications de notes
```javascript
fetch('https://wendlasida.pythonanywhere.com/api/preferences-notification/modifier_preferences/', {
  method: 'PATCH',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    notif_nouvelle_note: false
  })
})
.then(response => response.json())
.then(data => {
  console.log('Préférences mises à jour:', data);
});
```

### Exemple 3: Consulter mes notifications
```javascript
fetch('https://wendlasida.pythonanywhere.com/api/notifications-email/', {
  headers: {
    'Authorization': 'Bearer ' + token
  }
})
.then(response => response.json())
.then(data => {
  console.log('Mes notifications:', data.results);
});
```

---

## 🧪 TESTS

### Test du système
```bash
cd ~/school/backend
source ~/.virtualenvs/myenv/bin/activate
python tester_notifications_email.py
```

### Test des endpoints
```bash
# Récupérer mes préférences
curl -X GET https://wendlasida.pythonanywhere.com/api/preferences-notification/mes_preferences/ \
  -H "Authorization: Bearer TOKEN"

# Modifier mes préférences
curl -X PATCH https://wendlasida.pythonanywhere.com/api/preferences-notification/modifier_preferences/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"notif_nouvelle_note": false}'

# Consulter mes notifications
curl -X GET https://wendlasida.pythonanywhere.com/api/notifications-email/ \
  -H "Authorization: Bearer TOKEN"
```

---

## 🐛 DÉPANNAGE

### Les notifications ne sont pas créées
1. Vérifier que les migrations sont appliquées: `python manage.py migrate`
2. Vérifier que les préférences existent: `python tester_notifications_email.py`
3. Vérifier les logs: `tail -f /var/log/wendlasida.pythonanywhere.com.error.log`

### Les emails ne sont pas envoyés
1. Vérifier la configuration email dans `.env`
2. Vérifier que `EMAIL_BACKEND` est configuré sur SMTP
3. Vérifier que le mot de passe d'application Gmail est correct
4. Vérifier les logs d'erreur

### Les préférences ne sont pas sauvegardées
1. Vérifier que l'utilisateur est authentifié
2. Vérifier que les données envoyées sont valides
3. Vérifier les logs d'erreur

---

## 📚 DOCUMENTATION

- **Documentation détaillée**: `TRAVAIL_TERMINE_NOTIFICATIONS_EMAIL.md`
- **Guide de déploiement**: `COMMANDES_DEPLOIEMENT_NOTIFICATIONS.md`
- **Guide d'intégration**: `GUIDE_INTEGRATION_NOTIFICATIONS.md`
- **Résumé final**: `RESUME_FINAL_TRAVAIL.md`

---

## 🔗 LIENS UTILES

- **Backend**: https://wendlasida.pythonanywhere.com
- **Frontend**: https://school-wheat-six.vercel.app
- **API Docs**: https://wendlasida.pythonanywhere.com/api/

---

## 📞 SUPPORT

Pour toute question ou problème:
1. Consulter la documentation dans les fichiers `.md`
2. Exécuter `python tester_notifications_email.py`
3. Vérifier les logs d'erreur
4. Contacter l'équipe de développement

---

**Version**: 1.0.0  
**Date**: 6 mars 2026  
**Statut**: ✅ Production Ready
