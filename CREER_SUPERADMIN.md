# 👤 CRÉER UN COMPTE SUPER ADMIN

## 📋 COMMANDES PYTHONANYWHERE

### 1. Ouvrir un Bash Console sur PythonAnywhere

### 2. Naviguer vers le projet
```bash
cd ~/school/backend
```

### 3. Activer l'environnement virtuel
```bash
source ~/.virtualenvs/myenv/bin/activate
```

### 4. Créer le superadmin
```bash
python manage.py createsuperuser
```

### 5. Répondre aux questions:

```
Email: admin@unierp.bf
Prénom: Admin
Nom: Système
Password: [Choisir un mot de passe sécurisé]
Password (again): [Répéter le mot de passe]
```

**Exemple de mot de passe sécurisé**: `UniERP2026!Admin`

---

## ✅ RÉSULTAT

```
Superuser created successfully.
```

---

## 🔐 ACCÈS DJANGO ADMIN

### URL: https://wendlasida.pythonanywhere.com/admin/

### Identifiants:
- **Email**: admin@unierp.bf
- **Mot de passe**: [Le mot de passe que tu as choisi]

---

## 📊 CE QUE TU POURRAS FAIRE

Une fois connecté sur Django Admin, tu pourras:

### 1. Voir toutes les demandes d'inscription
- Demandes Service Communication
- Demandes Service Académique
- Demandes Service Comptabilité
- Demandes Inscription Professeur
- Demandes Inscription Étudiant

### 2. Valider les demandes
- Cliquer sur une demande
- Voir les détails
- Valider ou rejeter

### 3. Gérer tous les utilisateurs
- Voir tous les comptes créés
- Modifier les informations
- Désactiver des comptes

### 4. Gérer toutes les données
- Universités
- Filières
- Classes
- Notes
- Paiements
- Etc.

---

## 🧪 TEST COMPLET

### Étape 1: Créer le superadmin
```bash
cd ~/school/backend
source ~/.virtualenvs/myenv/bin/activate
python manage.py createsuperuser
```

### Étape 2: Se connecter
1. Ouvrir: https://wendlasida.pythonanywhere.com/admin/
2. Entrer: admin@unierp.bf
3. Entrer: [ton mot de passe]
4. Cliquer "Se connecter"

### Étape 3: Tester une inscription
1. Ouvrir: https://school-wheat-six.vercel.app/inscription-communication.html
2. Remplir le formulaire
3. Envoyer

### Étape 4: Valider dans Django Admin
1. Aller dans "Demandes Service Communication"
2. Voir la nouvelle demande
3. Cliquer dessus
4. Noter l'ID (ex: 1)

### Étape 5: Valider via l'API
Sur PythonAnywhere Bash Console:
```bash
cd ~/school/backend
python manage.py shell
```

```python
from api.models import DemandeInscriptionCommunication, Utilisateur
from django.utils import timezone
import uuid

# Récupérer la demande
demande = DemandeInscriptionCommunication.objects.first()

# Générer mot de passe
password = f"comm{uuid.uuid4().hex[:8]}"

# Créer utilisateur
utilisateur = Utilisateur.objects.create_user(
    email=demande.email,
    password=password,
    prenom=demande.prenom,
    nom=demande.nom,
    role='communication'
)

# Mettre à jour demande
demande.statut = 'validee'
demande.date_traitement = timezone.now()
demande.utilisateur_cree = utilisateur
demande.save()

# Afficher le mot de passe
print(f"Email: {utilisateur.email}")
print(f"Mot de passe: {password}")
```

### Étape 6: Tester la connexion
1. Ouvrir: https://school-wheat-six.vercel.app/connexion-communication.html
2. Entrer l'email et le mot de passe affichés
3. Se connecter

---

## 🎯 RÉSUMÉ

**Commande unique pour créer le superadmin**:
```bash
cd ~/school/backend && source ~/.virtualenvs/myenv/bin/activate && python manage.py createsuperuser
```

**Identifiants suggérés**:
- Email: admin@unierp.bf
- Mot de passe: UniERP2026!Admin

**URL Django Admin**: https://wendlasida.pythonanywhere.com/admin/

---

## 🔒 SÉCURITÉ

⚠️ **IMPORTANT**: 
- Ne partage JAMAIS le mot de passe admin
- Change-le régulièrement
- Utilise un mot de passe fort (min 12 caractères, majuscules, minuscules, chiffres, symboles)

**Bon mot de passe**: `UniERP2026!Admin#Secure`
**Mauvais mot de passe**: `admin123`
