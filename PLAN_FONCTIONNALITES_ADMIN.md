# 📋 Plan: Fonctionnalités Admin Complètes

## 🎯 Objectifs

### 1. Gestion des Emplois du Temps
- Créer des emplois du temps pour chaque classe/filière
- Assigner automatiquement aux enseignants
- Envoyer des notifications aux profs
- Interface drag & drop pour faciliter la création

### 2. Gestion Financière Rigoureuse
- Tableau de bord financier complet
- Suivi des paiements par étudiant
- Alertes automatiques pour impayés
- Notifications discrètes aux étudiants
- Lettres de rappel automatiques
- Statistiques financières

### 3. Anonymat et Discrétion
- L'étudiant voit son solde dans son espace privé
- Pas d'affichage public des impayés
- Notifications privées uniquement
- Système de rappels progressifs

## 📊 Fonctionnalités Détaillées

### A. Gestion des Emplois du Temps

#### Interface Admin
```
┌─────────────────────────────────────────────────────────┐
│ 📅 Gestion des Emplois du Temps                         │
├─────────────────────────────────────────────────────────┤
│ Filière: [Licence 1 Informatique ▼]                    │
│ Année: [2024-2025 ▼]                                    │
│ Semestre: [Semestre 1 ▼]                                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│        Lundi    Mardi   Mercredi  Jeudi    Vendredi     │
│ 08:00  ┌─────┐ ┌─────┐ ┌─────┐  ┌─────┐  ┌─────┐      │
│        │Algo │ │Math │ │     │  │BDD  │  │     │      │
│ 10:00  │Prof │ │Prof │ │     │  │Prof │  │     │      │
│        │Salle│ │Salle│ │     │  │Salle│  │     │      │
│        └─────┘ └─────┘ └─────┘  └─────┘  └─────┘      │
│ 10:00  ┌─────┐ ┌─────┐ ┌─────┐  ┌─────┐  ┌─────┐      │
│        │     │ │     │ │Prog │  │     │  │Sys  │      │
│ 12:00  │     │ │     │ │Prof │  │     │  │Prof │      │
│        │     │ │     │ │Salle│  │     │  │Salle│      │
│        └─────┘ └─────┘ └─────┘  └─────┘  └─────┘      │
│                                                          │
│ [+ Ajouter un cours] [📤 Publier l'emploi du temps]    │
└─────────────────────────────────────────────────────────┘
```

