#!/usr/bin/env python
"""
Script de nettoyage de la base de données
Conserve 3 filières avec leurs matières
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import *

print("\n" + "="*60)
print("🗑️  NETTOYAGE BASE DE DONNÉES + 3 FILIÈRES")
print("="*60 + "\n")

admin_email = 'admin@unierp.bf'

# 1. Supprimer tous les utilisateurs sauf l'admin
print("📋 Suppression des utilisateurs...")
users_to_delete = Utilisateur.objects.exclude(email=admin_email)
count_users = users_to_delete.count()
users_to_delete.delete()
print(f"   ✅ {count_users} utilisateurs supprimés\n")

# 2. Supprimer toutes les données SAUF Université, Filières et Matières
print("📋 Suppression des données...")

models_to_clean = [
    ('Étudiants', Etudiant),
    ('Enseignants', Enseignant),
    ('Notes', Note),
    ('Présences', Presence),
    ('Paiements', Paiement),
    ('Notifications', Notification),
    ('Messages', Message),
    ('Publications', Publication),
    ('Sondages', Sondage),
    ('Événements', Evenement),
    ('Inscriptions', Inscription),
    ('Classes', Classe),
    ('Promotions', Promotion),
    ('Demandes Inscription Étudiants', DemandeInscription),
    ('Demandes Inscription Professeurs', DemandeInscriptionProfesseur),
    ('Demandes Communication', DemandeInscriptionCommunication),
    ('Demandes Académique', DemandeInscriptionAcademique),
    ('Demandes Comptabilité', DemandeInscriptionComptabilite),
]

for name, model in models_to_clean:
    try:
        count = model.objects.all().count()
        if count > 0:
            model.objects.all().delete()
            print(f"   ✅ {count} {name} supprimé(s)")
        else:
            print(f"   ⚪ 0 {name}")
    except Exception as e:
        print(f"   ⚠️  Erreur {name}: {str(e)}")

# 3. Garder seulement 3 filières avec leurs matières
print("\n📋 Conservation de 3 filières...")

total_filieres = Filiere.objects.count()

if total_filieres > 3:
    # Garder les 3 premières filières
    filieres_a_garder = list(Filiere.objects.all()[:3].values_list('id', flat=True))
    
    # Supprimer les matières des autres filières
    Matiere.objects.exclude(filiere_id__in=filieres_a_garder).delete()
    
    # Supprimer les autres filières
    filieres_supprimees = Filiere.objects.exclude(id__in=filieres_a_garder).count()
    Filiere.objects.exclude(id__in=filieres_a_garder).delete()
    
    print(f"   ✅ {filieres_supprimees} filières supprimées")
    print(f"   ✅ 3 filières conservées")
else:
    print(f"   ✅ {total_filieres} filières conservées")

# Afficher les filières conservées
print("\n📚 Filières conservées:")
for filiere in Filiere.objects.all():
    nb_matieres = filiere.matieres.count()
    print(f"   • {filiere.code} - {filiere.nom} ({nb_matieres} matières)")

print("\n" + "="*60)
print("✅ BASE DE DONNÉES NETTOYÉE!")
print("="*60)

# 4. Vérification finale
print("\n📊 VÉRIFICATION:")
admin = Utilisateur.objects.get(email=admin_email)
print(f"   Email: {admin.email}")
print(f"   Rôle: {admin.role}")

total_users = Utilisateur.objects.count()
total_filieres = Filiere.objects.count()
total_matieres = Matiere.objects.count()
total_universites = Universite.objects.count()

print(f"\n   Total utilisateurs: {total_users}")
print(f"   Total universités: {total_universites}")
print(f"   Total filières: {total_filieres}")
print(f"   Total matières: {total_matieres}")

print("\n" + "="*60)
print("✅ TERMINÉ!")
print("="*60 + "\n")
