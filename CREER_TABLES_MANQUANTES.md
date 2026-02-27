# 🔧 Créer les Tables Manquantes

## Le Problème
Les tables `api_classe`, `api_inscription`, `api_enseignementmatiere` n'existent pas dans la base de données.

## ✅ Solution (4 Commandes)

Vous êtes dans `/home/Wendlasida/school/backend`, exécutez:

### 1️⃣ Créer les migrations
```bash
python manage.py makemigrations
```

**Résultat attendu:**
```
Migrations for 'api':
  api/migrations/0006_classe_inscription_enseignementmatiere.py
    - Create model Classe
    - Create model Inscription
    - Create model EnseignementMatiere
```

### 2️⃣ Appliquer les migrations
```bash
python manage.py migrate
```

**Résultat attendu:**
```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, sessions
Running migrations:
  Applying api.0006_classe_inscription_enseignementmatiere... OK
```

### 3️⃣ Créer la structure complète
```bash
python reorganiser_structure_complete.py
```

**Résultat attendu:**
```
🔄 RÉORGANISATION DE LA STRUCTURE HIÉRARCHIQUE
============================================================

🏛️ 0. Configuration de l'Université...
   ℹ️  Université existante: Université Aube Nouvelle

📚 1. Configuration de la filière Informatique...
   ✅ Filière créée: Licence 1 Informatique

🏫 2. Configuration de la classe L1 INFO...
   ✅ Classe créée: L1-INFO-A

📖 3. Configuration de la matière Informatique...
   ✅ Matière créée: Introduction à l'Informatique (INFO-101)

👨‍🏫 4. Configuration du Prof Ouedraogo...
   ✅ Prof créé: Jean Ouedraogo (j.ouedraogo@uan.bf)

🔗 5. Assignation Prof → Matière → Classe...
   ✅ Enseignement créé: Prof Ouedraogo enseigne INFO-101 à L1-INFO-A

👨‍🎓 6. Configuration de Moussa Diallo...
   ✅ Étudiant créé: Moussa Diallo (m.diallo@etu.bf)

📝 7. Inscription de Moussa dans la classe...
   ✅ Inscription créée: Moussa Diallo → L1-INFO-A

👥 8. Configuration du Bureau Exécutif...
   ✅ Bureau créé: Bureau Exécutif (bureau@uan.bf)

============================================================
✅ STRUCTURE HIÉRARCHIQUE CRÉÉE AVEC SUCCÈS!
```

### 4️⃣ Créer les données de test
```bash
python creer_donnees_test_completes.py
```

**Résultat attendu:**
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

## 🔄 Étape Finale: Recharger l'Application

1. Allez dans l'onglet **Web** de PythonAnywhere
2. Cliquez sur **"Reload Wendlasida.pythonanywhere.com"**

## 🌐 Tester sur Vercel

1. https://school-wheat-six.vercel.app
2. **Ctrl + Shift + R** pour vider le cache
3. Connectez-vous: **m.diallo@etu.bf** / **etudiant123**

Le dashboard devrait maintenant afficher:
- ✅ Emploi du temps (3 cours)
- ✅ Notes (15.5 et 17.0)
- ✅ Moyenne (16.25/20)
- ✅ Supports de cours (3)

## 🎉 C'est Terminé!
