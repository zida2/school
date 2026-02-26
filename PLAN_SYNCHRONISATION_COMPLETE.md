# PLAN DE SYNCHRONISATION COMPLÈTE DU SYSTÈME
## UniERP BF - Architecture de Communication

Date: 26 février 2026

---

## 🎯 OBJECTIF
Créer un système de communication bidirectionnel complet entre tous les acteurs:
- **Admin** ↔️ Étudiants, Enseignants, Bureau Exécutif
- **Enseignants** ↔️ Étudiants, Admin
- **Bureau Exécutif** ↔️ Étudiants, Admin
- **Étudiants** ↔️ Admin, Enseignants, Bureau Exécutif

---

## 📊 ANALYSE DES ESPACES ACTUELS

### 1. ESPACE ÉTUDIANT (dashboard-etudiant.html)
**Pages existantes:**
- ✅ Tableau de bord
- ✅ Mes notes
- ✅ Emploi du temps
- ✅ Absences
- ✅ Cours
- ✅ Supports de cours
- ✅ Évaluations
- ✅ Demandes (ENVOI uniquement)
- ✅ Réclamations (ENVOI uniquement)
- ✅ Publications (RÉCEPTION uniquement)
- ✅ Sondages (RÉCEPTION uniquement)
- ✅ Questionnaires (RÉCEPTION uniquement)
- ✅ Objets perdus
- ✅ Mes paiements

**Boutons manquants:**
- ❌ Voir les réponses aux demandes
- ❌ Voir les réponses aux réclamations
- ❌ Participer aux sondages (bouton existe mais pas codé)
- ❌ Remplir les questionnaires (bouton existe mais pas codé)

---

### 2. ESPACE ADMIN (dashboard-admin.html)
**Pages existantes:**
- ✅ Tableau de bord
- ✅ Étudiants
- ✅ Enseignants
- ✅ Filières
- ✅ Emploi du temps
- ✅ Paiements

**Pages manquantes:**
- ❌ Demandes reçues (des étudiants)
- ❌ Réclamations reçues (des étudiants)
- ❌ Publications (créer et gérer)
- ❌ Sondages (créer et gérer)
- ❌ Objets perdus (gérer)
- ❌ Notifications
- ❌ Messagerie interne

---

### 3. ESPACE ENSEIGNANT (dashboard-prof.html)
**À analyser et compléter**

**Pages attendues:**
- ✅ Tableau de bord
- ✅ Mes cours
- ✅ Saisie des notes
- ✅ Absences
- ❌ Demandes reçues (des étudiants)
- ❌ Réclamations sur notes (des étudiants)
- ❌ Supports de cours (upload)
- ❌ Évaluations (créer)
- ❌ Questionnaires reçus (évaluations par étudiants)
- ❌ Emploi du temps
- ❌ Messagerie

---

### 4. ESPACE BUREAU EXÉCUTIF (dashboard-bureau.html)
**À analyser et compléter**

**Pages attendues:**
- ✅ Tableau de bord
- ❌ Publications (créer et gérer)
- ❌ Sondages (créer et gérer)
- ❌ Objets perdus (gérer)
- ❌ Événements
- ❌ Demandes reçues
- ❌ Messagerie

---

## 🔄 FLUX DE COMMUNICATION À IMPLÉMENTER

### A. DEMANDES ADMINISTRATIVES

**Flux:**
```
Étudiant → [Demande] → Admin/Professeur
Admin/Professeur → [Réponse] → Étudiant
```

**Actions nécessaires:**
1. ✅ Étudiant: Créer demande (FAIT)
2. ❌ Admin: Page "Demandes reçues" avec liste
3. ❌ Admin: Bouton "Répondre" sur chaque demande
4. ❌ Admin: Modal de réponse
5. ❌ Professeur: Page "Demandes reçues"
6. ❌ Professeur: Bouton "Répondre"
7. ❌ Étudiant: Voir les réponses dans la page Demandes
8. ❌ Notification en temps réel

---

### B. RÉCLAMATIONS SUR NOTES

**Flux:**
```
Étudiant → [Réclamation] → Enseignant
Enseignant → [Réponse/Correction] → Étudiant
Enseignant → [Notification] → Admin (si correction)
```

**Actions nécessaires:**
1. ✅ Étudiant: Créer réclamation (FAIT)
2. ❌ Enseignant: Page "Réclamations reçues"
3. ❌ Enseignant: Bouton "Traiter" sur chaque réclamation
4. ❌ Enseignant: Modal de réponse avec option correction
5. ❌ Étudiant: Voir les réponses dans la page Réclamations
6. ❌ Admin: Notification si note corrigée
7. ❌ Mise à jour automatique de la note si acceptée

