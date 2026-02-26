#!/usr/bin/env python
"""
Script pour tester l'API des enseignants
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur, Enseignant
from api.serializers import EnseignantSerializer

print("\n" + "="*60)
print("TEST API ENSEIGNANTS")
print("="*60)

# Test 1: Récupérer tous les enseignants
print("\n1. Récupération de tous les enseignants:")
enseignants = Enseignant.objects.all()
print(f"   Nombre d'enseignants: {enseignants.count()}")

# Test 2: Sérialisation
print("\n2. Sérialisation des enseignants:")
serializer = EnseignantSerializer(enseignants, many=True)
data = serializer.data
print(f"   Données sérialisées: {len(data)} enseignant(s)")

for ens in data:
    print(f"\n   - {ens['prenom']} {ens['nom']}")
    print(f"     Email: {ens['email']}")
    print(f"     Spécialité: {ens.get('specialite', 'N/A')}")
    print(f"     Grade: {ens.get('grade', 'N/A')}")
    print(f"     Statut: {ens['statut']}")

# Test 3: Vérifier les utilisateurs admin
print("\n3. Utilisateurs admin/superadmin:")
admins = Utilisateur.objects.filter(role__in=['admin', 'superadmin'])
for admin in admins:
    print(f"   - {admin.email} ({admin.role})")

print("\n" + "="*60 + "\n")
