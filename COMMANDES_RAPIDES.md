# ⚡ Commandes Rapides - PythonAnywhere

## 🚀 Créer les Données de Test (3 commandes)

Copiez-collez ces 3 blocs dans la console Bash de PythonAnywhere:

### 1️⃣ Mettre à jour le code
```bash
cd ~/school && git pull && cd backend
```

### 2️⃣ Créer les données
```bash
python creer_donnees_test_completes.py
```

### 3️⃣ Recharger l'app
Allez dans l'onglet **Web** → Cliquez sur **"Reload"** (bouton vert)

---

## ✅ C'est Tout!

Ensuite:
1. Allez sur https://school-wheat-six.vercel.app
2. Appuyez sur **Ctrl + Shift + R** pour vider le cache
3. Connectez-vous avec **m.diallo@etu.bf** / **etudiant123**

Le dashboard devrait maintenant afficher:
- ✅ Emploi du temps (3 cours/semaine)
- ✅ Notes (15.5 et 17.0)
- ✅ Supports de cours (3 documents)

---

## ❌ Si Erreur

Si vous voyez une erreur, exécutez d'abord:
```bash
python reorganiser_structure_complete.py
```

Puis recommencez l'étape 2.

---

## 📋 Vérification Rapide

Pour vérifier que les données sont créées:
```bash
python manage.py shell -c "from api.models import EmploiDuTemps, NoteEvaluation, SupportCours; print(f'Emplois: {EmploiDuTemps.objects.count()}, Notes: {NoteEvaluation.objects.count()}, Supports: {SupportCours.objects.count()}')"
```

Résultat attendu: `Emplois: 3, Notes: 2, Supports: 3`
