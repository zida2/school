#!/usr/bin/env python
"""
Tester ce que l'API retourne pour l'étudiant Moussa Diallo
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from django.test import RequestFactory
from api.models import Utilisateur
from api.views import SondageViewSet, ObjetPerduViewSet, PublicationViewSet, DemandeAdministrativeViewSet

# Créer une fausse requête
factory = RequestFactory()
user = Utilisateur.objects.get(email='m.diallo@etu.bf')

print("=" * 70)
print(f"TEST API POUR: {user.get_full_name()} ({user.email})")
print("=" * 70)

# Test Sondages
print("\n📊 SONDAGES:")
request = factory.get('/api/sondages/')
request.user = user
view = SondageViewSet.as_view({'get': 'list'})
response = view(request)
print(f"   Status: {response.status_code}")
print(f"   Nombre de sondages: {len(response.data) if response.status_code == 200 else 'Erreur'}")
if response.status_code == 200 and response.data:
    for s in response.data:
        print(f"   - {s['titre']} (statut: {s['statut']})")

# Test Objets Perdus
print("\n🔍 OBJETS PERDUS:")
request = factory.get('/api/objets-perdus/')
request.user = user
view = ObjetPerduViewSet.as_view({'get': 'list'})
response = view(request)
print(f"   Status: {response.status_code}")
print(f"   Nombre d'objets: {len(response.data) if response.status_code == 200 else 'Erreur'}")
if response.status_code == 200 and response.data:
    for o in response.data:
        print(f"   - {o['nom_objet']} ({o['type_declaration']}, statut: {o['statut']})")

# Test Publications
print("\n📰 PUBLICATIONS:")
request = factory.get('/api/publications/')
request.user = user
view = PublicationViewSet.as_view({'get': 'list'})
response = view(request)
print(f"   Status: {response.status_code}")
print(f"   Nombre de publications: {len(response.data) if response.status_code == 200 else 'Erreur'}")
if response.status_code == 200 and response.data:
    for p in response.data:
        print(f"   - {p['titre']} (statut: {p['statut']})")

# Test Demandes
print("\n📨 DEMANDES:")
request = factory.get('/api/demandes-administratives/')
request.user = user
view = DemandeAdministrativeViewSet.as_view({'get': 'list'})
response = view(request)
print(f"   Status: {response.status_code}")
print(f"   Nombre de demandes: {len(response.data) if response.status_code == 200 else 'Erreur'}")
if response.status_code == 200 and response.data:
    for d in response.data:
        print(f"   - {d['objet']} (statut: {d['statut']})")

print("\n" + "=" * 70)
