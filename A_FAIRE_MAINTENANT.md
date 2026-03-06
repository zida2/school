# ⚡ À FAIRE MAINTENANT

## 1. DÉPLOYER SUR PYTHONANYWHERE (5 min)

Ouvrir: https://www.pythonanywhere.com/user/wendlasida/

Copier-coller dans Bash Console:
```bash
cd ~/school/backend
git pull origin main
python manage.py migrate
python manage.py check
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

## 2. VÉRIFIER VERCEL (1 min)

Ouvrir: https://school-wheat-six.vercel.app/accueil.html

Vérifier que la page s'affiche correctement.

## 3. TESTER UNE INSCRIPTION (2 min)

1. Aller sur: https://school-wheat-six.vercel.app/accueil.html
2. Cliquer "Service Communication" → "S'inscrire"
3. Remplir le formulaire
4. Vérifier le message de succès

## 4. VALIDER DANS ADMIN (2 min)

1. Aller sur: https://wendlasida.pythonanywhere.com/admin/
2. Se connecter
3. Aller dans "Demandes Service Communication"
4. Valider la demande
5. Noter le mot de passe généré

## 5. TESTER LA CONNEXION (1 min)

1. Aller sur: https://school-wheat-six.vercel.app/connexion-communication.html
2. Se connecter avec les identifiants
3. Vérifier la redirection

---

## ✅ RÉSULTAT

Le système sera 100% opérationnel!

**TEMPS TOTAL: 11 minutes**
