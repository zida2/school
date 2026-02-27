#!/usr/bin/env python
"""
Script pour tester la connexion directement
"""

import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur

def test_login_direct():
    print("=" * 60)
    print("🧪 TEST DE CONNEXION DIRECT")
    print("=" * 60)
    print()
    
    # Test 1: Vérifier que le serveur Django tourne
    print("📋 Test 1: Vérifier le serveur Django")
    try:
        response = requests.get('http://127.0.0.1:8000/api/me/', timeout=2)
        print(f"   ✅ Serveur Django accessible (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("   ❌ ERREUR: Serveur Django non accessible!")
        print("   💡 Démarrez le serveur avec: python manage.py runserver")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    print()
    
    # Test 2: Vérifier les comptes dans la base de données
    print("📋 Test 2: Vérifier les comptes")
    comptes = [
        ('Étudiant', 'm.diallo@etu.bf', 'etudiant123'),
        ('Bureau', 'bureau@uan.bf', 'bureau123'),
        ('Enseignant', 'j.ouedraogo@uan.bf', 'enseignant123'),
        ('Admin', 'admin@uan.bf', 'admin123'),
    ]
    
    for role, email, password in comptes:
        try:
            user = Utilisateur.objects.get(email=email)
            pwd_ok = user.check_password(password)
            status = "✅" if pwd_ok else "❌"
            print(f"   {status} {role}: {email} - Password: {'OK' if pwd_ok else 'INCORRECT'}")
        except Utilisateur.DoesNotExist:
            print(f"   ❌ {role}: {email} - COMPTE INTROUVABLE")
    print()
    
    # Test 3: Tester l'API de login pour chaque compte
    print("📋 Test 3: Tester l'API de login")
    for role, email, password in comptes:
        print(f"\n   🔐 Test connexion {role} ({email})...")
        try:
            response = requests.post(
                'http://127.0.0.1:8000/api/login/',
                json={'email': email, 'password': password},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"      ✅ Connexion réussie!")
                print(f"      User: {data.get('user', {}).get('nom')} {data.get('user', {}).get('prenom')}")
                print(f"      Role: {data.get('user', {}).get('role')}")
                print(f"      Token: {data.get('access', 'N/A')[:30]}...")
            else:
                print(f"      ❌ Connexion échouée! Status: {response.status_code}")
                try:
                    error = response.json()
                    print(f"      Erreur: {error}")
                except:
                    print(f"      Réponse: {response.text[:200]}")
        except Exception as e:
            print(f"      ❌ Erreur: {e}")
    
    print()
    print("=" * 60)
    print("✅ TESTS TERMINÉS")
    print("=" * 60)
    print()
    
    return True

if __name__ == '__main__':
    print()
    success = test_login_direct()
    
    if not success:
        print("⚠️ ACTIONS NÉCESSAIRES:")
        print("   1. Démarrer le serveur Django:")
        print("      cd backend")
        print("      python manage.py runserver")
        print()
        print("   2. Réessayer ce script")
        print()
    else:
        print("💡 POUR TESTER DANS LE NAVIGATEUR:")
        print("   1. Ouvrir: http://127.0.0.1:8080/")
        print("   2. Cliquer sur un compte")
        print("   3. Vérifier la connexion")
        print()
        print("💡 SI LA CONNEXION NE FONCTIONNE PAS:")
        print("   1. Ouvrir la console du navigateur (F12)")
        print("   2. Regarder les erreurs dans l'onglet Console")
        print("   3. Regarder les requêtes dans l'onglet Network")
        print()
