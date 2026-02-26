#!/usr/bin/env python
"""
Script pour tester l'ajout d'un enseignant via l'API
"""
import requests
import json

API_BASE = 'http://127.0.0.1:8000/api'

print("\n" + "="*60)
print("TEST AJOUT ENSEIGNANT")
print("="*60)

# 1. Connexion admin
print("\n1. Connexion admin...")
response = requests.post(f'{API_BASE}/auth/login/', 
                        json={'email': 'admin@uan.bf', 'password': 'Admin2024!'})

if response.status_code != 200:
    print(f"❌ Erreur de connexion: {response.text}")
    exit(1)

token = response.json().get('access')
print("✅ Connexion réussie")

# 2. Récupérer les enseignants avant
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(f'{API_BASE}/enseignants/', headers=headers)
data = response.json()
if isinstance(data, dict) and 'results' in data:
    enseignants_avant = data['results']
else:
    enseignants_avant = data
print(f"\n2. Enseignants avant: {len(enseignants_avant)}")

# 3. Ajouter un nouvel enseignant
print("\n3. Ajout d'un nouvel enseignant...")
nouvel_enseignant = {
    'prenom': 'Test',
    'nom': 'Enseignant',
    'email': 'test.enseignant@uan.bf',
    'telephone': '+226 70 00 00 00',
    'specialite': 'Mathématiques',
    'grade': 'maitre_assistant',
    'statut': 'actif',
    'universite': 1
}

print(f"Données envoyées: {json.dumps(nouvel_enseignant, indent=2)}")

response = requests.post(f'{API_BASE}/enseignants/', 
                        headers=headers,
                        json=nouvel_enseignant)

print(f"Status code: {response.status_code}")
print(f"Réponse: {response.text[:500]}")

if response.status_code in [200, 201]:
    print("✅ Enseignant ajouté avec succès")
    enseignant_cree = response.json()
    print(f"ID: {enseignant_cree.get('id')}")
    print(f"Matricule: {enseignant_cree.get('matricule')}")
else:
    print(f"❌ Erreur: {response.status_code}")
    try:
        erreur = response.json()
        print(f"Détails: {json.dumps(erreur, indent=2)}")
    except:
        print(f"Réponse brute: {response.text}")

# 4. Vérifier la liste après
print("\n4. Vérification...")
response = requests.get(f'{API_BASE}/enseignants/', headers=headers)
data = response.json()
if isinstance(data, dict) and 'results' in data:
    enseignants_apres = data['results']
else:
    enseignants_apres = data
print(f"Enseignants après: {len(enseignants_apres)}")

if len(enseignants_apres) > len(enseignants_avant):
    print("✅ L'enseignant a bien été ajouté à la base de données")
else:
    print("❌ L'enseignant n'a pas été ajouté")

print("\n" + "="*60 + "\n")
