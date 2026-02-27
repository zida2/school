# 🔧 GUIDE DE DÉPANNAGE - PROBLÈME DE CONNEXION

Date: 26 février 2026

---

## ❌ PROBLÈME

Vous ne pouvez pas vous connecter sur http://127.0.0.1:8080/

---

## ✅ SOLUTION ÉTAPE PAR ÉTAPE

### Étape 1: Démarrer le Serveur Django (OBLIGATOIRE)

Le serveur Django DOIT être démarré pour que la connexion fonctionne!

**Ouvrir un terminal et exécuter:**

```bash
cd backend
python manage.py runserver
```

**Vous devriez voir:**
```
Django version 6.0.2, using settings 'erp_backend.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

⚠️ **IMPORTANT:** Laissez ce terminal ouvert! Le serveur doit rester actif.

---

### Étape 2: Ouvrir le Frontend

**Dans un AUTRE terminal ou navigateur:**

1. Ouvrir: `http://127.0.0.1:8080/` ou ouvrir directement `index.html`
2. Cliquer sur un compte (ex: 👔 Administrateur)
3. Vérifier la connexion

---

### Étape 3: Vérifier que Tout Fonctionne

**Exécuter le script de test:**

```bash
cd backend
python test_login_direct.py
```

**Résultat attendu:**
```
✅ Serveur Django accessible
✅ Étudiant: m.diallo@etu.bf - Password: OK
✅ Bureau: bureau@uan.bf - Password: OK
✅ Enseignant: j.ouedraogo@uan.bf - Password: OK
✅ Admin: admin@uan.bf - Password: OK
```

---

## 🐛 PROBLÈMES COURANTS

### Problème 1: "Serveur Django non accessible"

**Cause:** Le serveur Django n'est pas démarré

**Solution:**
```bash
cd backend
python manage.py runserver
```

---

### Problème 2: "Port 8000 already in use"

**Cause:** Un autre processus utilise le port 8000

**Solution Windows:**
```bash
# Trouver le processus
netstat -ano | findstr :8000

# Tuer le processus (remplacer PID par le numéro trouvé)
taskkill /PID <PID> /F

# Redémarrer le serveur
python manage.py runserver
```

---

### Problème 3: "CORS error" dans la console

**Cause:** Problème de configuration CORS

**Solution:** Vérifier que le serveur Django tourne sur http://127.0.0.1:8000/

---

### Problème 4: "Invalid credentials"

**Cause:** Mot de passe incorrect

**Solution:**
```bash
cd backend
python verifier_tous_comptes.py
```

Cela réinitialisera tous les mots de passe si nécessaire.

---

### Problème 5: Page blanche ou erreur 404

**Cause:** Mauvaise URL ou fichiers manquants

**Solution:**
1. Vérifier que vous êtes dans le bon dossier
2. Ouvrir directement `index.html` dans le navigateur
3. Ou utiliser un serveur HTTP simple:
   ```bash
   python -m http.server 8080
   ```

---

## 🧪 TESTS DE DIAGNOSTIC

### Test 1: Vérifier le Serveur Django

**Ouvrir dans le navigateur:**
```
http://127.0.0.1:8000/api/auth/me/
```

**Résultat attendu:**
```json
{"detail": "Authentication credentials were not provided."}
```

✅ Si vous voyez ce message, le serveur fonctionne!

---

### Test 2: Vérifier les Comptes

**Exécuter:**
```bash
cd backend
python verifier_tous_comptes.py
```

---

### Test 3: Tester la Connexion API

**Exécuter:**
```bash
cd backend
python test_login_direct.py
```

---

## 📋 CHECKLIST DE VÉRIFICATION

Avant de tester la connexion, vérifiez:

