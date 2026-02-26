#!/usr/bin/env python
"""
Script pour tester la connexion admin via l'API
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
import json

def test_connexion_admin():
    print("=" * 60)
    print("🧪 TEST DE CONNEXION ADMIN VIA L'API")
    print("=" * 60)
    print()
    
    # Test 1: Authentification Django
    print("📋 Test 1: Authentification Django")
    user = authenticate(username='admin@uan.bf', password='admin123')
    if user:
        print(f"   ✅ Authentification réussie: {user.nom} {user.prenom}")
        print(f"   Rôle: {user.role}")
    else:
        print("   ❌ Authentification échouée!")
    print()
    
    # Test 2: API Login
    print("📋 Test 2: API Login (/api/login/)")
    client = Client()
    response = client.post('/api/login/', {
        'email': 'admin@uan.bf',
        'password': 'admin123'
    }, content_type='application/json')
    
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Login réussi!")
        print(f"   Access Token: {data.get('access', 'N/A')[:50]}...")
        print(f"   Refresh Token: {data.get('refresh', 'N/A')[:50]}...")
        print(f"   User: {data.get('user', {}).get('nom')} {data.get('user', {}).get('prenom')}")
        print(f"   Role: {data.get('user', {}).get('role')}")
    else:
        print(f"   ❌ Login échoué!")
        try:
            print(f"   Erreur: {response.json()}")
        except:
            print(f"   Réponse: {response.content}")
    print()
    
    # Test 3: API Me
    if response.status_code == 200:
        print("📋 Test 3: API Me (/api/me/)")
        data = response.json()
        access_token = data.get('access')
        
        response_me = client.get('/api/me/', 
            HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        print(f"   Status Code: {response_me.status_code}")
        if response_me.status_code == 200:
            me_data = response_me.json()
            print(f"   ✅ Récupération profil réussie!")
            print(f"   Nom: {me_data.get('nom')} {me_data.get('prenom')}")
            print(f"   Email: {me_data.get('email')}")
            print(f"   Role: {me_data.get('role')}")
        else:
            print(f"   ❌ Récupération profil échouée!")
            try:
                print(f"   Erreur: {response_me.json()}")
            except:
                print(f"   Réponse: {response_me.content}")
        print()
    
    print("=" * 60)
    print("✅ TESTS TERMINÉS")
    print("=" * 60)
    print()
    
    print("💡 Pour tester dans le navigateur:")
    print("   1. Ouvrir: http://127.0.0.1:8080/")
    print("   2. Cliquer sur le compte Admin")
    print("   3. Vérifier la connexion")
    print()

if __name__ == '__main__':
    print()
    test_connexion_admin()
