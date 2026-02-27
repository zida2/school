@echo off
echo ========================================
echo    DEMARRAGE DU SERVEUR DJANGO
echo ========================================
echo.
echo Demarrage du backend sur http://127.0.0.1:8000/
echo.
echo IMPORTANT: Laissez cette fenetre OUVERTE!
echo.
cd backend
python manage.py runserver
pause
