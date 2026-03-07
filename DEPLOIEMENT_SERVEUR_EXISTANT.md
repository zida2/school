# 🚀 Déploiement sur serveur existant

Guide pour déployer UniERP BF sur le serveur existant du client.

## 📋 Prérequis serveur

### Informations nécessaires
- [ ] Adresse IP ou nom de domaine du serveur
- [ ] Accès SSH (utilisateur + mot de passe ou clé SSH)
- [ ] Système d'exploitation (Ubuntu, CentOS, etc.)
- [ ] Accès root ou sudo

### Logiciels requis
- Docker et Docker Compose
- Git
- Nginx (optionnel si Docker gère tout)

## 🔧 Étape 1: Connexion au serveur

```bash
# Se connecter via SSH
ssh utilisateur@IP_SERVEUR

# Ou avec une clé SSH
ssh -i chemin/vers/cle.pem utilisateur@IP_SERVEUR
```

## 📦 Étape 2: Installation de Docker

### Ubuntu/Debian
```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER

# Installer Docker Compose
sudo apt install docker-compose-plugin -y

# Vérifier l'installation
docker --version
docker compose version
```

### CentOS/RHEL
```bash
# Installer Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# Démarrer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
```

## 📥 Étape 3: Récupérer le code

```bash
# Créer un dossier pour l'application
mkdir -p ~/unierp
cd ~/unierp

# Cloner le repository (si Git est configuré)
git clone https://github.com/VOTRE_USERNAME/unierp.git .

# OU transférer les fichiers via SCP depuis votre machine locale
# Sur votre machine locale:
# scp -r ./unierp utilisateur@IP_SERVEUR:~/unierp/
```

## ⚙️ Étape 4: Configuration

```bash
cd ~/unierp

# Copier le fichier d'environnement
cp .env.docker .env

# Éditer la configuration
nano .env
```

### Configuration minimale (.env)

```env
# Django
SECRET_KEY=GENERER_UNE_CLE_SECURISEE_ICI
DEBUG=False
ALLOWED_HOSTS=IP_SERVEUR,votre-domaine.com

# Base de données
DB_NAME=erp_universitaire
DB_USER=postgres
DB_PASSWORD=MOT_DE_PASSE_SECURISE_BDD
DB_HOST=db
DB_PORT=5432

# Admin
ADMIN_EMAIL=admin@unierp.bf
ADMIN_PASSWORD=MOT_DE_PASSE_ADMIN_SECURISE

# Email (IMPORTANT)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=email-universite@gmail.com
EMAIL_HOST_PASSWORD=mot_de_passe_app_gmail
DEFAULT_FROM_EMAIL=noreply@unierp.bf

# Frontend
FRONTEND_URL=http://IP_SERVEUR
CORS_ORIGINS=http://IP_SERVEUR,http://localhost
```

### Générer une SECRET_KEY sécurisée

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🚀 Étape 5: Lancer l'application

```bash
# Lancer tous les services
docker compose up -d

# Vérifier que tout fonctionne
docker compose ps

# Voir les logs
docker compose logs -f
```

## 🔥 Étape 6: Configuration du pare-feu

```bash
# Installer UFW (si pas déjà installé)
sudo apt install ufw -y

# Autoriser SSH (IMPORTANT!)
sudo ufw allow 22/tcp

# Autoriser HTTP et HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Activer le pare-feu
sudo ufw enable

# Vérifier le statut
sudo ufw status
```

## 🌐 Étape 7: Configuration du nom de domaine (optionnel)

Si vous avez un nom de domaine:

### 1. Configurer les DNS

Dans votre registrar de domaine (Namecheap, GoDaddy, etc.):

```
Type: A
Name: @
Value: IP_SERVEUR
TTL: 3600

Type: A
Name: www
Value: IP_SERVEUR
TTL: 3600
```

### 2. Attendre la propagation DNS (5-30 minutes)

```bash
# Vérifier la propagation
nslookup votre-domaine.com
```

### 3. Configurer SSL avec Let's Encrypt

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenir un certificat SSL
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

# Le certificat se renouvelle automatiquement
# Tester le renouvellement:
sudo certbot renew --dry-run
```

### 4. Mettre à jour la configuration

Modifier `nginx/conf.d/default.conf` pour activer HTTPS (décommenter les lignes SSL).

```bash
# Redémarrer Nginx
docker compose restart nginx
```

## ✅ Étape 8: Vérification

### Tester l'accès

```bash
# Backend API
curl http://IP_SERVEUR/api/

