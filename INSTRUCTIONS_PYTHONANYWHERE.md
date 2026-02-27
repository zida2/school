# 📋 Instructions PythonAnywhere - Création des Données de Test

## 🎯 Objectif
Créer les données de test (emploi du temps, notes, supports) pour que le dashboard affiche des informations.

---

## 📝 Commandes à Exécuter (Copier-Coller)

### Étape 1: Mettre à jour le code
```bash
cd ~/school
git pull
cd backend
```

### Étape 2: Vérifier les prérequis (optionnel mais recommandé)
```bash
python verifier_avant_creation_donnees.py
```

Si vous voyez des erreurs ❌, exécutez d'abord:
```bash
python reorganiser_structure_complete.py
```

### Étape 3: Créer les données de test
```bash
python creer_donnees_test_completes.py
```

---

## ✅ Résultat Attendu

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

---

## 🔄 Étape 4: Recharger l'Application

1. Allez dans l'onglet **Web** de PythonAnywhere
2. Cliquez sur le bouton vert **"Reload Wendlasida.pythonanywhere.com"**

---

## 🌐 Étape 5: Tester sur Vercel

1. Allez sur: https://school-wheat-six.vercel.app
2. Videz le cache: **Ctrl + Shift + R** (ou **Cmd + Shift + R** sur Mac)
3. Connectez-vous avec:
   - **Étudiant**: m.diallo@etu.bf / etudiant123
   - **Prof**: j.ouedraogo@uan.bf / enseignant123

---

## 📊 Ce Qui Sera Affiché

### Dashboard Étudiant (Moussa Diallo)
- ✅ Emploi du temps de la semaine (3 cours)
- ✅ Notes: CC1 (15.5/20), CC2 (17.0/20)
- ✅ Moyenne: 16.25/20
- ✅ 3 supports de cours disponibles
- ✅ Prochaine évaluation: Examen Final (dans 30 jours)

### Dashboard Prof (Prof Ouedraogo)
- ✅ Emploi du temps de la semaine
- ✅ Liste des étudiants (Moussa Diallo)
- ✅ Évaluations créées (2 CC + 1 Examen)
- ✅ Supports de cours publiés

---

## ❌ En Cas d'Erreur

### Erreur: "Cannot resolve keyword 'classe'"
**Cause**: Ancienne version du script
**Solution**:
```bash
cd ~/school
git pull
cd backend
python creer_donnees_test_completes.py
```

### Erreur: "DoesNotExist: Enseignant matching query does not exist"
**Cause**: Les données de base (prof, étudiant, classe) n'existent pas
**Solution**:
```bash
python reorganiser_structure_complete.py
python creer_donnees_test_completes.py
```

### Erreur: "IntegrityError: NOT NULL constraint failed"
**Cause**: Données incomplètes
**Solution**:
```bash
python reorganiser_structure_complete.py
python creer_donnees_test_completes.py
```

---

## 🔍 Vérification Rapide

Pour vérifier que tout fonctionne:

```bash
# Vérifier les emplois du temps
python manage.py shell -c "from api.models import EmploiDuTemps; print(f'Emplois du temps: {EmploiDuTemps.objects.count()}')"

# Vérifier les notes
python manage.py shell -c "from api.models import NoteEvaluation; print(f'Notes: {NoteEvaluation.objects.count()}')"

# Vérifier les supports
python manage.py shell -c "from api.models import SupportCours; print(f'Supports: {SupportCours.objects.count()}')"
```

---

## 📞 Support

Si vous rencontrez un problème:
1. Copiez le message d'erreur complet
2. Partagez-le pour diagnostic
3. Indiquez à quelle étape l'erreur s'est produite

---

## ✨ Prochaines Étapes

Une fois les données créées et le dashboard fonctionnel:
- Tester la création de nouvelles demandes
- Tester l'ajout de notes par le prof
- Tester l'upload de supports de cours
- Vérifier les notifications
