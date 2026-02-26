# 🎓 UniERP BF - Système de Gestion Universitaire Premium

Système ERP complet pour la gestion universitaire au Burkina Faso.

---

## 📊 État du Projet

```
Backend:     ████████░░ 80% - Code prêt, intégration manuelle requise
Frontend:    ███░░░░░░░ 30% - Étudiant OK, autres espaces à compléter
Design:      ██████████ 100% - Responsive et moderne
Tests:       ██░░░░░░░░ 20% - Tests de base effectués
Docs:        ██████████ 100% - Documentation complète
```

**Statut Global**: 🟡 EN COURS (40% complété)

---

## 🚀 Démarrage Rapide

### 1. Installation

```bash
# Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend (dans un autre terminal)
python -m http.server 8080
```

### 2. Accès

- **Frontend**: http://127.0.0.1:8080/index.html
- **Backend API**: http://127.0.0.1:8000/api/
- **Admin Django**: http://127.0.0.1:8000/admin/

### 3. Connexion

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Super Admin | superadmin@uan.bf | super123 |
| Admin | admin@uan.bf | admin123 |
| Enseignant | j.ouedraogo@uan.bf | enseignant123 |
| Étudiant | m.diallo@etu.bf | etudiant123 |
| Bureau Exécutif | bureau@uan.bf | bureau123 |

---

## 📚 Documentation

### 🎯 Pour Démarrer
1. **[LISEZMOI_INTEGRATION.md](LISEZMOI_INTEGRATION.md)** - Guide de démarrage
2. **[GUIDE_INTEGRATION_RAPIDE.md](GUIDE_INTEGRATION_RAPIDE.md)** - Démarrage rapide (2h)
3. **[ETAT_INTEGRATION_COMPLET.md](ETAT_INTEGRATION_COMPLET.md)** - État actuel

### 📋 Documentation Complète
- **[INDEX_DOCUMENTATION.md](INDEX_DOCUMENTATION.md)** - Index de tous les documents
- **[PLAN_INTEGRATION_COMPLETE.md](PLAN_INTEGRATION_COMPLETE.md)** - Plan détaillé
- **[INTEGRATION_COMPLETE_RESUME.md](INTEGRATION_COMPLETE_RESUME.md)** - Résumé final

### 🔧 Documentation Technique
- **[backend/INTEGRATION_ETAPE_1.md](backend/INTEGRATION_ETAPE_1.md)** - Instructions backend
- **[backend/api/views_extensions.py](backend/api/views_extensions.py)** - Code à intégrer

---

## ✨ Fonctionnalités

### ✅ Implémentées

#### Espace Étudiant
- ✅ Dashboard avec statistiques
- ✅ Consultation des notes
- ✅ Emploi du temps
- ✅ Paiements et solde
- ✅ Supports de cours
- ✅ Création de demandes
- ✅ Création de réclamations
- ✅ Affichage publications
- ✅ Affichage sondages
- ✅ Déclaration objets perdus

#### Espace Admin (Partiel)
- ✅ Dashboard avec statistiques
- ✅ Gestion étudiants (CRUD)
- ✅ Gestion enseignants (CRUD)
- ✅ Gestion filières
- ✅ Emploi du temps
- ✅ Paiements

#### Design
- ✅ Interface moderne dark theme
- ✅ Responsive (mobile, tablette, desktop)
- ✅ Animations fluides
- ✅ Page de connexion responsive

### 🔄 En Cours

#### Backend
- 🔄 Intégration des extensions dans views.py
- 🔄 Tests des endpoints

#### Frontend
- 🔄 Pages admin manquantes
- 🔄 Pages enseignant manquantes
- 🔄 Pages bureau manquantes

### ⏳ À Venir

#### Flux de Communication
- ⏳ Admin → Répondre demandes → Étudiant
- ⏳ Enseignant → Traiter réclamations → Étudiant
- ⏳ Bureau → Créer publications → Étudiants
- ⏳ Bureau → Créer sondages → Étudiants
- ⏳ Étudiant → Participer sondages → Bureau
- ⏳ Étudiant → Remplir questionnaires → Enseignant

#### Système
- ⏳ Notifications en temps réel
- ⏳ Badges de compteur
- ⏳ Messagerie interne

---

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS)
    ↓ API REST (JWT)
Backend (Django REST Framework)
    ↓ ORM
