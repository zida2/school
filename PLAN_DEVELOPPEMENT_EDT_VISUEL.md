# 🚀 Plan de Développement - Emploi du Temps Visuel

## 📋 Vue d'Ensemble

Développement complet d'un système d'emploi du temps visuel avec grille horaire interactive.

**Durée estimée**: 11-16 heures
**Complexité**: Élevée
**Impact**: Majeur

## 🎯 Objectifs

1. ✅ Grille horaire visuelle (Lundi-Dimanche, 8h-18h)
2. ✅ Ajout de cours par clic sur les créneaux
3. ✅ Filtres: Filière → Promotion → Classe
4. ✅ Auto-assignation des professeurs
5. ✅ Vérification des conflits
6. ✅ Envoi automatique aux profs et étudiants

## 📦 Étapes de Développement

### ÉTAPE 1: Préparation Backend (1-2h)
**Fichiers à modifier**:
- `backend/api/models.py` - Ajouter champs manquants
- `backend/api/serializers.py` - Mettre à jour serializers
- `backend/api/views.py` - Ajouter endpoints

**Tâches**:
- [ ] Ajouter `type_cours` au modèle EmploiDuTemps
- [ ] Créer endpoint `verifier-conflits/`
- [ ] Créer endpoint `envoyer-emails/`
- [ ] Créer endpoint `par-classe/{id}/`
- [ ] Tester les endpoints

### ÉTAPE 2: Interface Grille HTML/CSS (2-3h)
**Fichiers à créer**:
- `frontend/css/emploi-temps-grid.css` - Styles de la grille
- `frontend/js/emploi-temps-grid.js` - Logique de la grille

**Tâches**:
- [ ] Créer la structure HTML de la grille
- [ ] Styliser la grille (responsive)
- [ ] Ajouter les en-têtes (jours, heures)
- [ ] Créer les cellules cliquables
- [ ] Tester l'affichage

### ÉTAPE 3: Modal Ajout de Cours (1-2h)
**Fichiers à modifier**:
- `frontend/dashboard-admin.html` - Ajouter le modal

**Tâches**:
- [ ] Créer le modal d'ajout
- [ ] Formulaire avec tous les champs
- [ ] Auto-remplissage jour/heure
- [ ] Sélection matière → auto-assignation prof
- [ ] Validation du formulaire

### ÉTAPE 4: Logique d'Affichage des Cours (2-3h)
**Fichiers à modifier**:
- `frontend/js/emploi-temps-grid.js`

**Tâches**:
- [ ] Charger les cours depuis l'API
- [ ] Afficher les cours dans la grille
- [ ] Gérer les cours de plusieurs heures
- [ ] Couleurs par type (CM, TD, TP)
- [ ] Hover et tooltips

### ÉTAPE 5: Gestion des Conflits (1-2h)
**Fichiers à modifier**:
- `frontend/js/emploi-temps-grid.js`
- `backend/api/views.py`

**Tâches**:
- [ ] Vérifier disponibilité professeur
- [ ] Vérifier disponibilité salle
- [ ] Vérifier chevauchement classe
- [ ] Afficher les alertes
- [ ] Bloquer l'ajout si conflit

### ÉTAPE 6: Sauvegarde et Modification (1-2h)
**Fichiers à modifier**:
- `frontend/js/emploi-temps-grid.js`

**Tâches**:
- [ ] Sauvegarder un cours
- [ ] Modifier un cours existant
- [ ] Supprimer un cours
- [ ] Rafraîchir la grille
- [ ] Gestion des erreurs

### ÉTAPE 7: Envoi Automatique Emails (2-3h)
**Fichiers à créer/modifier**:
- `backend/api/views_emploi_temps.py` - Logique d'envoi
- `backend/api/email_service.py` - Templates emails

**Tâches**:
- [ ] Créer template email professeur
- [ ] Créer template email étudiant
- [ ] Fonction d'envoi groupé
- [ ] Bouton "Envoyer" dans l'interface
- [ ] Confirmation d'envoi

