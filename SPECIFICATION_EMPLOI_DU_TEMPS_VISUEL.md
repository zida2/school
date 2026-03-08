# 📅 Spécification - Emploi du Temps Visuel

## 🎯 Objectif

Créer un système d'emploi du temps visuel avec une grille horaire interactive permettant de:
1. Visualiser la semaine complète (Lundi à Dimanche, 8h à 18h)
2. Ajouter des cours par glisser-déposer ou clic
3. Assigner automatiquement aux professeurs et étudiants
4. Envoyer automatiquement par email

## 📊 Interface Utilisateur

### Vue Principale - Grille Horaire

```
┌─────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┐
│ Heure   │ Lundi  │ Mardi  │ Mercr. │ Jeudi  │ Vendr. │ Samedi │Dimanch.│
├─────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┤
│ 08:00   │   +    │   +    │   +    │   +    │   +    │   +    │   +    │
│ 09:00   │   +    │ [Cours]│   +    │   +    │   +    │   +    │   +    │
│ 10:00   │   +    │   +    │   +    │   +    │   +    │   +    │   +    │
│ 11:00   │   +    │   +    │   +    │   +    │   +    │   +    │   +    │
│ 12:00   │   +    │   +    │   +    │   +    │   +    │   +    │   +    │
│ 13:00   │   +    │   +    │   +    │   +    │   +    │   +    │   +    │
│ 14:00   │   +    │   +    │   +    │   +    │   +    │   +    │   +    │
│ 15:00   │   +    │   +    │   +    │   +    │   +    │   +    │   +    │
│ 16:00   │   +    │   +    │   +    │   +    │   +    │   +    │   +    │
│ 17:00   │   +    │   +    │   +    │   +    │   +    │   +    │   +    │
└─────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘
```

### Filtres en Haut

```
┌─────────────────────────────────────────────────────────────────┐
│ Filière: [Informatique ▼]  Promotion: [2024 ▼]  Classe: [L1-A ▼]│
│                                                                   │
│ [📅 Nouvelle Semaine] [💾 Enregistrer] [📧 Envoyer aux Profs/Étudiants]│
└─────────────────────────────────────────────────────────────────┘
```

### Modal Ajout de Cours

Quand on clique sur un créneau (+):

```
┌─────────────────────────────────────────┐
│ ➕ Ajouter un cours                      │
├─────────────────────────────────────────┤
│                                         │
│ Jour: Lundi                             │
│ Heure début: 09:00                      │
│ Heure fin: [10:00 ▼]                    │
│                                         │
│ Matière: [Algorithmique ▼]              │
│ Professeur: [Auto] (Prof de la matière)│
│ Salle: [Amphi A ▼]                      │
│                                         │
│ Type: [○ Cours  ○ TD  ○ TP]            │
│                                         │
│ [Annuler]  [Ajouter]                    │
└─────────────────────────────────────────┘
```

### Carte de Cours (dans la grille)

```
┌─────────────────────────┐
│ 🔵 Algorithmique        │
│ 👨‍🏫 Prof. Dupont         │
│ 📍 Amphi A              │
│ ⏰ 09:00 - 11:00        │
│ [✏️] [🗑️]               │
└─────────────────────────┘
```

## 🔧 Fonctionnalités

### 1. Création de l'Emploi du Temps

#### Étape 1: Sélection du Contexte
- Admin sélectionne: Filière → Promotion → Classe
- Le système charge l'emploi du temps existant pour cette classe

#### Étape 2: Ajout de Cours
- Clic sur un créneau horaire (+)
- Modal s'ouvre avec:
  - Jour et heure pré-remplis
  - Liste des matières de la filière
  - Professeur auto-assigné (celui qui enseigne la matière)
  - Sélection de la salle
  - Durée (1h, 2h, 3h)
  - Type (Cours magistral, TD, TP)

#### Étape 3: Validation
- Vérification des conflits:
  - ✅ Professeur disponible (pas de cours en même temps)
  - ✅ Salle disponible
  - ✅ Pas de chevauchement pour la classe
- Affichage visuel du cours dans la grille

#### Étape 4: Enregistrement
- Bouton "💾 Enregistrer" sauvegarde tous les cours
- Génération automatique de l'emploi du temps

### 2. Envoi Automatique

#### Aux Professeurs
- Email avec leur emploi du temps personnel
- Liste de tous leurs cours de la semaine
- Salles et classes assignées

#### Aux Étudiants
- Email avec l'emploi du temps de leur classe
- Tous les cours de la semaine
- Professeurs et salles

### 3. Gestion des Conflits

Le système détecte automatiquement:
- ❌ Professeur déjà occupé
- ❌ Salle déjà réservée
- ❌ Chevauchement de cours pour la classe
- ⚠️ Trop de cours dans la journée (>6h)

## 📦 Modèles de Données

### EmploiDuTemps (existant)
```python
class EmploiDuTemps(models.Model):
    matiere = ForeignKey(Matiere)
    classe = ForeignKey(Classe)  # NOUVEAU
    jour = CharField(choices=JOURS)
    heure_debut = TimeField()
    heure_fin = TimeField()
    salle = CharField()
    type_cours = CharField(choices=['CM', 'TD', 'TP'])  # NOUVEAU
    semaine = CharField(choices=['toutes', 'paire', 'impaire'])
```

