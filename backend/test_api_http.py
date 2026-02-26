#!/usr/bin/env python
"""
Script pour tester l'API HTTP des enseignants
"""
import requests
import json

API_BASE = 'http://127.0.0.1:8000/api'

print("\n" + "="*60)
print("TEST API HTTP")
print("="*60)

# Test 1: Login admin
print("\n1. Connexion en tant qu'admin...")
login_data = {
    'email': 'admin@uan.bf',
    'password': 'Admin2024!'
}

try:
    response = requests.post(f'{API_BASE}/auth/login/', json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access')
        print(f"   ✅ Connexion réussie")
        print(f"   Token: {token[:50]}...")
        
        # Test 2: Récupérer les enseignants
        print("\n2. Récupération des enseignants...")
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{API_BASE}/enseignants/', headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            # Gérer la pagination DRF
            if isinstance(data, dict) and 'results' in data:
                enseignants = data['results']
            else:
                enseignants = data
                
            print(f"   ✅ {len(enseignants)} enseignant(s) récupéré(s)")
            
            for ens in enseignants:
                print(f"\n   - {ens['prenom']} {ens['nom']}")
                print(f"     Email: {ens['email']}")
                print(f"     Spécialité: {ens.get('specialite', 'N/A')}")
        else:
            print(f"   ❌ Erreur: {response.text}")
    else:
        print(f"   ❌ Erreur de connexion: {response.text}")
        
except Exception as e:
    print(f"   ❌ Exception: {str(e)}")

print("\n" + "="*60 + "\n")