Base de données (SQLite)
```

### Technologies

**Backend**:
- Django 4.2
- Django REST Framework
- JWT Authentication
- SQLite (dev) / PostgreSQL (prod)

**Frontend**:
- HTML5, CSS3
- JavaScript ES6+ (Vanilla)
- Chart.js (graphiques)
- Fetch API

**Design**:
- Dark theme
- Responsive design
- Animations CSS
- Mobile-first

---

## 📁 Structure du Projet

```
unierpbf/
├── backend/
│   ├── api/
│   │   ├── models.py              # Modèles Django
│   │   ├── serializers.py         # Serializers DRF
│   │   ├── views.py               # ViewSets
│   │   ├── views_extensions.py   # ← Code à intégrer
│   │   ├── urls.py                # Routes API
│   │   └── permissions.py         # Permissions
│   ├── erp_backend/
│   │   ├── settings.py            # Configuration
│   │   └── urls.py                # URLs principales
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html                 # Page de connexion
│   ├── dashboard-etudiant.html    # ✅ Fonctionnel
│   ├── dashboard-admin.html       # ⚠️ À compléter
│   ├── dashboard-prof.html        # ⚠️ À compléter
│   ├── dashboard-bureau.html      # ⚠️ À compléter
│   ├── css/
│   │   └── dashboard-premium.css  # Styles
│   └── js/
│       ├── api.js                 # API wrapper
│       ├── mock-data.js           # Données mock
│       └── fix-navigation.js      # Navigation
│
└── docs/
    ├── LISEZMOI_INTEGRATION.md
    ├── GUIDE_INTEGRATION_RAPIDE.md
    ├── ETAT_INTEGRATION_COMPLET.md
    ├── PLAN_INTEGRATION_COMPLETE.md
    ├── INDEX_DOCUMENTATION.md
    └── ... (13 fichiers de documentation)
```

---

## 🎯 Prochaines Étapes

### Priorité 1: Backend (2h)
1. Intégrer le code dans views.py (45min)
2. Tester les endpoints (30min)
3. Frontend Admin - Demandes (45min)

### Priorité 2: Flux Réclamations (4h)
4. Frontend Admin - Réclamations (1h)
5. Frontend Enseignant - Réclamations (1h)
6. Frontend Étudiant - Réponses (1h)
7. Tests flux complets (1h)

### Priorité 3: Publications & Sondages (6h)
8. Frontend Bureau - Publications (1h30)
9. Frontend Bureau - Sondages (2h)
10. Frontend Étudiant - Sondages (1h)
11. Tests (1h30)

**Temps total estimé**: ~19 heures

---

## 🧪 Tests

### Tests Backend

```bash
cd backend
python manage.py test

# Tests manuels avec curl
curl -X GET http://127.0.0.1:8000/api/reclamations/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Tests Frontend

1. Ouvrir http://127.0.0.1:8080/index.html
2. Se connecter avec un compte test
3. Vérifier que le dashboard s'affiche
4. Tester les fonctionnalités

---

## 📝 Contribution

### Workflow

1. Lire `LISEZMOI_INTEGRATION.md`
2. Suivre `GUIDE_INTEGRATION_RAPIDE.md`
3. Intégrer le backend avec `backend/INTEGRATION_ETAPE_1.md`
4. Développer le frontend selon `PLAN_INTEGRATION_COMPLETE.md`
5. Tester et documenter

### Conventions

- **Backend**: snake_case, Django conventions
- **Frontend**: camelCase, ES6+
- **CSS**: kebab-case, BEM-like
- **Commits**: Conventional Commits
- **Documentation**: Markdown

---

## 📞 Support

### Documentation
- Consultez `INDEX_DOCUMENTATION.md` pour naviguer
- Lisez `GUIDE_INTEGRATION_RAPIDE.md` pour l'aide

### Problèmes Courants

**Serveur ne démarre pas**:
```bash
cd backend
python manage.py migrate
python manage.py runserver
```

**Erreur 401 (Non autorisé)**:
- Se reconnecter
- Vérifier le token JWT

**Erreur 403 (Interdit)**:
- Vérifier le rôle de l'utilisateur
- Vérifier les permissions

**Frontend ne charge pas**:
- Vider le cache (Ctrl+Shift+R)
- Vérifier la console (F12)
- Vérifier que le serveur tourne

---

## 🔐 Sécurité

- ✅ Authentification JWT
- ✅ Permissions par rôle
- ✅ Protection CSRF
- ✅ Validation des données
- ✅ Filtrage des requêtes
- ⚠️ Rate limiting (à ajouter)
- ⚠️ HTTPS (production)

---

## 📱 Responsive

L'interface fonctionne sur:
- ✅ Desktop (1920x1080+)
- ✅ Laptop (1366x768+)
- ✅ Tablette (768x1024+)
- ✅ Mobile (375x667+)

Breakpoints:
- 1024px (tablette)
- 640px (mobile)
- 400px (petit mobile)

---

## 📊 Statistiques

- **Lignes de code**: ~10,000+
- **Lignes de documentation**: ~3,500+
- **Fichiers de documentation**: 13
- **Temps de développement**: 40+ heures
- **Temps restant estimé**: 19 heures
- **Progression**: 40%

---

## 🎓 Équipe

Développé avec ❤️ pour l'Université Aube Nouvelle, Burkina Faso 🇧🇫

---

## 📄 Licence

Propriétaire - Tous droits réservés

---

## 🎉 Remerciements

Merci à tous les contributeurs et testeurs qui ont rendu ce projet possible.

---

**Dernière mise à jour**: 26 février 2026  
**Version**: 1.0.0-beta  
**Statut**: 🟡 EN DÉVELOPPEMENT

**Pour commencer, lisez [LISEZMOI_INTEGRATION.md](LISEZMOI_INTEGRATION.md)!**
