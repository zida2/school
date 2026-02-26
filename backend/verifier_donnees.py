#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Etudiant, DemandeAdministrative, Publication, Sondage, ObjetPerdu

# Vérifier l'étudiant Moussa Diallo
etudiant = Etudiant.objects.filter(utilisateur__email='m.diallo@etu.bf').first()

if etudiant:
    print(f"✅ Étudiant trouvé: {etudiant.get_full_name()}")
    print(f"   Email: {etudiant.utilisateur.email}")
    print(f"   ID: {etudiant.id}")
    
    # Vérifier ses demandes
    demandes = DemandeAdministrative.objects.filter(etudiant=etudiant)
    print(f"\n📨 Demandes de cet étudiant: {demandes.count()}")
    for d in demandes:
        print(f"   - {d.objet} ({d.statut})")
    
    # Vérifier les objets perdus
    objets = ObjetPerdu.objects.filter(declarant=etudiant.utilisateur)
    print(f"\n🔍 Objets perdus déclarés: {objets.count()}")
    for o in objets:
        print(f"   - {o.nom_objet} ({o.type_declaration})")
else:
    print("❌ Étudiant m.diallo@etu.bf non trouvé")

# Vérifier les publications (visibles par tous)
publications = Publication.objects.filter(statut='publie')
print(f"\n📰 Publications publiées: {publications.count()}")
for p in publications:
    print(f"   - {p.titre}")

# Vérifier les sondages actifs (visibles par tous)
sondages = Sondage.objects.filter(statut='actif')
print(f"\n📊 Sondages actifs: {sondages.count()}")
for s in sondages:
    print(f"   - {s.titre}")