#### Fonctionnalités
1. **Créer un cours**:
   - Sélectionner matière (auto-remplit l'enseignant)
   - Choisir jour, heure début, heure fin
   - Choisir salle
   - Choisir semaine (toutes/paire/impaire)

2. **Publier l'emploi du temps**:
   - Valider qu'il n'y a pas de conflits
   - Envoyer notification à tous les profs concernés
   - Envoyer notification à tous les étudiants de la filière

3. **Vérifications automatiques**:
   - Pas de chevauchement de salles
   - Pas de chevauchement pour un prof
   - Pas de chevauchement pour une classe

### B. Gestion Financière

#### Dashboard Financier Admin
```
┌─────────────────────────────────────────────────────────┐
│ 💰 Tableau de Bord Financier                            │
├─────────────────────────────────────────────────────────┤
│ Total Encaissé: 15,450,000 FCFA ✅                      │
│ Total Impayés:   3,250,000 FCFA ⚠️                      │
│ Taux de Recouvrement: 82.6%                             │
├─────────────────────────────────────────────────────────┤
│ 📊 Statistiques par Filière                             │
│ ┌─────────────────┬──────────┬──────────┬────────┐     │
│ │ Filière         │ Encaissé │ Impayés  │ Taux   │     │
│ ├─────────────────┼──────────┼──────────┼────────┤     │
│ │ L1 Informatique │ 5.2M     │ 800K     │ 86.7%  │     │
│ │ L2 Gestion      │ 4.8M     │ 1.2M     │ 80.0%  │     │
│ │ L3 Marketing    │ 5.4M     │ 1.25M    │ 81.2%  │     │
│ └─────────────────┴──────────┴──────────┴────────┘     │
├─────────────────────────────────────────────────────────┤
│ ⚠️ Étudiants en Situation d'Impayé (23)                │
│ [Voir la liste] [Envoyer rappels] [Générer rapport]    │
└─────────────────────────────────────────────────────────┘
```

#### Liste des Impayés
```
┌─────────────────────────────────────────────────────────┐
│ 📋 Étudiants en Situation d'Impayé                      │
├─────────────────────────────────────────────────────────┤
│ Filtres: [Filière ▼] [Niveau ▼] [Montant dû ▼]         │
├─────────────────────────────────────────────────────────┤
│ # │ Matricule    │ Nom           │ Dû      │ Actions   │
│ 1 │ ETU-2024-045 │ Traoré Ali    │ 250K    │ [📧][📄]  │
│ 2 │ ETU-2024-089 │ Kaboré Marie  │ 180K    │ [📧][📄]  │
│ 3 │ ETU-2024-123 │ Sawadogo Jean │ 320K    │ [📧][📄]  │
└─────────────────────────────────────────────────────────┘

Actions:
📧 = Envoyer notification
📄 = Générer lettre de rappel
```

#### Système de Rappels Progressifs
1. **Rappel 1** (J+7 après échéance):
   - Notification dans l'espace étudiant
   - Email de rappel amical
   - Ton: "Rappel amical de votre échéance de paiement"

2. **Rappel 2** (J+15):
   - Notification + Email
   - Ton: "Deuxième rappel - Veuillez régulariser votre situation"

3. **Rappel 3** (J+30):
   - Notification + Email + Lettre officielle
   - Ton: "Dernier rappel avant mesures administratives"

4. **Mesures** (J+45):
   - Blocage de l'accès aux notes
   - Blocage de l'accès aux supports de cours
   - Convocation administrative

### C. Espace Étudiant - Finances

#### Carte "Ma Situation Financière"
```
┌─────────────────────────────────────────────────────────┐
│ 💳 Ma Situation Financière                              │
├─────────────────────────────────────────────────────────┤
│ Frais d'inscription: 500,000 FCFA                       │
│ Montant payé:        320,000 FCFA ✅                    │
│ Reste à payer:       180,000 FCFA ⚠️                    │
│                                                          │
│ Échéance: 15 Février 2025 (dans 12 jours)              │
│                                                          │
│ [📄 Voir mes paiements] [💰 Effectuer un paiement]     │
└─────────────────────────────────────────────────────────┘
```

#### Historique des Paiements
```
┌─────────────────────────────────────────────────────────┐
│ 📋 Historique de mes Paiements                          │
├─────────────────────────────────────────────────────────┤
│ Date       │ Montant   │ Mode      │ Reçu              │
│ 15/01/2025 │ 150,000   │ Orange M. │ [📄 Télécharger]  │
│ 10/12/2024 │ 100,000   │ Espèces   │ [📄 Télécharger]  │
│ 05/11/2024 │  70,000   │ Moov M.   │ [📄 Télécharger]  │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Implémentation Technique

### Phase 1: Corriger l'Erreur Admin ✅
```javascript
// Déplacer les déclarations de fonctions avant leur utilisation
// Ou utiliser async/await correctement
```

### Phase 2: Emplois du Temps
1. **Backend**:
   - Endpoint pour créer/modifier emploi du temps
   - Validation des conflits
   - Notification automatique aux profs

2. **Frontend**:
   - Interface de création (formulaire ou drag & drop)
   - Calendrier visuel
   - Bouton "Publier"

### Phase 3: Gestion Financière
1. **Backend**:
   - Endpoint statistiques financières
   - Endpoint liste des impayés
   - Système de rappels automatiques (Celery tasks)
   - Génération de lettres PDF

2. **Frontend**:
   - Dashboard financier
   - Liste des impayés avec filtres
   - Boutons d'action (notification, lettre)

### Phase 4: Espace Étudiant - Finances
1. **Backend**:
   - Endpoint situation financière étudiant
   - Endpoint historique paiements
   - Génération de reçus PDF

2. **Frontend**:
   - Carte "Ma Situation Financière"
   - Historique des paiements
   - Téléchargement de reçus

## 📊 Modèles de Données

### Notification de Rappel
```python
class RappelPaiement(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    type_rappel = models.CharField(max_length=20, choices=[
        ('rappel_1', 'Premier rappel'),
        ('rappel_2', 'Deuxième rappel'),
        ('rappel_3', 'Dernier rappel'),
        ('mesure', 'Mesure administrative')
    ])
    montant_du = models.DecimalField(max_digits=12, decimal_places=0)
    date_envoi = models.DateTimeField(auto_now_add=True)
    envoye_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    lu = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)
```

### Lettre de Rappel
```python
class LettreRappel(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    type_lettre = models.CharField(max_length=20)
    contenu = models.TextField()
    fichier_pdf = models.FileField(upload_to='lettres_rappel/')
    date_generation = models.DateTimeField(auto_now_add=True)
    generee_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
```

## 🎨 Design

### Principes
1. **Discrétion**: Pas d'affichage public des impayés
2. **Clarté**: Informations financières claires et précises
3. **Accessibilité**: Facile de voir ce qui reste à payer
4. **Professionnalisme**: Ton respectueux dans les rappels

### Couleurs
- ✅ Vert: Paiement à jour
- ⚠️ Orange: Échéance proche
- ❌ Rouge: Impayé (mais discret)

## ✅ Checklist

### Priorité 1 (Urgent)
- [ ] Corriger erreur `chargerDemandes`
- [ ] Créer interface emploi du temps admin
- [ ] Créer dashboard financier admin
- [ ] Ajouter carte finances dans dashboard étudiant

### Priorité 2 (Important)
- [ ] Système de notifications automatiques
- [ ] Génération de lettres de rappel
- [ ] Validation des conflits emploi du temps
- [ ] Historique des paiements étudiant

### Priorité 3 (Nice to have)
- [ ] Drag & drop pour emploi du temps
- [ ] Graphiques financiers avancés
- [ ] Export Excel des impayés
- [ ] Paiement en ligne intégré

---

**Commençons par corriger l'erreur puis créer ces fonctionnalités!**
