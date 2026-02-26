#!/usr/bin/env python
"""
Script de test pour vérifier les paiements et les étudiants de l'enseignant
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Enseignant, Etudiant, Matiere, Paiement

print("=" * 60)
print("TEST DES PAIEMENTS ET ÉTUDIANTS")
print("=" * 60)

# Test 1: Vérifier les paiements
print("\n1. PAIEMENTS ENREGISTRÉS:")
print("-" * 60)
paiements = Paiement.objects.all()
print(f"✅ {paiements.count()} paiement(s) trouvé(s)\n")

for p in paiements[:5]:  # Afficher les 5 premiers
    print(f"Reçu: {p.numero_recu}")
    print(f"Étudiant: {p.etudiant.prenom} {p.etudiant.nom} ({p.etudiant.matricule})")
    print(f"Montant: {p.montant} FCFA")
    print(f"Mode: {p.mode}")
    print(f"Date: {p.date_paiement}")
    print(f"Statut: {p.statut}")
    print("-" * 60)

# Test 2: Vérifier les étudiants de J. Ouedraogo
print("\n2. ÉTUDIANTS DE J. OUEDRAOGO:")
print("-" * 60)
try:
    enseignant = Enseignant.objects.get(email='j.ouedraogo@uan.bf')
    print(f"Enseignant: {enseignant.prenom} {enseignant.nom}")
    print(f"Matières enseignées: {enseignant.matieres.count()}")
    
    # Récupérer toutes les filières de ses matières
    filieres = set(enseignant.matieres.values_list('filiere', flat=True))
    print(f"Filières concernées: {len(filieres)}")
    
    # Récupérer tous les étudiants de ces filières
    etudiants = Etudiant.objects.filter(filiere__in=filieres).distinct()
    print(f"\n✅ {etudiants.count()} étudiant(s) dans ses filières\n")
    
    for e in etudiants[:10]:  # Afficher les 10 premiers
        print(f"- {e.matricule}: {e.prenom} {e.nom} ({e.filiere.nom} - {e.niveau})")
    
    if etudiants.count() > 10:
        print(f"... et {etudiants.count() - 10} autre(s)")
        
except Enseignant.DoesNotExist:
    print("❌ Enseignant J. Ouedraogo non trouvé")

# Test 3: Statistiques globales
print("\n3. STATISTIQUES GLOBALES:")
print("-" * 60)
total_etudiants = Etudiant.objects.count()
total_paiements = Paiement.objects.filter(statut='valide').count()
montant_total = sum(p.montant for p in Paiement.objects.filter(statut='valide'))
total_impayes = sum(e.solde_du for e in Etudiant.objects.all())

print(f"Total étudiants: {total_etudiants}")
print(f"Total paiements validés: {total_paiements}")
print(f"Montant total encaissé: {montant_total:,.0f} FCFA")
print(f"Total impayés: {total_impayes:,.0f} FCFA")

print("\n" + "=" * 60)
print("TEST TERMINÉ")
print("=" * 60)
