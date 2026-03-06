# 📋 SYSTÈME D'INSCRIPTION PROFESSEURS

## 🎯 Workflow Complet

### 1. Professeur S'inscrit
- Formulaire public accessible sans compte
- Renseigne ses informations
- Demande créée avec statut "en_attente"

### 2. Admin Voit la Demande
- Liste des demandes dans dashboard admin
- Peut voir toutes les infos du prof
- Peut valider ou rejeter

### 3. Validation Admin
- Admin valide la demande
- Système crée automatiquement:
  - Compte utilisateur (role: professeur)
  - Email envoyé avec identifiants
  - Statut: "validé"

### 4. Admin Assigne Étudiants
- Admin assigne des étudiants au prof
- Prof voit uniquement SES étudiants

### 5. Prof Gère Ses Étudiants
- Saisie notes
- Envoi notifications
- Gestion emploi du temps
- Uniquement pour ses étudiants assignés

---

## 📊 Modèle Backend

```python
class DemandeInscriptionProfesseur(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('rejetee', 'Rejetée')
    ]
    
    # Infos personnelles
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    
    # Infos professionnelles
    specialite = models.CharField(max_length=200)  # Ex: Mathématiques
    diplome = models.CharField(max_length=200)  # Ex: Doctorat en Maths
    experience = models.IntegerField()  # Années d'expérience
    cv = models.FileField(upload_to='cv_profs/', null=True)
    
    # Gestion
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    date_demande = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)
    utilisateur_cree = models.ForeignKey(Utilisateur, null=True, on_delete=models.SET_NULL)
    commentaire_admin = models.TextField(blank=True)
```

---

## 🔗 API Endpoints

```
POST   /api/demandes-inscription-professeur/     → Créer demande (public)
GET    /api/demandes-inscription-professeur/     → Liste (admin only)
GET    /api/demandes-inscription-professeur/:id/ → Détail (admin only)
POST   /api/demandes-inscription-professeur/:id/valider/   → Valider
POST   /api/demandes-inscription-professeur/:id/rejeter/   → Rejeter
```

---

## 📱 Page d'Inscription Prof

URL: `/inscription-professeur.html`

Champs:
- Nom, Prénom
- Email, Téléphone
- Spécialité (ex: Mathématiques, Physique, etc.)
- Diplôme (ex: Licence, Master, Doctorat)
- Années d'expérience
- CV (upload fichier)
- Lettre de motivation (optionnel)

---

## 👔 Dashboard Admin

Nouvelle section: "Demandes Professeurs"

Affiche:
- Liste des demandes en attente
- Infos du prof
- Boutons: Valider / Rejeter
- Historique des demandes

---

## ✅ À Implémenter

1. Backend:
   - Modèle DemandeInscriptionProfesseur
   - ViewSet avec actions valider/rejeter
   - Serializer
   - Migration

2. Frontend:
   - Page inscription-professeur.html
   - Section dans dashboard-admin.html
   - Gestion des demandes

3. Email:
   - Email confirmation demande reçue
   - Email validation avec identifiants
   - Email rejet avec raison

---

**Veux-tu que je commence l'implémentation maintenant?**
