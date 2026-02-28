# 🚀 DÉPLOIEMENT EN 3 ÉTAPES SIMPLES

## 📍 ÉTAPE 1: OUVRIR PYTHONANYWHERE
1. Allez sur: **https://www.pythonanywhere.com**
2. Connectez-vous avec votre compte **Wendlasida**
3. Cliquez sur l'onglet **"Consoles"**
4. Cliquez sur **"Bash"**

---

## 📍 ÉTAPE 2: METTRE À JOUR LE CODE
Dans la console Bash qui s'ouvre, copiez-collez ces commandes **une par une**:

```bash
cd ~/school/backend
```
↓ Appuyez sur Entrée, puis:

```bash
git pull origin main
```
↓ Appuyez sur Entrée

**Vous devriez voir:**
```
Updating 503bc2f..1f75ccc
Fast-forward
 backend/api/models.py | 17 +++++++---
 ...
```

✅ **C'est bon!** Les fichiers sont mis à jour.

---

## 📍 ÉTAPE 3: RECHARGER L'APPLICATION
1. Cliquez sur l'onglet **"Web"** (en haut)
2. Trouvez votre application: **wendlasida.pythonanywhere.com**
3. Cliquez sur le **gros bouton vert "Reload"**
4. Attendez 10-20 secondes

✅ **C'EST FAIT!** 🎉

---

## 🧪 VÉRIFICATION (OPTIONNEL)
Pour vérifier que tout fonctionne, dans la console Bash:

```bash
python verifier_deploiement.py
```

Vous devriez voir tous les tests en ✅

---

## 🎯 TESTER L'APPLICATION

### 1. Ouvrir l'application
https://school-wheat-six.vercel.app

### 2. Se connecter comme PROF
- Email: **j.ouedraogo@uan.bf**
- Password: **enseignant123**

### 3. Aller dans "Saisie des notes"
- Sélectionnez: **Licence 1 Informatique**
- Sélectionnez une matière: **Algorithmique**
- Vous devriez voir **Moussa DIALLO** dans la liste

### 4. Saisir une note
- Note CC: **15**
- Note Examen: **16**
- Moyenne calculée automatiquement: **15.6**
- Cliquez sur **"Publier les notes"**

### 5. Vérifier côté étudiant
- Déconnectez-vous
- Reconnectez-vous avec: **m.diallo@etu.bf** / **etudiant123**
- Vérifiez que les notes apparaissent

---

## ❓ BESOIN D'AIDE?

Si quelque chose ne fonctionne pas:
1. Videz le cache du navigateur: **Ctrl + Shift + R**
2. Vérifiez les logs d'erreur dans PythonAnywhere (onglet Web > Error log)
3. Essayez de recharger l'application une deuxième fois

---

**C'est tout! Simple et rapide! 🚀**
