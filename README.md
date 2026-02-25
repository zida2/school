# 🎓 UniERP BF - Système de Gestion Universitaire Premium

Plateforme ERP ultra premium pour la gestion complète des universités au Burkina Faso.

## 🚀 Démarrage rapide

### 1. Lancer le backend Django
```bash
cd backend
python manage.py runserver
```

### 2. Ouvrir le frontend
Ouvrir `index.html` dans un navigateur moderne

### 3. Se connecter avec les comptes de démonstration

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Super Admin | superadmin@erp.bf | SuperAdmin2024! |
| Admin | admin@uan.bf | Admin2024! |
| Enseignant | j.ouedraogo@uan.bf | enseignant123 |
| Étudiant | m.diallo@etu.bf | etudiant123 |

## 📁 Structure du projet

```
├── backend/                    # Backend Django REST
│   ├── api/                   # Application principale
│   ├── erp_backend/           # Configuration Django
│   └── manage.py              # Script de gestion
├── css/
│   └── dashboard-premium.css  # Design ultra premium
├── js/
│   ├── api.js                 # Fonctions API
│   ├── app.js                 # Application
│   └── data.js                # Données
├── index.html                 # Page de connexion
├── dashboard-admin.html       # Dashboard administrateur
├── dashboard-prof.html        # Dashboard enseignant
├── dashboard-etudiant.html    # Dashboard étudiant
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
