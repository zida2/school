# 🚀 COMMENT DÉMARRER LE SYSTÈME

Date: 26 février 2026

---

## ✅ MÉTHODE RAPIDE (RECOMMANDÉE)

### Double-cliquez sur: `demarrer_tout.bat`

Ce script va:
1. ✅ Démarrer le backend Django (port 8000)
2. ✅ Démarrer le frontend HTTP (port 8080)
3. ✅ Ouvrir automatiquement le navigateur

**C'est tout!** Le système sera prêt en quelques secondes.

---

## 📋 MÉTHODES ALTERNATIVES

### Méthode 1: Scripts Séparés

**Étape 1:** Double-cliquez sur `demarrer_backend.bat`
- Cela démarre le serveur Django
- Laissez cette fenêtre OUVERTE

**Étape 2:** Double-cliquez sur `demarrer_frontend.bat`
- Cela démarre le serveur frontend
- Laissez cette fenêtre OUVERTE

**Étape 3:** Ouvrez votre navigateur
- Allez sur: http://127.0.0.1:8080/

---

### Méthode 2: Manuellement (Terminal)

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
python -m http.server 8080
```

**Navigateur:**
```
http://127.0.0.1:8080/
```

---

## ⚠️ IMPORTANT

### À FAIRE:
- ✅ Laisser les fenêtres de terminal OUVERTES
- ✅ Ne PAS fermer les fenêtres pendant l'utilisation
- ✅ Utiliser le navigateur pour accéder au système

### À NE PAS FAIRE:
- ❌ Ne fermez PAS les fenêtres de terminal
- ❌ Ne cliquez PAS sur la croix rouge des fenêtres
- ❌ N'appuyez PAS sur CTRL+C dans les terminaux

---

## 🛑 COMMENT ARRÊTER LE SYSTÈME

### Méthode 1: Fermer les Fenêtres
Fermez simplement les fenêtres de terminal (Backend et Frontend)

### Méthode 2: CTRL+C
Dans chaque terminal, appuyez sur `CTRL+C`

---

## 🔍 VÉRIFIER QUE TOUT FONCTIONNE

### Backend (Django)
Ouvrez dans le navigateur: http://127.0.0.1:8000/api/auth/me/

**Résultat attendu:**
```json
{"detail": "Authentication credentials were not provided."}
```

✅ Si vous voyez ce message, le backend fonctionne!

---

### Frontend (HTTP)
Ouvrez dans le navigateur: http://127.0.0.1:8080/

**Résultat attendu:**
Vous devriez voir la page de connexion du système ERP.

✅ Si vous voyez la page, le frontend fonctionne!

---

## 🐛 PROBLÈMES COURANTS

### Problème: "Port already in use"

**Solution:**
1. Fermez toutes les fenêtres de terminal
2. Redémarrez votre ordinateur
3. Relancez `demarrer_tout.bat`

---

### Problème: "Python not found"

**Solution:**
Vérifiez que Python est installé:
```bash
python --version
```

Si Python n'est pas installé, téléchargez-le depuis: https://www.python.org/

---

### Problème: Page blanche ou erreur 404

**Solution:**
1. Vérifiez que vous êtes dans le bon dossier
2. Vérifiez que les fichiers HTML existent
3. Essayez d'ouvrir directement `index.html`

---

## 📞 COMPTES DE TEST

Une fois le système démarré, utilisez ces comptes:

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

## 🎯 RÉSUMÉ RAPIDE

1. **Double-cliquez sur:** `demarrer_tout.bat`
2. **Attendez** que les fenêtres s'ouvrent (5-10 secondes)
3. **Le navigateur s'ouvre** automatiquement
4. **Connectez-vous** avec un compte de test
5. **Profitez** du système!

---

## 📸 CE QUE VOUS DEVRIEZ VOIR

### Fenêtre Backend (Django)
```
Django version 6.0.2, using settings 'erp_backend.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Fenêtre Frontend (HTTP)
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

### Navigateur
La page de connexion du système ERP avec les 4 comptes de test.

---

Date: 26 février 2026
Version: 1.0
Statut: ✅ PRÊT À UTILISER

**Double-cliquez sur `demarrer_tout.bat` et c'est parti!** 🚀

