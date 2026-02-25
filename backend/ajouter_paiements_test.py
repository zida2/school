#!/usr/bin/env python
"""
Script pour ajouter des paiements de test
"""
import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Etudiant, Paiement, AnneeAcademique, Utilisateur
from decimal import Decimal

print("=" * 60)
print("AJOUT DE PAIEMENTS DE TEST")
print("=" * 60)

# Récupérer l'année académique active
annee = AnneeAcademique.objects.filter(active=True).first()
if not annee:
    annee = AnneeAcademique.objects.first()

if not annee:
    print("❌ Aucune année académique trouvée")
    exit(1)

# Récupérer un utilisateur admin pour enregistrer les paiements
admin = Utilisateur.objects.filter(role__in=['admin', 'superadmin']).first()
if not admin:
    print("❌ Aucun administrateur trouvé")
    exit(1)

# Récupérer tous les étudiants
etudiants = list(Etudiant.objects.all())
print(f"\n✅ {len(etudiants)} étudiant(s) trouvé(s)")

# Modes de paiement
modes = ['especes', 'orange_money', 'moov_money', 'virement', 'cheque']
types = ['inscription', 'acompte', 'solde']

# Créer des paiements pour quelques étudiants
nb_paiements = min(8, len(etudiants))
etudiants_selectionnes = random.sample(etudiants, nb_paiements)

paiements_crees = 0

for i, etudiant in enumerate(etudiants_selectionnes, 1):
    # Montants variés
    montants = [50000, 75000, 100000, 150000]
    montant = random.choice(montants)
    
    # Date de paiement dans les 30 derniers jours
    jours_avant = random.randint(0, 30)
    date_paiement = date.today() - timedelta(days=jours_avant)
    
    # Créer le paiement
    numero_recu = f"REC-2024-{str(i).zfill(6)}"
    
    paiement = Paiement.objects.create(
        etudiant=etudiant,
        annee_academique=annee,
        numero_recu=numero_recu,
        montant=Decimal(montant),
        mode=random.choice(modes),
        type_paiement=random.choice(types),
        statut='valide',
        date_paiement=date_paiement,
        enregistre_par=admin,
        observations=f"Paiement test pour {etudiant.prenom} {etudiant.nom}"
    )
    
    # Mettre à jour le solde dû de l'étudiant
    montant_paye_total = etudiant.paiements.filter(statut='valide').aggregate(
        total=django.db.models.Sum('montant')
    )['total'] or 0
    
    frais = etudiant.filiere.frais_inscription
    etudiant.solde_du = max(0, int(frais) - int(montant_paye_total))
    etudiant.save()
    
    print(f"\n✅ Paiement créé:")
    print(f"   Reçu: {numero_recu}")
    print(f"   Étudiant: {etudiant.prenom} {etudiant.nom}")
    print(f"   Montant: {montant:,} FCFA")
    print(f"   Mode: {paiement.mode}")
    print(f"   Date: {date_paiement}")
    print(f"   Nouveau solde dû: {etudiant.solde_du:,} FCFA")
    
    paiements_crees += 1

print("\n" + "=" * 60)
print(f"✅ {paiements_crees} paiement(s) créé(s) avec succès")
print("=" * 60)

# Afficher les statistiques
total_encaisse = Paiement.objects.filter(statut='valide').aggregate(
    total=django.db.models.Sum('montant')
)['total'] or 0

total_impayes = Etudiant.objects.aggregate(
    total=django.db.models.Sum('solde_du')
)['total'] or 0

print(f"\nSTATISTIQUES:")
print(f"- Total encaissé: {total_encaisse:,} FCFA")
print(f"- Total impayés: {total_impayes:,} FCFA")
