# 🎓 UniERP BF - Système de Gestion Universitaire

Système ERP complet pour la gestion universitaire avec backend Django, frontend web et application mobile PWA.

## � Structure du projet

```
unierp/
├── backend/              # Backend Django REST API
│   ├── api/             # Application principale
│   ├── erp_backend/     # Configuration Django
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/            # Frontend Web (Admin, Services, Professeurs)
│   ├── css/            # Styles
│   ├── js/             # Scripts JavaScript
│   ├── *.html          # Pages HTML
│   └── vercel.json     # Configuration Vercel
│
├── mobile/             # Application Mobile PWA (Étudiants)
│   ├── index.html      # Page principale
│   ├── dashboard.html  # Dashboard étudiant
│   ├── inscription.html
│   ├── styles.css
│   ├── sw.js          # Service Worker
│   └── manifest.json  # Manifest PWA
│
├── nginx/              # Configuration Nginx
│   ├── nginx.conf
│   └── conf.d/
│
├── docker-compose.yml  # Configuration Docker production
├── docker-compose.dev.yml  # Configuration Docker développement
└── .env.docker        # Variables d'environnement
```

## 🚀 Démarrage rapide

### Avec Docker (Recommandé)

```bash
# 1. Configuration
cp .env.docker .env
nano .env  # Modifier les valeurs

# 2. Lancer tous les services
docker compose up -d

# 3. Accéder à l'application
# Frontend: http://localhost
# Mobile: http://localhost/mobile/
# Admin: http://localhost/admin/
```

### Sans Docker (Développement local)

**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
# Ouvrir index.html dans un navigateur
# Ou utiliser un serveur local: python -m http.server 8080
```

## 🌐 URLs de l'application

### Production
- **Frontend**: https://school-wheat-six.vercel.app
- **Mobile**: https://school-wheat-six.vercel.app/mobile/
- **Backend API**: https://wendlasida.pythonanywhere.com/api/
- **Django Admin**: https://wendlasida.pythonanywhere.com/admin/

### Local (Docker)
- **Frontend**: http://localhost
- **Mobile**: http://localhost/mobile/
- **Backend API**: http://localhost/api/
- **Django Admin**: http://localhost/admin/

## 👥 Utilisateurs du système

### 1. Administrateur
- **Accès**: `frontend/connexion-admin.html`
- **Rôle**: Gestion complète du système
- **Identifiants par défaut**: admin@unierp.bf / Admin2026

### 2. Services Administratifs
- **Communication**: `frontend/connexion-communication.html`
- **Académique**: `frontend/connexion-academique.html`
- **Comptabilité**: `frontend/connexion-comptabilite.html`

### 3. Professeurs
- **Accès**: `frontend/connexion-professeur.html`
- **Inscription**: `frontend/inscription-professeur.html`

### 4. Étudiants
- **Accès**: `mobile/index.html`
- **Inscription**: `mobile/inscription.html`

## 🔧 Configuration

### Variables d'environnement (.env)

```env
# Django
SECRET_KEY=votre-clé-secrète
DEBUG=False
ALLOWED_HOSTS=localhost,votre-domaine.com

# Base de données
DB_NAME=erp_universitaire
DB_USER=postgres
DB_PASSWORD=mot_de_passe_securise
DB_HOST=db
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
DEFAULT_FROM_EMAIL=noreply@unierp.bf

# Admin
ADMIN_EMAIL=admin@unierp.bf
ADMIN_PASSWORD=Admin2026
```

## � Déploiement

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

### Mobile (Vercel)
```bash
cd mobile
vercel --prod
```

### Backend (Docker)
```bash
docker compose up -d
```

Voir les guides détaillés:
- [GUIDE_DOCKER.md](GUIDE_DOCKER.md) - Guide complet Docker
- [README_DOCKER.md](README_DOCKER.md) - Documentation Docker rapide

## 🛠️ Commandes utiles

### Docker
```bash
# Démarrer
docker compose up -d

# Arrêter
docker compose down

# Logs
docker compose logs -f

# Shell Django
docker compose exec backend python manage.py shell

# Migrations
docker compose exec backend python manage.py migrate

# Créer superadmin
docker compose exec backend python manage.py createsuperuser
```

### Backend (sans Docker)
```bash
cd backend

# Migrations
python manage.py makemigrations
python manage.py migrate

# Créer superadmin
python manage.py createsuperuser

# Collecter fichiers statiques
python manage.py collectstatic

# Lancer serveur
python manage.py runserver
```

## 📚 Fonctionnalités

### Administration
- ✅ Gestion des étudiants
- ✅ Gestion des enseignants
- ✅ Gestion des filières et matières
- ✅ Validation des inscriptions
- ✅ Gestion des paiements
- ✅ Emploi du temps
- ✅ Statistiques et rapports

### Services Administratifs
- ✅ Communication: Publications, événements
- ✅ Académique: Emploi du temps, programmes
- ✅ Comptabilité: Paiements, frais

### Étudiants (Mobile)
- ✅ Inscription en ligne
- ✅ Consultation des notes
- ✅ Emploi du temps
- ✅ Paiements
- ✅ Notifications
- ✅ Mode hors ligne (PWA)

### Professeurs
- ✅ Saisie des notes
- ✅ Gestion des présences
- ✅ Emploi du temps
- ✅ Liste des étudiants

## 🔐 Sécurité

- Authentification JWT
- Permissions par rôle
- HTTPS en production
- CORS configuré
- Validation des données
- Protection CSRF

## 📞 Support

Pour toute question ou problème:
- Documentation: Voir les fichiers MD dans le projet
- Issues: Créer une issue sur GitHub

## 📄 Licence

Propriétaire - UniERP BF

---

**Version**: 1.0.0  
**Dernière mise à jour**: 6 Mars 2026
