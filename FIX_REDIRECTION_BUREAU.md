# 🔧 Fix: Redirection Bureau Exécutif

**Date**: 28 février 2026  
**Problème**: Le bureau exécutif ne redirige pas après connexion

---

## ❌ Problème

Après connexion avec le compte bureau exécutif (`bureau@uan.bf`), la redirection vers `dashboard-bureau.html` ne fonctionnait pas.

**Console**:
```
🚀 Redirection vers dashboard pour rôle: bureau
```

Mais pas de redirection effective.

---

## 🔍 Cause

Le backend retourne le rôle `"bureau"` mais le frontend cherchait uniquement `"bureau_executif"`.

**Code problématique** (index.html):
```javascript
} else if (role === 'bureau_executif') {
    console.log('➡️ Redirection vers dashboard-bureau.html');
    window.location.href = 'dashboard-bureau.html';
}
```

**Résultat**: Aucune condition ne correspondait, donc pas de redirection.

---

## ✅ Solution

Ajout du support pour les deux variantes du rôle: `"bureau"` et `"bureau_executif"`.

### 1. index.html - Redirection après login

**Avant**:
```javascript
} else if (role === 'bureau_executif') {
    console.log('➡️ Redirection vers dashboard-bureau.html');
    window.location.href = 'dashboard-bureau.html';
}
```

**Après**:
```javascript
} else if (role === 'bureau_executif' || role === 'bureau') {
    console.log('➡️ Redirection vers dashboard-bureau.html');
    window.location.href = 'dashboard-bureau.html';
} else {
    console.warn('⚠️ Rôle non reconnu:', role);
    showAlert('Rôle non reconnu. Contactez l\'administrateur.', 'warning');
}
```

**Améliorations**:
- ✅ Support de `"bureau"` et `"bureau_executif"`
- ✅ Message d'erreur si rôle non reconnu

### 2. js/fix-navigation.js - Vérification des permissions

**Avant**:
```javascript
if (role === 'bureau_executif') return userRole === 'bureau_executif';
```

**Après**:
```javascript
if (role === 'bureau_executif') return userRole === 'bureau_executif' || userRole === 'bureau';
if (role === 'bureau') return userRole === 'bureau_executif' || userRole === 'bureau';
```

**Résultat**: Les deux variantes sont acceptées pour l'authentification.

---

## 🎯 Rôles Supportés

### Tous les Rôles avec Variantes

| Rôle Principal | Variantes Acceptées |
|----------------|---------------------|
| `admin` | `admin`, `administrateur` |
| `superadmin` | `superadmin` |
| `professeur` | `professeur`, `enseignant` |
| `enseignant` | `enseignant`, `professeur` |
| `etudiant` | `etudiant` |
| `bureau_executif` | `bureau_executif`, `bureau` |

---

## 🧪 Test

### Avant le Fix

1. Se connecter avec `bureau@uan.bf` / `bureau123`
2. Console: "Redirection vers dashboard pour rôle: bureau"
3. ❌ Pas de redirection
4. Reste sur la page de login

### Après le Fix

1. Se connecter avec `bureau@uan.bf` / `bureau123`
2. Console: "Redirection vers dashboard pour rôle: bureau"
3. Console: "➡️ Redirection vers dashboard-bureau.html"
4. ✅ Redirection vers `dashboard-bureau.html`

---

## 📋 Fichiers Modifiés

1. **index.html**
   - Ajout support `role === 'bureau'`
   - Ajout message d'erreur pour rôles non reconnus

2. **js/fix-navigation.js**
   - Ajout support `userRole === 'bureau'`
   - Vérification bidirectionnelle

---

## 🔄 Déploiement

### Frontend (Vercel)

Le déploiement se fait automatiquement via GitHub:
1. Push effectué ✅
2. Vercel détecte le changement
3. Déploiement automatique
4. Attendre 1-2 minutes
5. Vider le cache: `Ctrl + Shift + R`

### Test

1. Ouvrir: https://school-wheat-six.vercel.app
2. Se connecter avec `bureau@uan.bf` / `bureau123`
3. Vérifier la redirection vers `dashboard-bureau.html`

---

## 💡 Pourquoi Deux Variantes?

Le backend Django utilise `bureau_executif` dans le modèle `Utilisateur.ROLES`, mais certaines parties du code peuvent retourner `bureau` (version courte).

**Solution**: Supporter les deux pour éviter les problèmes de redirection.

---

## ⚠️ Note Importante

Si vous rencontrez toujours le problème:

1. **Vider le cache du navigateur**:
   - Chrome/Edge: `Ctrl + Shift + R`
   - Firefox: `Ctrl + F5`

2. **Vérifier la console**:
   - Ouvrir DevTools (F12)
   - Onglet Console
   - Chercher "Redirection vers dashboard pour rôle:"
   - Vérifier le rôle retourné

3. **Vérifier le backend**:
   ```bash
   python manage.py shell
   ```
   ```python
   from api.models import Utilisateur
   user = Utilisateur.objects.get(email='bureau@uan.bf')
   print(user.role)  # Doit afficher 'bureau_executif' ou 'bureau'
   ```

---

## 🎉 Résultat

- ✅ Redirection bureau exécutif fonctionne
- ✅ Support des deux variantes de rôle
- ✅ Message d'erreur pour rôles non reconnus
- ✅ Code plus robuste

---

**Commit**: `41246ce` - Fix: Redirection bureau exécutif (support 'bureau' et 'bureau_executif') 🔧

**Le problème est résolu!** 🚀
