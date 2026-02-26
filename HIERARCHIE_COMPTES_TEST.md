# 🔐 HIÉRARCHIE DES COMPTES DE TEST
## Organisation en cascade pour tests rapides

Date: 26 février 2026

---

## 🎯 OBJECTIF

Organiser les comptes de test en hiérarchie pour faciliter la vérification rapide des fonctionnalités selon les rôles.

---

## 📊 HIÉRARCHIE

```
👔 ADMIN (Niveau 4)
    ↓ Peut tester tous les comptes
    ├─ 👨‍🏫 ENSEIGNANT (Niveau 3)
    │   ↓ Attribué à l'admin
    │   ├─ 🏛️ BUREAU (Niveau 2)
    │   │   ↓ Attribué à l'enseignant
    │   │   └─ 👨‍🎓 ÉTUDIANT (Niveau 1)
    │   │       ↓ Attribué au bureau
    │   │       └─ Compte de base
```

---

## 🔑 COMPTES DE TEST

### Niveau 1: Étudiant 👨‍🎓
```
Email: m.diallo@etu.bf
Password: etudiant123
Nom: Moussa Diallo
Niveau: L1 Informatique
Couleur: Orange (#f59e0b)
```

**Attribué à**: Bureau Exécutif

**Fonctionnalités à tester**:
- ✅ Consultation des notes
- ✅ Création de demandes administratives
- ✅ Création de réclamations sur les notes
- ✅ Affichage des réponses (demandes + réclamations)
- ✅ Liste des enseignants
- ✅ Emploi du temps
- ✅ Supports de cours
- ✅ Paiements

---

### Niveau 2: Bureau Exécutif 🏛️
```
Email: bureau@uan.bf
Password: bureau123
Nom: Bureau Exécutif
Rôle: Gestion des publications et sondages
Couleur: Violet (#8b5cf6)
```

**Attribué à**: Enseignant

**Fonctionnalités à tester**:
- ✅ Création de publications
- ✅ Création de sondages
- ✅ Gestion des objets perdus
- ✅ Consultation des étudiants (compte attribué: Moussa Diallo)

---

### Niveau 3: Enseignant 👨‍🏫
```
Email: j.ouedraogo@uan.bf
Password: enseignant123
Nom: Jean Ouedraogo
Matières: Informatique
Couleur: Vert (#10b981)
```

**Attribué à**: Administrateur

**Fonctionnalités à tester**:
- ✅ Saisie des notes
- ✅ Gestion des réclamations
- ✅ Traitement et correction des notes
- ✅ Réponse aux demandes étudiants
- ✅ Upload de supports de cours
- ✅ Gestion des présences
- ✅ Consultation du bureau (compte attribué: Bureau)

---

### Niveau 4: Administrateur 👔
```
Email: admin@uan.bf
Password: admin123
Nom: Administrateur
Rôle: Gestion complète du système
Couleur: Bleu (#6366f1)
```

**Attribué à**: Personne (niveau le plus élevé)

**Fonctionnalités à tester**:
- ✅ Gestion des étudiants (CRUD)
- ✅ Gestion des enseignants (CRUD)
- ✅ Gestion des filières
- ✅ Réponse aux demandes administratives
- ✅ Consultation des réclamations
- ✅ Gestion des paiements
- ✅ Emploi du temps
- ✅ Consultation de l'enseignant (compte attribué: Jean Ouedraogo)

---

## 🔄 FLUX DE TEST RECOMMANDÉ

### Test Complet (30 minutes)

#### 1. Commencer par l'Étudiant (5 min)
```
1. Se connecter: m.diallo@etu.bf / etudiant123
2. Tester:
   - Consultation des notes
   - Création d'une demande
   - Création d'une réclamation
   - Liste des enseignants
3. Noter les IDs des demandes/réclamations créées
```

#### 2. Passer au Bureau (5 min)
```
1. Se connecter: bureau@uan.bf / bureau123
2. Tester:
   - Création d'une publication
   - Création d'un sondage
   - Vérifier que l'étudiant Moussa Diallo est visible
3. Vérifier les fonctionnalités bureau
```

#### 3. Passer à l'Enseignant (10 min)
```
1. Se connecter: j.ouedraogo@uan.bf / enseignant123
2. Tester:
   - Voir les réclamations de Moussa Diallo
   - Traiter une réclamation
   - Corriger une note
   - Répondre à une demande
   - Vérifier que le bureau est visible
3. Noter les modifications effectuées
```

#### 4. Finir par l'Admin (10 min)
```
1. Se connecter: admin@uan.bf / admin123
2. Tester:
   - Voir les demandes de Moussa Diallo
   - Répondre à une demande
   - Consulter les réclamations
   - Vérifier que l'enseignant Jean Ouedraogo est visible
3. Vérifier la cohérence globale
```

#### 5. Retour à l'Étudiant (5 min)
```
1. Se reconnecter: m.diallo@etu.bf / etudiant123
2. Vérifier:
   - Réponses aux demandes (admin + enseignant)
   - Réponses aux réclamations (enseignant)
   - Notes corrigées
   - Nouvelles moyennes
```

---

## 📋 SCÉNARIOS DE TEST

### Scénario 1: Flux Réclamation Complet

```
ÉTUDIANT (m.diallo@etu.bf)
    ↓ Crée réclamation sur une note
    
ENSEIGNANT (j.ouedraogo@uan.bf)
    ↓ Voit la réclamation (badge notification)
    ↓ Traite et corrige la note
    ↓ Envoie une réponse
    
ÉTUDIANT (m.diallo@etu.bf)
    ↓ Voit la réponse
    ↓ Voit la note corrigée
    ↓ Voit la nouvelle moyenne
```

