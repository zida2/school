# 🎯 Prochaines Étapes - Fonctionnalités Admin

## ✅ Ce qui vient d'être fait

1. **Erreur corrigée**: `chargerDemandes is not defined` ✅
2. **Plan complet créé**: `PLAN_FONCTIONNALITES_ADMIN.md` ✅
3. **Code pushé sur GitHub** ✅

## 📋 Fonctionnalités à Implémenter

### 1. Gestion des Emplois du Temps 📅

**Objectif**: L'admin crée l'emploi du temps et l'envoie automatiquement aux profs et étudiants.

**Interface à créer**:
- Calendrier hebdomadaire visuel
- Formulaire d'ajout de cours (Matière, Jour, Heure, Salle)
- Validation automatique des conflits
- Bouton "Publier" qui envoie des notifications

**Backend nécessaire**:
- Endpoint pour créer/modifier emploi du temps
- Validation des conflits (salle, prof, classe)
- Envoi automatique de notifications

### 2. Gestion Financière Rigoureuse 💰

**Objectif**: Suivi précis des paiements avec notifications discrètes aux étudiants.

**Interfaces à créer**:

#### A. Dashboard Financier Admin
- Total encaissé / Total impayés
- Taux de recouvrement
- Statistiques par filière
- Liste des étudiants en impayé

#### B. Actions Admin
- Bouton "Envoyer rappel" (notification privée)
- Bouton "Générer lettre" (PDF officiel)
- Filtres: Par filière, par montant, par ancienneté

#### C. Espace Étudiant - Finances
- Carte "Ma Situation Financière"
  - Frais d'inscription
  - Montant payé
  - Reste à payer
  - Échéance
- Historique des paiements
- Téléchargement de reçus

**Backend nécessaire**:
- Endpoint statistiques financières
- Endpoint liste des impayés
- Système de rappels automatiques
- Génération de lettres PDF
- Génération de reçus PDF

### 3. Système de Rappels Progressifs 📧

**Rappel 1** (J+7):
- Notification dans l'espace étudiant
- Email amical
- Ton: "Rappel amical de votre échéance"

**Rappel 2** (J+15):
- Notification + Email
- Ton: "Deuxième rappel - Veuillez régulariser"

**Rappel 3** (J+30):
- Notification + Email + Lettre officielle
- Ton: "Dernier rappel avant mesures"

**Mesures** (J+45):
- Blocage accès notes
- Blocage accès supports
- Convocation administrative

## 🔧 Implémentation Technique

### Modèles à Ajouter

```python
# backend/api/models.py

class RappelPaiement(models.Model):
    """Historique des rappels envoyés"""
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

class LettreRappel(models.Model):
    """Lettres officielles générées"""
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    type_lettre = models.CharField(max_length=20)
    contenu = models.TextField()
    fichier_pdf = models.FileField(upload_to='lettres_rappel/')
    date_generation = models.DateTimeField(auto_now_add=True)
    generee_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
```

### Endpoints API à Créer

```python
# backend/api/views.py

# Statistiques financières
@action(detail=False, methods=['get'])
def statistiques_financieres(self, request):
    # Retourner total encaissé, impayés, taux, etc.

# Liste des impayés
@action(detail=False, methods=['get'])
def liste_impayes(self, request):
    # Retourner étudiants avec solde_du > 0

# Envoyer rappel
@action(detail=True, methods=['post'])
def envoyer_rappel(self, request, pk=None):
    # Créer notification + email

# Générer lettre
@action(detail=True, methods=['post'])
def generer_lettre(self, request, pk=None):
    # Générer PDF et l'envoyer
```

## 📊 Priorités

### Priorité 1 (Cette semaine)
1. ✅ Corriger erreur admin
2. Créer dashboard financier admin
3. Ajouter carte finances dans dashboard étudiant
4. Endpoint statistiques financières

### Priorité 2 (Semaine prochaine)
1. Interface emploi du temps admin
2. Système de notifications automatiques
3. Génération de lettres de rappel
4. Historique des paiements étudiant

### Priorité 3 (Plus tard)
1. Drag & drop pour emploi du temps
2. Graphiques financiers avancés
3. Export Excel des impayés
4. Paiement en ligne intégré

## 🎨 Principes de Design

### Anonymat et Discrétion
- ✅ Pas d'affichage public des impayés
- ✅ Notifications privées uniquement
- ✅ Ton respectueux dans les rappels
- ✅ Interface claire mais discrète

### Couleurs
- 🟢 Vert: Paiement à jour
- 🟠 Orange: Échéance proche (7 jours)
- 🔴 Rouge: Impayé (mais discret, pas agressif)

### Messages
- ❌ Mauvais: "VOUS DEVEZ 180,000 FCFA!"
- ✅ Bon: "Reste à payer: 180,000 FCFA - Échéance: 15 Février"

## 🚀 Déploiement

Après chaque fonctionnalité:
```bash
# Sur PythonAnywhere
cd ~/school/backend
git pull origin main
python manage.py makemigrations  # Si nouveaux modèles
python manage.py migrate
# Recharger l'application (onglet Web → Reload)
```

## 📝 Tests à Effectuer

### Test 1: Dashboard Financier Admin
- [ ] Se connecter comme admin
- [ ] Voir les statistiques financières
- [ ] Voir la liste des impayés
- [ ] Envoyer un rappel à un étudiant
- [ ] Générer une lettre de rappel

### Test 2: Espace Étudiant - Finances
- [ ] Se connecter comme étudiant
- [ ] Voir sa situation financière
- [ ] Voir l'historique des paiements
- [ ] Télécharger un reçu
- [ ] Recevoir une notification de rappel

### Test 3: Emploi du Temps
- [ ] Se connecter comme admin
- [ ] Créer un emploi du temps
- [ ] Publier l'emploi du temps
- [ ] Vérifier que les profs reçoivent la notification
- [ ] Vérifier que les étudiants voient l'emploi du temps

## 💡 Idées Supplémentaires

### Gamification des Paiements
- Badge "Paiement à jour" pour les étudiants
- Classement des filières par taux de paiement
- Récompenses pour paiement anticipé

### Facilités de Paiement
- Plan de paiement échelonné
- Paiement en plusieurs fois
- Rappels avant échéance (proactif)

### Statistiques Avancées
- Prévision des encaissements
- Analyse des tendances de paiement
- Comparaison année par année

---

**Prêt à commencer l'implémentation! 🚀**

**Quelle fonctionnalité voulez-vous implémenter en premier?**
1. Dashboard financier admin
2. Carte finances dashboard étudiant
3. Interface emploi du temps
