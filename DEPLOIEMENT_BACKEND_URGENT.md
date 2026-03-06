# 🚨 DÉPLOIEMENT BACKEND URGENT

## ❌ PROBLÈME ACTUEL

L'inscription affiche "Erreur de connexion au serveur" car:
- ✅ Frontend déployé sur Vercel
- ❌ Backend PAS ENCORE déployé sur PythonAnywhere
- ❌ Migration 0016 pas appliquée sur le serveur

## 📋 COMMANDES À EXÉCUTER SUR PYTHONANYWHERE

### 1. Se connecter à PythonAnywhere
URL: https://www.pythonanywhere.com/user/wendlasida/

### 2. Ouvrir un Bash Console

### 3. Copier-coller ces commandes:

```bash
# Naviguer vers le projet
cd ~/school/backend

# Pull les modifications
git pull origin main

# Appliquer la migration 0016
python manage.py migrate

# Vérifier qu'il n'y a pas d'erreurs
python manage.py check

# Redémarrer l'application
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py

# Vérifier les migrations appliquées
python manage.py showmigrations api
```

## ✅ RÉSULTAT ATTENDU

Après ces commandes:
```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, sessions, token_blacklist
Running migrations:
  Applying api.0016_ajout_services_administratifs... OK

System check identified no issues (0 silenced).
```

## 🧪 TEST APRÈS DÉPLOIEMENT

### Test 1: API accessible
```bash
curl https://wendlasida.pythonanywhere.com/api/
```

### Test 2: Inscription Communication
```bash
curl -X POST https://wendlasida.pythonanywhere.com/api/demandes-inscription-communication/ \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Test",
    "prenom": "User",
    "email": "test@example.com",
    "telephone": "70000000",
    "poste_souhaite": "Chargé de communication"
  }'
```

### Test 3: Frontend
1. Ouvrir: https://school-wheat-six.vercel.app/inscription-communication.html
2. Remplir le formulaire
3. Vérifier: Message de succès au lieu de "Erreur de connexion"

## 📊 SYSTÈME D'INSCRIPTION

### Comment ça fonctionne:

1. **Utilisateur remplit le formulaire** (sans mot de passe)
   - Nom, Prénom, Email, Téléphone, Poste souhaité

2. **Données envoyées à l'API**
   - POST vers `/api/demandes-inscription-{service}/`
   - Statut: `en_attente`

3. **Admin valide la demande**
   - Se connecte sur Django Admin
   - Valide la demande
   - Système génère automatiquement:
     - Compte utilisateur
     - Mot de passe temporaire
     - Email envoyé (TODO)

4. **Utilisateur reçoit email**
   - Email avec identifiants
   - Mot de passe temporaire
   - Lien de connexion

5. **Utilisateur se connecte**
   - Va sur page de connexion
   - Entre email + mot de passe temporaire
   - Accède à son dashboard

## 🔐 SÉCURITÉ

- ✅ Pas de mot de passe dans le formulaire d'inscription
- ✅ Mot de passe généré automatiquement par le système
- ✅ Validation admin obligatoire
- ✅ Email unique (pas de doublons)

## ⏱️ TEMPS ESTIMÉ

- Déploiement backend: 5 minutes
- Tests: 2 minutes
- **TOTAL: 7 minutes**

## 🎯 APRÈS DÉPLOIEMENT

Le système sera 100% opérationnel:
- ✅ Inscriptions fonctionnent
- ✅ Données sauvegardées en base
- ✅ Validation admin possible
- ✅ Création comptes automatique

**DÉPLOYER MAINTENANT! 🚀**