**Temps estimé**: 5 minutes

---

### Scénario 2: Flux Demande à l'Admin

```
ÉTUDIANT (m.diallo@etu.bf)
    ↓ Crée demande administrative
    ↓ Destinataire: Administration
    
ADMIN (admin@uan.bf)
    ↓ Voit la demande (badge notification)
    ↓ Répond à la demande
    
ÉTUDIANT (m.diallo@etu.bf)
    ↓ Voit la réponse de l'admin
```

**Temps estimé**: 3 minutes

---

### Scénario 3: Flux Demande à un Enseignant

```
ÉTUDIANT (m.diallo@etu.bf)
    ↓ Va dans "Mes enseignants"
    ↓ Clique "Contacter" sur Jean Ouedraogo
    ↓ Crée demande (pré-remplie)
    
ENSEIGNANT (j.ouedraogo@uan.bf)
    ↓ Voit la demande
    ↓ Répond à la demande
    
ÉTUDIANT (m.diallo@etu.bf)
    ↓ Voit la réponse de Jean Ouedraogo
```

**Temps estimé**: 4 minutes

---

## 🎨 INTERFACE DE CONNEXION

### Ordre d'Affichage (Haut → Bas)

```
┌─────────────────────────────────────┐
│  👨‍🎓 Étudiant                        │
│  m.diallo@etu.bf                    │
├─────────────────────────────────────┤
│  🏛️ Bureau Exécutif                 │
│  bureau@uan.bf                      │
├─────────────────────────────────────┤
│  👨‍🏫 Enseignant                      │
│  j.ouedraogo@uan.bf                 │
├─────────────────────────────────────┤
│  👔 Administrateur                   │
│  admin@uan.bf                       │
└─────────────────────────────────────┘

HIÉRARCHIE DES COMPTES
👨‍🎓 Étudiant → attribué au 🏛️ Bureau
🏛️ Bureau → attribué au 👨‍🏫 Enseignant
👨‍🏫 Enseignant → attribué au 👔 Admin
👔 Admin → accès à tous les comptes
```

---

## ✅ AVANTAGES DE CETTE ORGANISATION

### Pour les Tests
- ✅ Ordre logique de bas en haut
- ✅ Chaque niveau teste le niveau inférieur
- ✅ Flux naturel de vérification
- ✅ Hiérarchie claire et visible

### Pour la Compréhension
- ✅ Rôles clairement identifiés avec icônes
- ✅ Légende explicative
- ✅ Couleurs distinctes
- ✅ Organisation intuitive

### Pour la Rapidité
- ✅ Un clic pour se connecter
- ✅ Pas besoin de mémoriser les mots de passe
- ✅ Ordre de test suggéré
- ✅ Vérification rapide des fonctionnalités

---

## 📝 CHECKLIST DE VÉRIFICATION

### Étudiant ✅
- [ ] Peut voir ses notes
- [ ] Peut créer une demande
- [ ] Peut créer une réclamation
- [ ] Peut voir ses enseignants
- [ ] Peut contacter un enseignant
- [ ] Peut voir les réponses aux demandes
- [ ] Peut voir les réponses aux réclamations
- [ ] Peut voir les notes corrigées

### Bureau ✅
- [ ] Peut créer une publication
- [ ] Peut créer un sondage
- [ ] Peut gérer les objets perdus
- [ ] Peut voir l'étudiant attribué

### Enseignant ✅
- [ ] Peut saisir des notes
- [ ] Peut voir les réclamations
- [ ] Peut traiter les réclamations
- [ ] Peut corriger les notes
- [ ] Peut répondre aux demandes
- [ ] Peut voir le bureau attribué

### Admin ✅
- [ ] Peut gérer les étudiants
- [ ] Peut gérer les enseignants
- [ ] Peut voir les demandes
- [ ] Peut répondre aux demandes
- [ ] Peut voir les réclamations
- [ ] Peut voir l'enseignant attribué

---

## 🎯 UTILISATION PRATIQUE

### Pour un Test Rapide (5 min)
```
1. Étudiant: Créer demande + réclamation
2. Enseignant: Traiter réclamation
3. Admin: Répondre à demande
4. Étudiant: Vérifier réponses
```

### Pour un Test Complet (30 min)
```
Suivre le "Flux de Test Recommandé" ci-dessus
```

### Pour Tester une Fonctionnalité Spécifique
```
1. Identifier le rôle concerné
2. Se connecter avec le compte approprié
3. Tester la fonctionnalité
4. Vérifier l'impact sur les autres rôles si nécessaire
```

---

## 🎊 RÉSULTAT

### Organisation Claire
- ✅ Hiérarchie visible sur la page de connexion
- ✅ Ordre logique (Étudiant → Bureau → Enseignant → Admin)
- ✅ Icônes pour identification rapide
- ✅ Légende explicative

### Tests Facilités
- ✅ Un clic pour chaque compte
- ✅ Flux de test suggéré
- ✅ Vérification rapide des fonctionnalités
- ✅ Cohérence entre les rôles

### Documentation
- ✅ Tous les comptes documentés
- ✅ Mots de passe accessibles
- ✅ Scénarios de test détaillés
- ✅ Checklist de vérification

---

## 🚀 DÉMARRAGE RAPIDE

1. **Ouvrir**: `http://127.0.0.1:8080/index.html`
2. **Voir**: Section "Accès rapide"
3. **Cliquer**: Sur le compte souhaité
4. **Tester**: Les fonctionnalités du rôle
5. **Vérifier**: L'impact sur les autres rôles

**C'est tout!** 🎉

---

Date: 26 février 2026
Version: 1.0
Statut: ✅ HIÉRARCHIE ORGANISÉE
