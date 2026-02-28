# Actions à effectuer sur PythonAnywhere

## Étapes à suivre

### 1. Mettre à jour le code backend

Ouvrez un bash console sur PythonAnywhere et exécutez:

```bash
cd ~/school/backend
git pull
```

Vous devriez voir:
```
Updating 08b5898..95360d4
Fast-forward
 backend/api/views.py                     | XX files changed
 backend/verifier_enseignant_ouedraogo.py | created
 dashboard-prof.html                      | XX insertions(+), XX deletions(-)
```

### 2. Recharger l'application web

1. Allez dans l'onglet **Web** de PythonAnywhere
2. Cliquez sur le bouton vert **"Reload wendlasida.pythonanywhere.com"**
3. Attendez que le message "Reloaded" apparaisse

### 3. Vérifier les logs d'erreur

Si des erreurs persistent après actualisation du frontend:

1. Dans l'onglet **Web**, cliquez sur le lien **"Error log"** en haut
2. Faites défiler jusqu'en bas pour voir les dernières erreurs
3. Cherchez les messages que j'ai ajoutés:
   - `"Utilisateur X n'a pas d'enseignant associé"`
   - `"Erreur filtre enseignant: ..."`

### 4. Tester sur le frontend

1. Actualisez la page frontend avec **Ctrl+Shift+R**
2. Connectez-vous avec j.ouedraogo@uan.bf / enseignant123
3. Allez dans l'onglet **"Saisie des notes"**
4. Vous devriez voir:
   - Les filtres: Filière, Matière, Année académique
   - Pas d'erreur 403 sur /api/filieres/
   - Pas d'erreur 500 sur /api/notes/

## Corrections effectuées

### Backend (backend/api/views.py)

1. ✅ **AnneeAcademiqueViewSet**: Lecture autorisée pour tous les utilisateurs authentifiés
2. ✅ **FiliereViewSet**: Lecture autorisée pour tous les utilisateurs authentifiés
3. ✅ **NoteViewSet**: Meilleure gestion d'erreur avec logs pour debug
4. ✅ Toutes les vérifications de rôle acceptent maintenant 'enseignant' ET 'professeur'

### Frontend (dashboard-prof.html)

1. ✅ Nouvelle interface de saisie des notes avec filtres
2. ✅ Calcul automatique de la moyenne en temps réel
3. ✅ Bouton "Sauvegarder tout" pour enregistrer les notes
4. ✅ Bouton "Publier les notes" pour notifier les étudiants
5. ✅ Suppression de la fonction obsolète chargerMatieresNotes

## Problèmes connus

### Erreur 500 sur /api/notes/?matiere=X

**Cause probable**: L'utilisateur n'a pas d'objet enseignant associé, ou il y a un problème avec les relations dans la base de données.

**Solution**: Vérifier les logs d'erreur sur PythonAnywhere après avoir rechargé l'application. Les messages de debug ajoutés nous diront exactement quel est le problème.

### Erreur 403 sur /api/filieres/

**Cause**: Le code n'a pas été mis à jour sur PythonAnywhere.

**Solution**: Faire `git pull` et recharger l'application.

## Commits récents

- `95360d4` - Fix: Supprimer fonction obsolète chargerMatieresNotes
- `255c904` - Fix: Autoriser enseignants à lire filières + meilleure gestion erreur notes
- `3915f63` - Feature: Nouvelle interface saisie notes avec filtres filière/matière/année et publication
- `ccc1898` - Fix: Autoriser enseignants à lire les années académiques
- `bc0a4b0` - Fix: Gestion erreur robuste pour chargement notes par matière
- `08b5898` - Fix: Accepter role enseignant en plus de professeur dans toutes les vues backend

## Contact

Si les erreurs persistent après avoir suivi toutes ces étapes, partagez-moi:
1. Le contenu du Error log de PythonAnywhere
2. Les erreurs dans la console du navigateur
3. Une capture d'écran de la page
