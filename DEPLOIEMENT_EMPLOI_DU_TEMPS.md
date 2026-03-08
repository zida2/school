# 🚀 Déploiement Emploi du Temps Visuel

## 📋 Checklist de Déploiement

### ✅ Fichiers Créés/Modifiés

#### Frontend
- ✅ `frontend/css/emploi-temps-grid.css` - Nouveau fichier
- ✅ `frontend/js/emploi-temps-grid.js` - Nouveau fichier
- ✅ `frontend/dashboard-admin.html` - Modifié (section emploi + head)

#### Backend
- ✅ `backend/api/models.py` - Modifié (EmploiDuTemps)
- ✅ `backend/api/migrations/0017_emploidutemps_classe_emploidutemps_type_cours.py` - Nouveau

#### Documentation
- ✅ `INTEGRATION_EMPLOI_DU_TEMPS_VISUEL.md` - Nouveau
- ✅ `DEPLOIEMENT_EMPLOI_DU_TEMPS.md` - Ce fichier

## 🔧 Instructions de Déploiement

### 1. Frontend (Vercel)

Les fichiers frontend sont déjà prêts. Vercel déploiera automatiquement après le push Git.

```bash
# Vérifier les fichiers modifiés
git status

# Ajouter les fichiers
git add frontend/css/emploi-temps-grid.css
git add frontend/js/emploi-temps-grid.js
git add frontend/dashboard-admin.html

# Commit
git commit -m "feat: Ajout emploi du temps visuel avec grille interactive"

# Push
git push origin main
```

Vercel déploiera automatiquement sur: https://school-wheat-six.vercel.app

### 2. Backend (PythonAnywhere)

#### Étape 1: Pousser les changements
```bash
# Ajouter les fichiers backend
git add backend/api/models.py
git add backend/api/migrations/0017_emploidutemps_classe_emploidutemps_type_cours.py

# Commit
git commit -m "feat: Ajout champs type_cours et classe au modèle EmploiDuTemps"

# Push
git push origin main
```

#### Étape 2: Sur PythonAnywhere

1. **Ouvrir un Bash Console sur PythonAnywhere**

2. **Naviguer vers le projet**
   ```bash
   cd ~/wendlasida.pythonanywhere.com
   ```

3. **Récupérer les changements**
   ```bash
   git pull origin main
   ```

4. **Activer l'environnement virtuel**
   ```bash
   source .venv/bin/activate
   ```

5. **Appliquer la migration**
   ```bash
   python manage.py migrate
   ```

   Vous devriez voir:
   ```
   Running migrations:
     Applying api.0017_emploidutemps_classe_emploidutemps_type_cours... OK
   ```

6. **Recharger l'application web**
   - Aller sur l'onglet "Web" de PythonAnywhere
   - Cliquer sur le bouton vert "Reload wendlasida.pythonanywhere.com"

## 🧪 Tests à Effectuer

### 1. Test Frontend
1. Ouvrir https://school-wheat-six.vercel.app/frontend/connexion-admin.html
2. Se connecter avec: admin@unierp.bf / Admin2026
3. Naviguer vers "Emploi du temps"
4. Vérifier que:
   - ✅ La grille s'affiche correctement
   - ✅ Les filtres (Filière, Promotion, Classe) sont présents
   - ✅ On peut cliquer sur une cellule pour ajouter un cours
   - ✅ Le modal s'ouvre correctement
   - ✅ Les champs sont pré-remplis (jour, heure)

### 2. Test Backend
1. Créer un cours via l'interface
2. Vérifier qu'il apparaît dans la grille
3. Modifier un cours existant
4. Supprimer un cours
5. Vérifier que les données sont bien sauvegardées

### 3. Test Responsive
1. Ouvrir sur mobile/tablet
2. Vérifier que la grille s'adapte
3. Vérifier que le modal est utilisable

## 🐛 Dépannage

### Problème: La grille ne s'affiche pas
**Solution**: Vérifier la console du navigateur (F12)
- Erreur de chargement CSS/JS?
- Erreur API?

### Problème: Erreur 400 lors de la création d'un cours
**Causes possibles**:
1. Migration non appliquée sur PythonAnywhere
2. Champ manquant dans le formulaire
3. Problème de validation

**Solution**: Vérifier les logs backend et la console navigateur

### Problème: Les cours ne s'affichent pas
**Solution**: 
1. Vérifier que la classe est sélectionnée dans les filtres
2. Vérifier l'appel API dans la console réseau (F12 → Network)
3. Vérifier que des cours existent pour cette classe

## 📊 Données de Test

Pour tester rapidement, créer quelques cours:

### Exemple 1: Cours de Mathématiques
- Jour: Lundi
- Heure: 08:00 - 10:00
- Matière: Mathématiques
- Classe: L1-A
- Salle: Amphi A
- Type: CM

### Exemple 2: TD Informatique
- Jour: Mardi
- Heure: 14:00 - 16:00
- Matière: Algorithmique
- Classe: L1-A
- Salle: Salle 101
- Type: TD

### Exemple 3: TP Physique
- Jour: Mercredi
- Heure: 10:00 - 12:00
- Matière: Physique
- Classe: L1-A
- Salle: Labo 1
- Type: TP

## 🎯 Fonctionnalités Disponibles

### Actuellement Opérationnelles
- ✅ Grille visuelle hebdomadaire
- ✅ Ajout de cours par clic sur cellule
- ✅ Modification de cours existants
- ✅ Suppression de cours
- ✅ Filtrage par classe
- ✅ Types de cours différenciés (CM/TD/TP)
- ✅ Design responsive

### À Implémenter (Optionnel)
- ⏳ Vérification des conflits (prof/salle)
- ⏳ Envoi automatique d'emails
- ⏳ Export PDF
- ⏳ Glisser-déposer
- ⏳ Copie d'emploi du temps

## 📞 Support

En cas de problème:
1. Vérifier les logs dans la console navigateur (F12)
2. Vérifier les logs backend sur PythonAnywhere
3. Consulter `INTEGRATION_EMPLOI_DU_TEMPS_VISUEL.md` pour les détails techniques

## ✅ Validation Finale

Après déploiement, vérifier:
- [ ] Frontend déployé sur Vercel
- [ ] Backend mis à jour sur PythonAnywhere
- [ ] Migration appliquée
- [ ] Grille s'affiche correctement
- [ ] Création de cours fonctionne
- [ ] Modification de cours fonctionne
- [ ] Suppression de cours fonctionne
- [ ] Responsive fonctionne

---

**Date**: 7 mars 2026
**Version**: 1.0
**Statut**: Prêt pour déploiement