### ÉTAPE 8: Tests et Optimisations (1-2h)
**Tâches**:
- [ ] Tester tous les scénarios
- [ ] Vérifier la responsivité
- [ ] Optimiser les performances
- [ ] Corriger les bugs
- [ ] Documentation

## 📁 Structure des Fichiers

```
backend/
├── api/
│   ├── models.py (modifier)
│   ├── serializers.py (modifier)
│   ├── views.py (modifier)
│   ├── views_emploi_temps.py (créer)
│   └── email_service.py (modifier)

frontend/
├── css/
│   └── emploi-temps-grid.css (créer)
├── js/
│   └── emploi-temps-grid.js (créer)
└── dashboard-admin.html (modifier)
```

## 🔄 Workflow de Développement

### Session 1 (3-4h): Backend + Structure
1. Modifier les modèles
2. Créer les endpoints
3. Créer la structure HTML de la grille
4. Styliser la grille

### Session 2 (3-4h): Interface Interactive
1. Modal d'ajout de cours
2. Logique d'affichage
3. Gestion des clics
4. Intégration API

### Session 3 (3-4h): Fonctionnalités Avancées
1. Vérification des conflits
2. Modification/Suppression
3. Envoi des emails
4. Tests finaux

### Session 4 (2-4h): Polish & Déploiement
1. Corrections de bugs
2. Optimisations
3. Documentation
4. Déploiement

## 🎨 Aperçu Visuel

```
┌────────────────────────────────────────────────────────────────┐
│ 📅 Emploi du Temps - Gestion Visuelle                          │
├────────────────────────────────────────────────────────────────┤
│ Filière: [Informatique ▼] Promotion: [2024 ▼] Classe: [L1-A ▼]│
│ [💾 Enregistrer] [📧 Envoyer aux Profs/Étudiants]              │
├────────────────────────────────────────────────────────────────┤
│       │ Lundi  │ Mardi  │ Mercr. │ Jeudi  │ Vendr. │ Sam │ Dim│
├───────┼────────┼────────┼────────┼────────┼────────┼─────┼────┤
│ 08:00 │   +    │   +    │   +    │   +    │   +    │  +  │ +  │
│ 09:00 │ [Algo] │   +    │   +    │   +    │   +    │  +  │ +  │
│ 10:00 │ [Algo] │   +    │   +    │   +    │   +    │  +  │ +  │
│ 11:00 │   +    │   +    │   +    │   +    │   +    │  +  │ +  │
│ ...   │   ...  │   ...  │   ...  │   ...  │   ...  │ ... │... │
└───────┴────────┴────────┴────────┴────────┴────────┴─────┴────┘
```

## 🚦 Critères de Succès

- [ ] Grille affichée correctement sur tous les écrans
- [ ] Ajout de cours fonctionnel
- [ ] Conflits détectés et bloqués
- [ ] Emails envoyés automatiquement
- [ ] Interface intuitive et rapide
- [ ] Pas de bugs majeurs
- [ ] Documentation complète

## 📝 Notes Importantes

1. **Responsive**: La grille doit s'adapter aux petits écrans
2. **Performance**: Optimiser le chargement des cours
3. **UX**: Interface intuitive, feedback visuel
4. **Sécurité**: Vérifier les permissions
5. **Emails**: Templates professionnels

## 🔗 Dépendances

- Backend Django REST Framework ✅
- Frontend JavaScript vanilla ✅
- API d'envoi d'emails ✅
- Base de données SQLite ✅

## 📊 Métriques de Suivi

- Temps passé par étape
- Nombre de bugs trouvés
- Temps de chargement de la grille
- Taux de réussite des envois d'emails

---

**Date de début**: 7 mars 2026
**Développeur**: Kiro AI
**Statut**: Prêt à démarrer
**Priorité**: HAUTE