# Frontend
curl http://IP_SERVEUR/

# Health check
curl http://IP_SERVEUR/health
```

### Accéder depuis un navigateur

- **Frontend**: http://IP_SERVEUR
- **Mobile**: http://IP_SERVEUR/mobile/
- **Django Admin**: http://IP_SERVEUR/admin/

### Identifiants par défaut

- Email: admin@unierp.bf
- Mot de passe: (celui configuré dans .env)

## 🔄 Mises à jour

```bash
# Se connecter au serveur
ssh utilisateur@IP_SERVEUR
cd ~/unierp

# Récupérer les dernières modifications
git pull origin main

# Reconstruire et redémarrer
docker compose down
docker compose up -d --build

# Vérifier les logs
docker compose logs -f
```

## 💾 Sauvegardes

### Sauvegarde manuelle

```bash
# Sauvegarder la base de données
docker compose exec -T db pg_dump -U postgres erp_universitaire > backup_$(date +%Y%m%d).sql

# Sauvegarder les fichiers médias
tar -czf media_backup_$(date +%Y%m%d).tar.gz backend/media/
```

### Sauvegarde automatique

Créer `/home/utilisateur/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/home/utilisateur/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

cd /home/utilisateur/unierp
docker compose exec -T db pg_dump -U postgres erp_universitaire > $BACKUP_DIR/db_$DATE.sql
tar -czf $BACKUP_DIR/media_$DATE.tar.gz backend/media/

# Garder seulement les 7 dernières sauvegardes
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +7 -delete

echo "Sauvegarde terminée: $DATE"
```

Rendre exécutable et automatiser:

```bash
chmod +x /home/utilisateur/backup.sh

# Ajouter au crontab (sauvegarde quotidienne à 2h)
crontab -e
# Ajouter: 0 2 * * * /home/utilisateur/backup.sh >> /home/utilisateur/backup.log 2>&1
```

## 🐛 Dépannage

### Les services ne démarrent pas

```bash
# Voir les logs détaillés
docker compose logs backend
docker compose logs db
docker compose logs nginx

# Vérifier l'espace disque
df -h

# Vérifier la mémoire
free -h
```

### Erreur de connexion à la base de données

```bash
# Vérifier que PostgreSQL est prêt
docker compose exec db pg_isready -U postgres

# Redémarrer les services
docker compose restart db
sleep 10
docker compose restart backend
```

### Port déjà utilisé

```bash
# Vérifier les ports utilisés
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443

# Arrêter le service qui utilise le port
sudo systemctl stop apache2  # ou nginx
```

## 📊 Monitoring

### Vérifier l'état des services

```bash
# Statut des containers
docker compose ps

# Utilisation des ressources
docker stats

# Espace disque
df -h

# Mémoire
free -h
```

### Logs

```bash
# Logs en temps réel
docker compose logs -f

# Logs d'un service spécifique
docker compose logs -f backend

# Logs système
sudo journalctl -u docker -f
```

## 🔐 Sécurité

### Checklist de sécurité

- [ ] SECRET_KEY changée
- [ ] DEBUG=False
- [ ] Mots de passe forts (DB, admin)
- [ ] Pare-feu configuré
- [ ] SSH sécurisé (clé SSH, pas de root)
- [ ] SSL/HTTPS activé
- [ ] Sauvegardes automatiques
- [ ] Monitoring actif

### Sécuriser SSH

```bash
# Éditer la configuration SSH
sudo nano /etc/ssh/sshd_config

# Modifier:
PermitRootLogin no
PasswordAuthentication no  # Si vous utilisez des clés SSH

# Redémarrer SSH
sudo systemctl restart sshd
```

## 📞 Support

En cas de problème:

1. Vérifier les logs: `docker compose logs -f`
2. Vérifier l'espace disque: `df -h`
3. Vérifier la mémoire: `free -h`
4. Redémarrer les services: `docker compose restart`

---

**Temps estimé de déploiement**: 1-2 heures  
**Difficulté**: Moyenne  
**Prérequis**: Connaissances de base en Linux et Docker