- [ ] Le serveur Django est démarré (`python manage.py runserver`)
- [ ] Le terminal du serveur Django est ouvert et actif
- [ ] Vous voyez "Starting development server at http://127.0.0.1:8000/"
- [ ] Vous pouvez accéder à http://127.0.0.1:8000/api/auth/me/
- [ ] Les comptes ont été vérifiés (`python verifier_tous_comptes.py`)
- [ ] Le frontend est accessible (http://127.0.0.1:8080/ ou index.html)

---

## 🎯 PROCÉDURE COMPLÈTE DE DÉMARRAGE

### Méthode 1: Deux Terminaux (RECOMMANDÉ)

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver
```
⚠️ Laisser ce terminal ouvert!

**Terminal 2 - Frontend:**
```bash
# Option A: Serveur HTTP Python
python -m http.server 8080

# Option B: Ouvrir directement
# Double-cliquer sur index.html
```

**Navigateur:**
```
http://127.0.0.1:8080/
```

---

### Méthode 2: Un Terminal + Navigateur

**Terminal - Backend:**
```bash
cd backend
python manage.py runserver
```
⚠️ Laisser ce terminal ouvert!

**Navigateur:**
```
Ouvrir directement: index.html
```

---

## 🔍 VÉRIFIER LA CONSOLE DU NAVIGATEUR

Si la connexion ne fonctionne toujours pas:

1. **Ouvrir la console du navigateur:** Appuyer sur `F12`
2. **Aller dans l'onglet "Console"**
3. **Chercher les erreurs en rouge**

### Erreurs Courantes:

**Erreur:** `Failed to fetch` ou `Network error`
**Solution:** Le serveur Django n'est pas démarré

**Erreur:** `CORS policy` ou `Access-Control-Allow-Origin`
**Solution:** Vérifier que le serveur Django tourne sur http://127.0.0.1:8000/

**Erreur:** `401 Unauthorized` ou `Invalid credentials`
**Solution:** Exécuter `python verifier_tous_comptes.py`

**Erreur:** `404 Not Found`
**Solution:** Vérifier l'URL de l'API dans `js/api.js`

---

## 📞 COMPTES DE TEST

Une fois le serveur démarré, utilisez ces comptes:

### 👨‍🎓 Étudiant
```
Email: m.diallo@etu.bf
Password: etudiant123
```

### 🏛️ Bureau Exécutif
```
Email: bureau@uan.bf
Password: bureau123
```

### 👨‍🏫 Enseignant
```
Email: j.ouedraogo@uan.bf
Password: enseignant123
```

### 👔 Administrateur
```
Email: admin@uan.bf
Password: admin123
```

---

## 🚀 DÉMARRAGE RAPIDE (RÉSUMÉ)

```bash
# 1. Démarrer le backend
cd backend
python manage.py runserver

# 2. Dans un autre terminal ou navigateur
# Ouvrir: http://127.0.0.1:8080/ ou index.html

# 3. Cliquer sur un compte et se connecter
```

---

## 💡 ASTUCES

### Astuce 1: Vérifier que le Serveur Tourne

**Commande rapide:**
```bash
curl http://127.0.0.1:8000/api/auth/me/
```

**Ou dans le navigateur:**
```
http://127.0.0.1:8000/api/auth/me/
```

Si vous voyez une réponse JSON, le serveur fonctionne!

---

### Astuce 2: Logs du Serveur Django

Les logs du serveur Django s'affichent dans le terminal où vous avez lancé `python manage.py runserver`.

**Exemple de logs normaux:**
```
[26/Feb/2026 20:30:15] "POST /api/auth/login/ HTTP/1.1" 200 1234
[26/Feb/2026 20:30:16] "GET /api/auth/me/ HTTP/1.1" 200 567
```

**Exemple de logs d'erreur:**
```
[26/Feb/2026 20:30:15] "POST /api/auth/login/ HTTP/1.1" 401 89
```

---

### Astuce 3: Redémarrer Proprement

Si rien ne fonctionne:

1. **Arrêter le serveur Django:** `CTRL+C` dans le terminal
2. **Vérifier les comptes:**
   ```bash
   python verifier_tous_comptes.py
   ```
3. **Redémarrer le serveur:**
   ```bash
   python manage.py runserver
   ```
4. **Rafraîchir le navigateur:** `F5` ou `CTRL+F5`

---

## ✅ RÉSULTAT ATTENDU

Après avoir suivi ce guide:

1. ✅ Le serveur Django tourne sur http://127.0.0.1:8000/
2. ✅ Le frontend est accessible sur http://127.0.0.1:8080/ ou via index.html
3. ✅ Vous pouvez cliquer sur un compte
4. ✅ La connexion fonctionne
5. ✅ Vous êtes redirigé vers le dashboard

---

## 📧 BESOIN D'AIDE?

Si le problème persiste après avoir suivi ce guide:

1. **Vérifier les logs du serveur Django** (terminal où tourne `python manage.py runserver`)
2. **Vérifier la console du navigateur** (F12 → Console)
3. **Exécuter les scripts de diagnostic:**
   ```bash
   cd backend
   python verifier_tous_comptes.py
   python test_login_direct.py
   ```
4. **Prendre une capture d'écran** des erreurs

---

Date: 26 février 2026
Version: 1.0
Statut: ✅ GUIDE COMPLET

**Le serveur Django DOIT être démarré pour que la connexion fonctionne!** 🚀

