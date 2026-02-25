#!/usr/bin/env python
"""
Script pour afficher tous les enseignants de la base de données
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Enseignant

print("\n" + "="*60)
print("LISTE DES ENSEIGNANTS")
print("="*60)

enseignants = Enseignant.objects.all()

if not enseignants.exists():
    print("\n⚠️  Aucun enseignant trouvé dans la base de données")
else:
    print(f"\n✅ {enseignants.count()} enseignant(s) trouvé(s):\n")
    
    for ens in enseignants:
        print(f"ID: {ens.id}")
        print(f"Nom: {ens.prenom} {ens.nom}")
        print(f"Email: {ens.email}")
        print(f"Matricule: {ens.matricule}")
        print(f"Spécialité: {ens.specialite or 'N/A'}")
        print(f"Grade: {ens.grade or 'N/A'}")
        print(f"Statut: {ens.statut}")
        print(f"Université: {ens.universite.nom if ens.universite else 'N/A'}")
        
        # Afficher les matières enseignées
        matieres = ens.matieres.all()
        if matieres.exists():
            print(f"Matières enseignées ({matieres.count()}):")
            for mat in matieres:
                print(f"  - {mat.nom} ({mat.code}) - {mat.filiere.nom}")
        else:
            print("Matières: Aucune")
        
        print("-" * 60)

print("\n")
