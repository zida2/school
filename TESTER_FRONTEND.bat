@echo off
echo ========================================
echo   SERVEUR WEB LOCAL - FRONTEND
echo ========================================
echo.
echo Le serveur va demarrer sur: http://localhost:8080
echo.
echo Pour tester l'inscription professeur:
echo http://localhost:8080/frontend/inscription-professeur-v2.html
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.
echo ========================================
echo.

cd frontend
python -m http.server 8080

pause