---

### C. PUBLICATIONS

**Flux:**
```
Bureau Exécutif → [Publication] → Tous les étudiants
Admin → [Publication] → Tous les étudiants
```

**Actions nécessaires:**
1. ✅ Étudiant: Voir publications (FAIT)
2. ❌ Bureau: Page "Mes publications"
3. ❌ Bureau: Bouton "Nouvelle publication"
4. ❌ Bureau: Modal de création avec upload fichier
5. ❌ Bureau: Boutons Modifier/Supprimer
6. ❌ Admin: Page "Publications" (gestion)
7. ❌ Notification push aux étudiants

---

### D. SONDAGES

**Flux:**
```
Bureau Exécutif → [Sondage] → Étudiants
Étudiants → [Réponses] → Bureau Exécutif
Bureau Exécutif → [Résultats] → Visible
```

**Actions nécessaires:**
1. ✅ Étudiant: Voir sondages (FAIT)
2. ❌ Étudiant: Bouton "Participer" fonctionnel
3. ❌ Étudiant: Modal avec questions du sondage
4. ❌ Étudiant: Soumettre réponses
5. ❌ Bureau: Page "Mes sondages"
6. ❌ Bureau: Bouton "Créer sondage"
7. ❌ Bureau: Modal de création avec questions
8. ❌ Bureau: Voir les résultats en temps réel
9. ❌ Bureau: Exporter résultats

---

### E. QUESTIONNAIRES D'ÉVALUATION

**Flux:**
```
Admin/Enseignant → [Questionnaire] → Étudiants
Étudiants → [Évaluation] → Enseignant/Admin
Admin → [Résultats anonymes] → Enseignant
```

**Actions nécessaires:**
1. ✅ Étudiant: Voir questionnaires (FAIT)
2. ❌ Étudiant: Bouton "Remplir" fonctionnel
3. ❌ Étudiant: Modal avec questions d'évaluation
4. ❌ Étudiant: Soumettre évaluation (anonyme)
5. ❌ Admin: Page "Questionnaires"
6. ❌ Admin: Créer questionnaire
7. ❌ Admin: Voir résultats agrégés
8. ❌ Enseignant: Voir ses évaluations (anonymes)

---

### F. OBJETS PERDUS

**Flux:**
```
Étudiant → [Déclaration] → Bureau Exécutif
Bureau Exécutif → [Mise à jour statut] → Étudiant
```

**Actions nécessaires:**
1. ✅ Étudiant: Voir objets perdus (FAIT)
2. ✅ Étudiant: Déclarer objet (FAIT)
3. ❌ Bureau: Page "Objets perdus"
4. ❌ Bureau: Boutons "Marquer comme récupéré"
5. ❌ Bureau: Bouton "Archiver"
6. ❌ Notification au déclarant

---

### G. SUPPORTS DE COURS

**Flux:**
```
Enseignant → [Upload support] → Étudiants de la matière
Étudiants → [Téléchargement] → Statistiques pour enseignant
```

**Actions nécessaires:**
1. ✅ Étudiant: Voir supports (FAIT)
2. ❌ Étudiant: Télécharger support (fonctionnel)
3. ❌ Enseignant: Page "Mes supports"
4. ❌ Enseignant: Bouton "Ajouter support"
5. ❌ Enseignant: Upload fichier avec métadonnées
6. ❌ Enseignant: Voir statistiques de téléchargement
7. ❌ Admin: Voir tous les supports

---

## 🛠️ PLAN D'IMPLÉMENTATION

### PHASE 1: BACKEND - API Endpoints (PRIORITAIRE)
```python
# Demandes
GET /api/demandes-administratives/  # Filtrer par destinataire
POST /api/demandes-administratives/{id}/repondre/
PATCH /api/demandes-administratives/{id}/  # Changer statut

# Réclamations
GET /api/reclamations/  # Filtrer par enseignant
POST /api/reclamations/{id}/traiter/
PATCH /api/reclamations/{id}/corriger-note/

# Publications
POST /api/publications/
PUT /api/publications/{id}/
DELETE /api/publications/{id}/

# Sondages
POST /api/sondages/
POST /api/sondages/{id}/repondre/
GET /api/sondages/{id}/resultats/

# Questionnaires
POST /api/evaluations/
POST /api/evaluations/{id}/repondre/
GET /api/evaluations/{id}/resultats/

# Objets perdus
PATCH /api/objets-perdus/{id}/  # Changer statut

# Supports
POST /api/supports/
GET /api/supports/statistiques/
```

