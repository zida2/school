# 🚀 Commandes Finales PythonAnywhere

**Copiez-collez ces commandes une par une dans le terminal PythonAnywhere**

---

## 📋 Commandes à Exécuter

```bash
# 1. Aller dans le dossier backend
cd ~/school/backend

# 2. Récupérer les dernières modifications
git pull origin main

# 3. Voir l'état des migrations
python manage.py showmigrations api

# 4. Fusionner les migrations conflictuelles
python manage.py makemigrations --merge
```

**⚠️ Quand demandé "Do you want to merge these migration branches? [y/N]"**  
**Tapez: y**

```bash
# 5. Marquer toutes les migrations comme appliquées (sans les exécuter)
python manage.py migrate --fake

# 6. Vérifier que tout est OK
python manage.py showmigrations api
```

**✅ Vous devriez voir toutes les migrations avec [X]**

```bash
# 7. Tester l'import des modèles
python manage.py shell
```

**Dans le shell Python, tapez:**
```python
from api.models import Classe, Inscription, EnseignementMatiere
print("✅ Imports OK!")
print("Nombre de classes:", Classe.objects.count())
exit()
```

---

## 🔄 Recharger l'Application

1. Allez dans l'onglet **"Web"** de PythonAnywhere
2. Cliquez sur le bouton **"Reload wendlasida.pythonanywhere.com"**
3. Attendez 5-10 secondes

---

## ✅ Tester les Endpoints

Ouvrez ces URLs dans votre navigateur:

1. **Page d'accueil**:
   ```
   https://wendlasida.pythonanywhere.com/api/
   ```

2. **Classes**:
   ```
   https://wendlasida.pythonanywhere.com/api/classes/
   ```

3. **Enseignements**:
   ```
   https://wendlasida.pythonanywhere.com/api/enseignements/
   ```

4. **Enseignements par Enseignant**:
   ```
   https://wendlasida.pythonanywhere.com/api/enseignements/par_enseignant/
   ```

5. **Finances**:
   ```
   https://wendlasida.pythonanywhere.com/api/finances/statistiques/
   ```

---

## 🎯 Résultat Attendu

- ✅ Toutes les URLs fonctionnent sans erreur
- ✅ Les endpoints retournent des données JSON
- ✅ L'application est opérationnelle

---

## ⚠️ Si Problème

### Si "git pull" échoue

```bash
git stash
git pull origin main
```

### Si l'application ne démarre pas

```bash
# Voir les logs d'erreur
tail -n 50 /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

Ou consultez les logs dans l'onglet "Web" → "Error log"

---

**C'est tout! Après ces étapes, tout devrait fonctionner.** 🎉
