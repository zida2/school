#!/bin/bash

# Script de déploiement final
# À exécuter sur PythonAnywhere

echo "🚀 DÉPLOIEMENT BACKEND - DÉBUT"
echo "================================"

# 1. Aller dans le répertoire backend
echo "📁 Navigation vers le répertoire backend..."
cd ~/school/backend

# 2. Activer l'environnement virtuel
echo "🐍 Activation de l'environnement virtuel..."
source ~/.virtualenvs/myenv/bin/activate

# 3. Appliquer les migrations
echo "📊 Application des migrations..."
python manage.py migrate

# 4. Vérifier les migrations
echo "✅ Vérification des migrations..."
python manage.py showmigrations | grep -E "(0009_suppression_paiements|0010_notification_email)"

# 5. Tester le système de notifications
echo "🧪 Test du système de notifications..."
python tester_notifications_email.py

# 6. Redémarrer l'application
echo "🔄 Redémarrage de l'application..."
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py

echo ""
echo "================================"
echo "✅ DÉPLOIEMENT BACKEND - TERMINÉ"
echo ""
echo "📝 Prochaines étapes:"
echo "1. Vérifier les logs: tail -f /var/log/wendlasida.pythonanywhere.com.error.log"
echo "2. Tester l'API: curl https://wendlasida.pythonanywhere.com/api/preferences-notification/"
echo "3. Déployer le frontend sur Vercel (git push)"
echo ""
echo "🎉 Le backend est maintenant déployé!"
