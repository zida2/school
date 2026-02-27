# 🔧 Solution Immédiate

## Le Problème
Le fichier sur PythonAnywhere n'est pas à jour. Il utilise encore `annee` au lieu de `libelle`.

## ✅ Solution en 2 Commandes

Copiez-collez ces 2 lignes dans la console PythonAnywhere:

```bash
cd ~/school && git pull && cd backend
python creer_donnees_test_completes.py
```

## 📊 Résultat Attendu

Vous devriez voir:
```
🔄 CRÉATION DES DONNÉES DE TEST COMPLÈTES
============================================================

📅 1. Création de l'année académique...
   ✅ Année académique créée: 2025-2026

📅 2. Création de l'emploi du temps...
   ✅ Cours créé: Lundi 08:00-10:00
   ✅ Cours créé: Mercredi 14:00-16:00
   ✅ Cours créé: Vendredi 10:00-12:00
```

## ❌ Si Toujours une Erreur

Si après `git pull` vous avez encore l'erreur, exécutez:

```bash
python reorganiser_structure_complete.py
python creer_donnees_test_completes.py
```

Cela va recréer toute la structure (Université, Filière, Classe, Prof, Étudiant) puis créer les données de test.

## 🔄 Après Succès

1. Allez dans l'onglet **Web** de PythonAnywhere
2. Cliquez sur **"Reload Wendlasida.pythonanywhere.com"**
3. Testez sur https://school-wheat-six.vercel.app (Ctrl+Shift+R pour vider le cache)
4. Connectez-vous avec **m.diallo@etu.bf** / **etudiant123**
