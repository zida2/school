@echo off
echo ========================================
echo    DEMARRAGE DU SERVEUR FRONTEND
echo ========================================
echo.
echo Demarrage du frontend sur http://127.0.0.1:8080/
echo.
echo IMPORTANT: Laissez cette fenetre OUVERTE!
echo.
python -m http.server 8080
pause
