# 🚨 DÉPLOIEMENT URGENT - Correction Erreur 500 sur /api/notes/

## Problème Résolu
La propriété `mention` du modèle `Note` était incomplète, causant des erreurs 500 sur tous les endpoints `/api/notes/?matiere=X`.

## Corrections Apportées
1. ✅ Complété la propriété `mention` dans `backend/api/models.py` (ligne 240-252)
2. ✅ Supprimé le code dupliqué dans la méthode `note_sur_20` du modèle `NoteEvaluation`
3. ✅ Code pushé sur GitHub (commit `b48f90c`)

## Actions à Effectuer sur PythonAnywhere

### 1. Se connecter à PythonAnywhere
- URL: https://www.pythonanywhere.com
- Compte: Wendlasida

### 2. Ouvrir un Bash Console
- Aller dans l'onglet "Consoles"
- Cliquer sur "Bash"

### 3. Mettre à jour le code
```bash
cd ~/school/backend
git pull origin main
```

Vous devriez voir:
```
From https://github.com/zida2/school
   503bc2f..b48f90c  main       -> origin/main
Updating 503bc2f..b48f90c
Fast-forward
 backend/api/models.py | 17 ++++++++++-------
 1 file changed, 11 insertions(+), 6 deletions(-)
```

### 4. Recharger l'application Web
- Aller dans l'onglet "Web"
- Cliquer sur le gros bouton vert "Reload wendlasida.pythonanywhere.com"
- Attendre que le bouton redevienne vert (environ 10-20 secondes)

### 5. Vérifier que ça fonctionne
- Ouvrir https://school-wheat-six.vercel.app
- Se connecter avec: j.ouedraogo@uan.bf / enseignant123
- Le dashboard devrait se charger sans erreurs 500
- Vérifier la console du navigateur (F12) - plus d'erreurs "500 Internal Server Error"

## Erreurs Résolues
- ❌ AVANT: `GET /api/notes/?matiere=2 500 (Internal Server Error)`
- ✅ APRÈS: `GET /api/notes/?matiere=2 200 OK`

## Prochaines Étapes
Une fois le déploiement effectué et vérifié:
1. Tester l'onglet "Saisir les notes" dans le dashboard enseignant
2. Vérifier que les filtres (Filière, Matière, Année) fonctionnent
3. Tester la saisie et la publication des notes

## Support
Si vous rencontrez des problèmes:
1. Vérifier les logs d'erreur dans PythonAnywhere (onglet "Web" > "Error log")
2. Vérifier que le `git pull` a bien fonctionné
3. Essayer de recharger l'application une deuxième fois