### PHASE 2: FRONTEND - Pages Admin
1. Page "Demandes reçues"
2. Page "Réclamations"
3. Page "Publications"
4. Page "Sondages"
5. Page "Objets perdus"
6. Page "Notifications"

### PHASE 3: FRONTEND - Pages Enseignant
1. Page "Demandes reçues"
2. Page "Réclamations sur notes"
3. Page "Mes supports"
4. Page "Mes évaluations"
5. Page "Questionnaires reçus"

### PHASE 4: FRONTEND - Pages Bureau Exécutif
1. Page "Publications"
2. Page "Sondages"
3. Page "Objets perdus"
4. Page "Événements"

### PHASE 5: FRONTEND - Compléter Étudiant
1. Coder bouton "Participer" sondages
2. Coder bouton "Remplir" questionnaires
3. Afficher réponses aux demandes
4. Afficher réponses aux réclamations
5. Téléchargement supports fonctionnel

### PHASE 6: NOTIFICATIONS & TEMPS RÉEL
1. Système de notifications
2. Badge de compteur
3. WebSocket pour temps réel (optionnel)
4. Emails de notification (optionnel)

---

## 📋 CHECKLIST COMPLÈTE

### BACKEND
- [ ] Endpoints demandes (répondre, changer statut)
- [ ] Endpoints réclamations (traiter, corriger note)
- [ ] Endpoints publications (CRUD)
- [ ] Endpoints sondages (CRUD + réponses + résultats)
- [ ] Endpoints questionnaires (CRUD + réponses + résultats)
- [ ] Endpoints objets perdus (changer statut)
- [ ] Endpoints supports (upload + stats)
- [ ] Permissions par rôle
- [ ] Filtres par destinataire/auteur

### FRONTEND ADMIN
- [ ] Page Demandes reçues
- [ ] Page Réclamations
- [ ] Page Publications (CRUD)
- [ ] Page Sondages (CRUD)
- [ ] Page Objets perdus
- [ ] Page Notifications
- [ ] Badges de compteur

### FRONTEND ENSEIGNANT
- [ ] Page Demandes reçues
- [ ] Page Réclamations notes
- [ ] Page Mes supports (upload)
- [ ] Page Questionnaires reçus
- [ ] Statistiques téléchargements

### FRONTEND BUREAU
- [ ] Page Publications (CRUD)
- [ ] Page Sondages (CRUD + résultats)
- [ ] Page Objets perdus (gestion)
- [ ] Page Événements

### FRONTEND ÉTUDIANT
- [ ] Coder "Participer" sondages
- [ ] Coder "Remplir" questionnaires
- [ ] Afficher réponses demandes
- [ ] Afficher réponses réclamations
- [ ] Téléchargement supports

---

## 🚀 ORDRE D'EXÉCUTION RECOMMANDÉ

1. **Backend: Demandes & Réclamations** (le plus urgent)
2. **Frontend Admin: Demandes & Réclamations**
3. **Frontend Enseignant: Réclamations**
4. **Frontend Étudiant: Voir réponses**
5. **Backend: Publications & Sondages**
6. **Frontend Bureau: Publications & Sondages**
7. **Frontend Étudiant: Participer sondages**
8. **Backend: Questionnaires**
9. **Frontend: Questionnaires complets**
10. **Système de notifications**

---

## ⏱️ ESTIMATION TEMPS

- Backend (Phase 1): 3-4 heures
- Frontend Admin (Phase 2): 2-3 heures
- Frontend Enseignant (Phase 3): 2-3 heures
- Frontend Bureau (Phase 4): 2 heures
- Frontend Étudiant (Phase 5): 1-2 heures
- Notifications (Phase 6): 2 heures

**TOTAL: 12-16 heures de développement**

---

## 📝 NOTES IMPORTANTES

1. **Permissions**: Chaque endpoint doit vérifier le rôle
2. **Filtres**: Les listes doivent être filtrées par destinataire
3. **Statuts**: Utiliser des statuts clairs (en_attente, en_cours, traitee, rejetee)
4. **Notifications**: Badge avec compteur sur chaque section
5. **Temps réel**: Optionnel mais recommandé pour UX
6. **Tests**: Tester chaque flux de bout en bout

---

Date de création: 26 février 2026
