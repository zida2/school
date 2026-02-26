# 🎓 ERP Universitaire - Burkina Faso

Système de gestion universitaire complet pour l'Université Aube Nouvelle.

## 🚀 Démarrage Rapide

### Backend (Django)

```bash
cd backend
python manage.py runserver 8000
```

### Frontend

```bash
python -m http.server 8080
```

### Accès

- **Frontend:** http://127.0.0.1:8080/
- **Backend API:** http://127.0.0.1:8000/api/
- **Admin Django:** http://127.0.0.1:8000/admin/

## 👥 Comptes de Test

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Super Admin | superadmin@uan.bf | super123 |
| Admin | admin@uan.bf | admin123 |
| Enseignant | j.ouedraogo@uan.bf | enseignant123 |
| Étudiant | m.diallo@etu.bf | etudiant123 |
| Bureau Exécutif | bureau@uan.bf | bureau123 |

## 📁 Structure

```
├── backend/              # Backend Django
│   ├── api/             # Application principale
│   ├── erp_backend/     # Configuration Django
│   └── manage.py        # Script de gestion Django
├── css/                 # Styles CSS
├── js/                  # Scripts JavaScript
├── dashboard-*.html     # Interfaces utilisateur
└── index.html          # Page de connexion
```

## ✨ Fonctionnalités

### Espace Administrateur
- Gestion des étudiants et enseignants
- Gestion des filières et matières
- Gestion des paiements
- Statistiques et rapports
- Emploi du temps

### Espace Enseignant
- Saisie des notes
- Gestion des évaluations
- Emploi du temps
- Supports de cours
- Statistiques de classe

### Espace Étudiant
- Consultation des notes
- Emploi du temps
- Supports de cours
- Paiements
- Absences
- Demandes administratives

### Bureau Exécutif
- Messagerie interne
- Publications
- Sondages
- Événements
- Gestion des membres
- + Toutes les fonctionnalités étudiant

## 🔧 Configuration

### Prérequis

- Python 3.8+
- Django 6.0+
- SQLite (inclus)

### Installation Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

### Créer un Super Admin

```bash
cd backend
python manage.py createsuperuser
```

## 📊 Technologies

- **Backend:** Django 6.0.2, Django REST Framework
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Base de données:** SQLite
- **API:** REST API avec JWT Authentication

## 🎨 Thèmes

L'application supporte les thèmes clair et sombre. Utilisez le bouton de changement de thème (🌙/☀️) en bas à droite.

## 📱 Responsive

L'interface est entièrement responsive et fonctionne sur:
- Desktop (1920x1080+)
- Laptop (1366x768+)
- Tablet (768x1024+)
- Mobile (375x667+)

## 🔐 Sécurité

- Authentification JWT
- Permissions par rôle
- Protection CSRF
- Validation des données
- Filtrage des requêtes

## 📞 Support

Pour toute question ou problème:
1. Vérifier que le backend est lancé
2. Vérifier que le frontend est lancé
3. Consulter les logs du serveur Django
4. Ouvrir la console du navigateur (F12)

## 📝 Licence

MIT License - Libre d'utilisation

---

**Version:** 1.0.0  
**Université:** Aube Nouvelle  
**Pays:** Burkina Faso 🇧🇫
