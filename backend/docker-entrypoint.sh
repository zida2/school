#!/bin/bash
set -e

echo "🔄 Attente de la base de données..."
python << END
import sys
import time
import psycopg2
from decouple import config

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        conn = psycopg2.connect(
            dbname=config('DB_NAME', default='erp_universitaire'),
            user=config('DB_USER', default='postgres'),
            password=config('DB_PASSWORD', default='postgres'),
            host=config('DB_HOST', default='db'),
            port=config('DB_PORT', default='5432')
        )
        conn.close()
        print("✅ Base de données prête!")
        sys.exit(0)
    except psycopg2.OperationalError:
        retry_count += 1
        print(f"⏳ Tentative {retry_count}/{max_retries}...")
        time.sleep(2)

print("❌ Impossible de se connecter à la base de données")
sys.exit(1)
END

echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "🔄 Application des migrations..."
python manage.py migrate --noinput

echo "👤 Création du superadmin si nécessaire..."
python manage.py shell << END
from api.models import Utilisateur
from decouple import config

admin_email = config('ADMIN_EMAIL', default='admin@unierp.bf')
admin_password = config('ADMIN_PASSWORD', default='Admin2026')

if not Utilisateur.objects.filter(email=admin_email).exists():
    Utilisateur.objects.create_superuser(
        email=admin_email,
        password=admin_password,
        nom='Administrateur',
        prenom='Système',
        role='admin'
    )
    print(f"✅ Superadmin créé: {admin_email}")
else:
    print(f"ℹ️  Superadmin existe déjà: {admin_email}")
END

echo "🚀 Démarrage du serveur..."
exec "$@"
