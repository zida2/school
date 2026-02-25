# 🎓 ERP Universitaire - Université Aube Nouvelle (UAN)

Système de gestion universitaire complet pour l'Université Aube Nouvelle du Burkina Faso.

## 🚀 Fonctionnalités

### 👨‍💼 Espace Administrateur
- Gestion des universités et filières
- Gestion des matières et enseignants
- Gestion des étudiants et inscriptions
- Suivi des paiements
- Statistiques et tableaux de bord
- Gestion des années académiques

### 👨‍🏫 Espace Enseignant
- Consultation des matières enseignées
- Gestion des évaluations (devoirs, interrogations, TP, projets, examens)
- Saisie des notes par évaluation
- Gestion des absences
- Publication des notes
- Consultation des étudiants
- Gestion des supports de cours

### 🎓 Espace Étudiant
- Consultation des notes et moyennes
- Téléchargement du bulletin
- Consultation des paiements
- Accès aux supports de cours
- Emploi du temps
- Notifications

## 🛠️ Technologies

### Backend
- **Django 5.0** - Framework Python
- **Django REST Framework** - API REST
- **SQLite** - Base de données (développement)
- **PostgreSQL** - Base de données (production)

### Frontend
- **HTML5/CSS3etudiant.html    # Dashboard étudiant
├── dashboard-superadmin.html  # Dashboard super admin
└── README.md
```

## ✨ Fonctionnalités

### 👨‍💼 Administrateur
- ✅ Gestion complète des étudiants
- ✅ Gestion des enseignants
- ✅ Gestion des filières et matières
- ✅ Suivi des paiements
- ✅ Statistiques et graphiques en temps réel

### 👨‍🏫 Enseignant
- ✅ Gestion des supports de cours
- ✅ Publication de ressources pédagogiques
- ✅ Consultation des matières enseignées

### 🎓 Étudiant
- ✅ Consultation des notes
- ✅ Accès aux supports de cours
- ✅ Suivi des paiements
- ✅ Emploi du temps

### ⚙️ Super Admin
- ✅ Gestion des universités clientes
- ✅ Gestion des licences SaaS
- ✅ Monitoring système
- ✅ Vue globale des utilisateurs

## 🎨 Design Ultra Premium

- **Thème sombre** avec fond #0a0e27
- **Effets glassmorphism** avec backdrop-filter
- **Animations sophistiquées** et transitions fluides
- **Graphiques Chart.js** avec thème sombre
- **Particules animées** en arrière-plan
- **Responsive design** pour tous les écrans

## 🛠️ Technologies

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Django REST Framework
- **Base de données**: SQLite
- **Graphiques**: Chart.js 4.4.0
- **Fonts**: Poppins, Inter, Outfit

## 📡 API Backend

Le backend expose une API REST sur `http://127.0.0.1:8000/api/`

### Endpoints principaux
- `POST /api/login/` - Authentification
- `GET /api/me/` - Utilisateur connecté
- `GET/POST /api/etudiants/` - Gestion étudiants
- `GET/POST /api/enseignants/` - Gestion enseignants
- `GET/POST /api/filieres/` - Gestion filières
- `GET/POST /api/supports/` - Supports de cours
- `GET /api/dashboard/admin/` - Dashboard admin
- `GET /api/dashboard/prof/` - Dashboard enseignant
- `GET /api/dashboard/etudiant/` - Dashboard étudiant

## 📝 Notes importantes

- **Vider le cache** (Ctrl + F5) après modifications CSS/JS
- Le **backend doit être actif** sur http://127.0.0.1:8000/
- Tous les **boutons d'action** sont fonctionnels
- Les **modals** s'ouvrent et se ferment correctement
- La **navigation** entre pages fonctionne

## 🔧 Installation complète

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install django djangorestframework django-cors-headers
python manage.py migrate
python setup.py  # Créer les données de test
python manage.py runserver
```

### Frontend
Aucune installation nécessaire. Ouvrir `index.html` directement.

## 📄 Licence

Propriétaire - Tous droits réservés

---

**Version 3.0 Ultra Premium** - Février 2025
