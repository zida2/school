# 🔧 Fix Git sur PythonAnywhere

## Le Problème
Git refuse de faire le merge car vous avez des modifications locales sur `db.sqlite3` et `requirements.txt`.

## ✅ Solution (Copier-Coller)

```bash
cd ~/school
git stash
git pull
cd backend
python creer_donnees_test_completes.py
```

## 📝 Explication

1. `git stash` - Met de côté vos modifications locales temporairement
2. `git pull` - Récupère les dernières mises à jour de GitHub
3. `cd backend` - Va dans le dossier backend
4. `python creer_donnees_test_completes.py` - Exécute le script corrigé

## ✅ Résultat Attendu

Après `git pull`, vous devriez voir:
```
Updating dd98785..1718332
Fast-forward
 COMMANDES_RAPIDES.md                       |  54 +++++
 GUIDE_CREATION_DONNEES_TEST.md             |  74 ++++++
 INSTRUCTIONS_PYTHONANYWHERE.md             | 168 +++++++++++++
 SOLUTION_IMMEDIATE.md                      |  35 +++
 backend/creer_donnees_test_completes.py    |  89 ++++---
 backend/verifier_avant_creation_donnees.py | 117 +++++++++
 ...
```

Puis après `python creer_donnees_test_completes.py`:
```
🔄 CRÉATION DES DONNÉES DE TEST COMPLÈTES
============================================================

📅 1. Création de l'année académique...
   ✅ Année académique créée: 2025-2026

📅 2. Création de l'emploi du temps...
   ✅ Cours créé: Lundi 08:00-10:00
   ✅ Cours créé: Mercredi 14:00-16:00
   ✅ Cours créé: Vendredi 10:00-12:00
   📊 Total: 3 cours/semaine

📝 3. Création des évaluations...
   ✅ Évaluation créée: Contrôle Continu 1
   ✅ Évaluation créée: Contrôle Continu 2
   ✅ Évaluation créée: Examen Final

📊 4. Création des notes...
   ✅ Note créée: CC1 = 15.5/20
   ✅ Note créée: CC2 = 17.0/20
   ✅ Note finale créée: Moyenne CC = 16.25/20

📚 5. Création des supports de cours...
   ✅ Support créé: Introduction à l'Informatique - Chapitre 1
   ✅ Support créé: TD 1 - Algorithmique
   ✅ Support créé: TP 1 - Programmation Python

============================================================
✅ DONNÉES DE TEST CRÉÉES AVEC SUCCÈS!
============================================================
```

## 🔄 Ensuite

1. Allez dans l'onglet **Web** de PythonAnywhere
2. Cliquez sur **"Reload Wendlasida.pythonanywhere.com"**
3. Testez sur https://school-wheat-six.vercel.app
4. Videz le cache: **Ctrl + Shift + R**
5. Connectez-vous: **m.diallo@etu.bf** / **etudiant123**

Le dashboard devrait maintenant afficher toutes les données!
