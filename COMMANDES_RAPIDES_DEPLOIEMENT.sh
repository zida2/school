#!/bin/bash
# 🚀 COMMANDES RAPIDES DE DÉPLOIEMENT
# Exécuter sur PythonAnywhere

echo "🚀 Déploiement des notifications email..."
echo ""

# 1. Aller dans le répertoire backend
cd ~/school/backend

# 2. Activer l'environnement virtuel
source ~/.virtualenvs/myenv/bin/activate

# 3. Appliquer les migrations
echo "📦 Application des migrations..."
python manage.py migrate

# 4. Tester le système
echo ""
echo "🧪 Test du système de notifications..."
python tester_notifications_email.py

# 5. Redémarrer l'application
echo ""
echo "🔄 Redémarrage de l'application..."
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py

echo ""
echo "✅ Déploiement terminé!"
echo ""
echo "📝 Prochaines étapes:"
echo "   1. Tester les endpoints API"
echo "   2. Configurer l'envoi d'emails dans .env (optionnel)"
echo "   3. Intégrer les notifications dans les ViewSets"
echo "   4. Supprimer les sections paiements du frontend"
echo ""
echo "🔗 Backend: https://wendlasida.pythonanywhere.com"
echo "🔗 Frontend: https://school-wheat-six.vercel.app"
