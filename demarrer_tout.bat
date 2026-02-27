@echo off
echo ========================================
echo    DEMARRAGE COMPLET DU SYSTEME
echo ========================================
echo.
echo Demarrage du backend et du frontend...
echo.

REM Démarrer le backend dans une nouvelle fenêtre
start "Backend Django" cmd /k "cd backend && python manage.py runserver"

REM Attendre 3 secondes
timeout /t 3 /nobreak > nul

REM Démarrer le frontend dans une nouvelle fenêtre
start "Frontend HTTP" cmd /k "python -m http.server 8080"

REM Attendre 2 secondes
timeout /t 2 /nobreak > nul

REM Ouvrir le navigateur
start http://127.0.0.1:8080/

echo.
echo ========================================
echo    SYSTEME DEMARRE!
echo ========================================
echo.
echo Backend: http://127.0.0.1:8000/
echo Frontend: http://127.0.0.1:8080/
echo.
echo IMPORTANT: Ne fermez PAS les fenetres Backend et Frontend!
echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause > nul
