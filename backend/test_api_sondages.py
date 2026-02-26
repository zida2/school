#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur, Sondage, ObjetPerdu
from api.serializers import SondageSerializer, ObjetPerduSerializer

# Récupérer l'utilisateur
user = Utilisateur.objects.get(email='m.diallo@etu.bf')

print("=" * 60)
print("TEST API SONDAGES")
print("=" * 60)

# Tester les sondages
sondages = Sondage.objects.filter(statut='actif')
print(f"\n✅ Sondages actifs dans la base: {sondages.count()}")

if sondages.exists():
    serializer = SondageSerializer(sondages, many=True)
    data = serializer.data
    print(f"\n📊 Données sérialisées:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    # Vérifier les champs
    if data:
        print(f"\n🔍 Champs disponibles dans le premier sondage:")
        for key in data[0].keys():
            print(f"   - {key}: {data[0][key]}")

print("\n" + "=" * 60)
print("TEST API OBJETS PERDUS")
print("=" * 60)

# Tester les objets perdus
objets = ObjetPerdu.objects.filter(statut='actif')
print(f"\n✅ Objets perdus actifs dans la base: {objets.count()}")

if objets.exists():
    serializer = ObjetPerduSerializer(objets, many=True)
    data = serializer.data
    print(f"\n🔍 Données sérialisées:")
    print(json.dumps(data[:2], indent=2, ensure_ascii=False))  # Afficher seulement les 2 premiers
    
    # Vérifier les champs
    if data:
        print(f"\n🔍 Champs disponibles dans le premier objet:")
        for key in data[0].keys():
            print(f"   - {key}: {data[0][key]}")
