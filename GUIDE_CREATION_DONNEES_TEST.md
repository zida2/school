# 🚀 Guide: Création des Données de Test

## Étape 1: Mettre à jour le code sur PythonAnywhere

Connectez-vous à la console Bash de PythonAnywhere et exécutez:

```bash
cd ~/school
git pull
cd backend
```

## Étape 2: Exécuter le script de création de données

```bash
python creer_donnees_test_completes.py
```

## Étape 3: Recharger l'application

1. Allez dans l'onglet **Web** de PythonAnywhere
2. Cliquez sur le bouton vert **"Reload Wendlasida.pythonanywhere.com"**

## Étape 4: Vider le cache du navigateur

Sur Vercel (https://school-wheat-six.vercel.app):
- Appuyez sur **Ctrl + Shift + R** (Windows/Linux)
- Ou **Cmd + Shift + R** (Mac)

## ✅ Résultat Attendu

Le script va créer:
- ✅ Année académique 2025-2026
- ✅ 3 cours par semaine (Lundi, Mercredi, Vendredi)
- ✅ 3 évaluations (2 CC + 1 Examen)
- ✅ Notes pour Moussa Diallo (15.5 et 17.0)
- ✅ 3 supports de cours (Cours, TD, TP)

## 📊 Données Créées

### Emploi du Temps
- **Lundi 08:00-10:00** - Amphi A
- **Mercredi 14:00-16:00** - Salle 12
- **Vendredi 10:00-12:00** - Lab Info 1

### Évaluations
- **CC1**: 15.5/20 (Bon travail)
- **CC2**: 17.0/20 (Très bien)
- **Examen Final**: À venir (dans 30 jours)

### Supports de Cours
- Introduction à l'Informatique - Chapitre 1
- TD 1 - Algorithmique
- TP 1 - Programmation Python

## 🔍 Vérification

Après avoir rechargé, connectez-vous avec:
- **Étudiant**: m.diallo@etu.bf / etudiant123
- **Prof**: j.ouedraogo@uan.bf / enseignant123

Le dashboard devrait maintenant afficher:
- Emploi du temps de la semaine
- Notes et moyennes
- Supports de cours disponibles
- Prochaines évaluations

## ❌ En cas d'erreur

Si vous voyez une erreur, copiez-la et partagez-la pour diagnostic.

Les erreurs courantes:
- **"Cannot resolve keyword"**: Le script n'est pas à jour → Refaire `git pull`
- **"DoesNotExist"**: Les données de base manquent → Exécuter d'abord `reorganiser_structure_complete.py`
