# 🐳 UniERP BF - Configuration Docker

Système ERP Universitaire avec Docker pour un déploiement simplifié.

## 🚀 Démarrage rapide (5 minutes)

```bash
# 1. Cloner le projet
git clone https://github.com/VOTRE_USERNAME/unierp.git
cd unierp

# 2. Configurer l'environnement
cp .env.docker .env
nano .env  # Modifier SECRET_KEY et mots de passe

# 3. Lancer l'application
docker compose up -d

# 4. Accéder à l'application
# Frontend: http://localhost
# Mobile: http://localhost/mobile/
# Admin: http://localhost/admin/
```

**Identifiants par défaut:**
- Email: `admin@unierp.bf`
- Mot de passe: `Admin2026`

## 📦 Architecture

```
┌─────────────────────────────────────────┐
│           Nginx (Port 80/443)           │
│  ┌──────────────┐  ┌─────────────────┐ │
│  │   Frontend   │  │  Mobile (PWA)   │ │
│  └──────────────┘  └─────────────────┘ │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      Backend Django (Port 8000)         │
│  • API REST                             │
│  • Django Admin                         │
│  • Authentification JWT                 │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│     PostgreSQL (Port 5432)              │
│  • Base de données                      │
│  • Volume persistant                    │
└─────────────────────────────────────────┘
```

## 📋 Services

| Service | Port | Description |
|---------|------|-------------|
| Nginx | 80, 443 | Serveur web et reverse proxy |
| Backend | 8000 | API Django REST |
| PostgreSQL | 5432 | Base de données |

## 🛠️ Commandes essentielles

### Gestion des services

```bash
# Démarrer
docker compose up -d

# Arrêter
docker compose down

# Redémarrer
docker compose restart

# Voir les logs
docker compose logs -f

# Statut des services
docker compose ps
```

### Développement

```bash
# Mode développement (avec hot-reload)
docker compose -f docker-compose.dev.yml up

# Accéder au shell Django
docker compose exec backend python manage.py shell

# Créer des migrations
docker compose exec backend python manage.py makemigrations

# Appliquer les migrations
docker compose exec backend python manage.py migrate

# Créer un superadmin
docker compose exec backend python manage.py createsuperuser
```

### Base de données

```bash
# Accéder à PostgreSQL
docker compose exec db psql -U postgres -d erp_universitaire

# Sauvegarder la base
docker compose exec -T db pg_dump -U postgres erp_universitaire > backup.sql

# Restaurer la base
docker compose exec -T db psql -U postgres erp_universitaire < backup.sql
```

## 🔧 Configuration

### Variables d'environnement (.env)

```env
# Django
SECRET_KEY=votre-clé-secrète-très-longue
DEBUG=False
ALLOWED_HOSTS=localhost,votre-domaine.com

# Base de données
DB_NAME=erp_universitaire
DB_USER=postgres
DB_PASSWORD=mot_de_passe_securise
DB_HOST=db
DB_PORT=5432

# Admin par défaut
ADMIN_EMAIL=admin@unierp.bf
ADMIN_PASSWORD=Admin2026

# CORS
CORS_ORIGINS=http://localhost:3000,https://votre-frontend.com
```

### Générer une SECRET_KEY

```bash
docker compose exec backend python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🌐 Déploiement en production

Voir les guides détaillés:
- **[GUIDE_DOCKER.md](GUIDE_DOCKER.md)** - Guide complet Docker
- **[DEPLOIEMENT_SERVEUR_PAYANT.md](DEPLOIEMENT_SERVEUR_PAYANT.md)** - Déploiement sur VPS

### Checklist production

- [ ] Changer `SECRET_KEY`
- [ ] `DEBUG=False`
- [ ] Configurer `ALLOWED_HOSTS`
- [ ] Mots de passe forts
- [ ] Configurer SSL/HTTPS
- [ ] Activer le pare-feu
- [ ] Configurer les sauvegardes
- [ ] Monitoring

## 📊 Monitoring

### Vérifier la santé

```bash
# Statut des containers
docker compose ps

# Utilisation des ressources
docker stats

# Logs d'erreurs
docker compose logs --tail=50 | grep -i error
```

### Health checks

```bash
# Backend
curl http://localhost:8000/api/health

# Nginx
curl http://localhost/health

# Base de données
docker compose exec db pg_isready -U postgres
```

## 🐛 Dépannage

### Le backend ne démarre pas

```bash
# Voir les logs
docker compose logs backend

# Reconstruire
docker compose build --no-cache backend
docker compose up -d
```

### Erreur de connexion à la base

```bash
# Vérifier PostgreSQL
docker compose exec db pg_isready

# Redémarrer les services
docker compose restart db
sleep 10
docker compose restart backend
```

### Réinitialiser complètement

```bash
# ⚠️ ATTENTION: Supprime toutes les données
docker compose down -v
docker compose up -d
```

## 💾 Sauvegardes

### Sauvegarde manuelle

```bash
# Base de données
docker compose exec -T db pg_dump -U postgres erp_universitaire > backup_$(date +%Y%m%d).sql

# Fichiers médias
tar -czf media_backup_$(date +%Y%m%d).tar.gz backend/media/
```

### Sauvegarde automatique

Voir [DEPLOIEMENT_SERVEUR_PAYANT.md](DEPLOIEMENT_SERVEUR_PAYANT.md) pour configurer les sauvegardes automatiques avec cron.

## 🔐 Sécurité

### Bonnes pratiques

1. **Mots de passe forts**: Utilisez des mots de passe complexes
2. **SECRET_KEY unique**: Générez une clé aléatoire
3. **DEBUG=False**: En production
4. **HTTPS**: Utilisez SSL/TLS
5. **Pare-feu**: Limitez les ports ouverts
6. **Sauvegardes**: Automatisez les backups
7. **Mises à jour**: Gardez Docker et les images à jour

## 📚 Documentation

- [GUIDE_DOCKER.md](GUIDE_DOCKER.md) - Guide complet Docker
- [DEPLOIEMENT_SERVEUR_PAYANT.md](DEPLOIEMENT_SERVEUR_PAYANT.md) - Déploiement VPS
- [CAHIER_DES_CHARGES_CLIENT.md](CAHIER_DES_CHARGES_CLIENT.md) - Spécifications

## 🆘 Support

### Problèmes courants

**Port déjà utilisé:**
```bash
# Changer les ports dans docker-compose.yml
ports:
  - "8080:80"  # Au lieu de 80:80
```

**Manque d'espace disque:**
```bash
# Nettoyer Docker
docker system prune -a
```

**Permissions:**
```bash
# Donner les permissions
sudo chown -R $USER:$USER backend/staticfiles backend/media
```

## 💰 Coûts d'hébergement

| Hébergeur | RAM | Prix/mois | Lien |
|-----------|-----|-----------|------|
| DigitalOcean | 2GB | $12 | [digitalocean.com](https://www.digitalocean.com) |
| Linode | 2GB | $10 | [linode.com](https://www.linode.com) |
| Vultr | 2GB | $12 | [vultr.com](https://www.vultr.com) |
| Hetzner | 2GB | €5.83 | [hetzner.com](https://www.hetzner.com) |

## 🎯 Prochaines étapes

1. ✅ Tester localement avec Docker
2. ✅ Choisir un hébergeur
3. ✅ Déployer sur le serveur
4. ✅ Configurer le domaine et SSL
5. ✅ Configurer les sauvegardes
6. ✅ Former les utilisateurs

---

**Version**: 1.0.0  
**Dernière mise à jour**: 6 Mars 2026  
**Licence**: Propriétaire