### Classe (existant)
```python
class Classe(models.Model):
    code = CharField()
    nom = CharField()
    filiere = ForeignKey(Filiere)
    niveau = CharField()  # L1, L2, L3, M1, M2
    promotion = ForeignKey(Promotion)
    effectif = IntegerField()
```

### Promotion (existant)
```python
class Promotion(models.Model):
    code = CharField()
    filiere = ForeignKey(Filiere)
    annee_entree = IntegerField()
    annee_sortie_prevue = IntegerField()
```

## 🎨 Design de la Grille

### HTML Structure
```html
<div class="emploi-grid">
    <div class="emploi-header">
        <div class="time-column">Heure</div>
        <div class="day-column">Lundi</div>
        <div class="day-column">Mardi</div>
        <!-- ... autres jours -->
    </div>
    
    <div class="emploi-body">
        <div class="time-row" data-hour="08">
            <div class="time-cell">08:00</div>
            <div class="course-cell" data-day="Lundi" data-hour="08">
                <!-- Cours ou bouton + -->
            </div>
            <!-- ... autres jours -->
        </div>
        <!-- ... autres heures -->
    </div>
</div>
```

### CSS
```css
.emploi-grid {
    display: grid;
    grid-template-columns: 80px repeat(7, 1fr);
    gap: 1px;
    background: #e5e7eb;
}

.course-cell {
    min-height: 60px;
    background: white;
    padding: 8px;
    cursor: pointer;
    position: relative;
}

.course-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px;
    border-radius: 8px;
    font-size: 12px;
}
```

## 🔄 Workflow Complet

### 1. Admin Crée l'Emploi du Temps
```
1. Sélectionne: Informatique → Promo 2024 → Classe L1-A
2. Clique sur Lundi 09:00
3. Sélectionne: Algorithmique (Prof auto-assigné)
4. Choisit: Amphi A, Durée 2h, Type CM
5. Valide → Cours ajouté dans la grille
6. Répète pour tous les cours de la semaine
7. Clique "💾 Enregistrer"
```

### 2. Système Valide
```
✅ Vérifie les conflits
✅ Sauvegarde dans la base de données
✅ Génère l'emploi du temps
```

### 3. Admin Envoie
```
1. Clique "📧 Envoyer aux Profs/Étudiants"
2. Système envoie automatiquement:
   - Email à chaque prof avec ses cours
   - Email à tous les étudiants de la classe
```

### 4. Réception
```
Professeurs reçoivent:
- Leur emploi du temps personnel
- Liste des classes à enseigner
- Salles assignées

Étudiants reçoivent:
- Emploi du temps de leur classe
- Liste des professeurs
- Salles de cours
```

## 📊 API Endpoints Nécessaires

### Existants (à utiliser)
- `GET /api/emplois-du-temps/` - Liste des cours
- `POST /api/emplois-du-temps/` - Créer un cours
- `PUT /api/emplois-du-temps/{id}/` - Modifier
- `DELETE /api/emplois-du-temps/{id}/` - Supprimer
- `GET /api/classes/` - Liste des classes
- `GET /api/promotions/` - Liste des promotions
- `GET /api/matieres/` - Liste des matières

### Nouveaux (à créer)
- `POST /api/emplois-du-temps/verifier-conflits/` - Vérifier disponibilité
- `POST /api/emplois-du-temps/envoyer-emails/` - Envoyer aux profs/étudiants
- `GET /api/emplois-du-temps/par-classe/{classe_id}/` - EDT d'une classe
- `GET /api/emplois-du-temps/par-professeur/{prof_id}/` - EDT d'un prof

## ⏱️ Estimation de Développement

### Phase 1: Interface Grille (4-6 heures)
- Créer la grille HTML/CSS
- Ajouter l'interactivité (clic sur cellules)
- Modal d'ajout de cours

### Phase 2: Logique Métier (3-4 heures)
- Gestion des cours dans la grille
- Vérification des conflits
- Sauvegarde en base de données

### Phase 3: Envoi Emails (2-3 heures)
- Génération des emails personnalisés
- Envoi automatique aux profs
- Envoi automatique aux étudiants

### Phase 4: Tests & Ajustements (2-3 heures)
- Tests de tous les scénarios
- Corrections de bugs
- Optimisations

**Total estimé: 11-16 heures de développement**

## 🚀 Prochaines Étapes

1. **Valider la spécification** avec toi
2. **Créer un prototype** de la grille visuelle
3. **Implémenter** les fonctionnalités une par une
4. **Tester** avec des données réelles
5. **Déployer** en production

## 💡 Fonctionnalités Bonus (Optionnelles)

- 🎨 Couleurs différentes par type de cours (CM, TD, TP)
- 📱 Version mobile responsive
- 🔄 Glisser-déposer pour déplacer les cours
- 📋 Copier l'emploi du temps d'une semaine à l'autre
- 📊 Statistiques (heures par prof, charge de travail)
- 🔔 Notifications push pour les changements
- 📥 Export PDF de l'emploi du temps
- 🔗 Lien public pour consulter l'EDT

---

**Date**: 7 mars 2026
**Statut**: Spécification complète
**Prêt pour développement**: Oui, après validation
