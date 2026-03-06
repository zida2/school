# 🚨 DÉPLOIEMENT MANUEL URGENT

## PROBLÈME
Les fichiers sur PythonAnywhere contiennent encore des références à `Paiement` qui n'existe plus.

## SOLUTION

### Sur votre machine Windows:

1. **Vérifiez que tous les fichiers sont corrects localement**
2. **Poussez TOUT sur GitHub**:

```powershell
cd C:\Users\Dési InnovaTech\Desktop\school
git add -A
git commit -m "Backend complet: suppression paiements + notifications email"
git push origin main --force
```

### Sur PythonAnywhere:

Une fois le push réussi, exécutez:

```bash
cd ~
rm -rf school
git clone https://github.com/zida2/school.git
cd school/backend
source ~/.virtualenvs/myenv/bin/activate
python manage.py migrate
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

## ALTERNATIVE: Déploiement sans Git

Si Git ne fonctionne pas, uploadez manuellement via l'interface Files de PythonAnywhere:

### Fichiers à uploader dans `/home/Wendlasida/school/backend/api/`:
1. `models.py`
2. `serializers.py`
3. `views.py`
4. `urls.py`
5. `admin.py`
6. `email_service.py` (nouveau)

### Fichiers à uploader dans `/home/Wendlasida/school/backend/`:
1. `tester_notifications_email.py` (nouveau)

### Après l'upload:
```bash
cd ~/school/backend
source ~/.virtualenvs/myenv/bin/activate
python manage.py migrate
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

## VÉRIFICATION

Après le déploiement, testez:

```bash
python manage.py shell -c "from api.models import NotificationEmail, PreferenceNotification; print('OK')"
```

Si vous voyez "OK", le déploiement a réussi!

## FRONTEND

Le frontend est déjà prêt. Poussez sur Vercel:

```powershell
git push origin main
```

Vercel déploiera automatiquement.

---

**Date**: 6 mars 2026  
**Statut**: EN ATTENTE DU PUSH GITHUB
