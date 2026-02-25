import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur, Universite, Filiere, Enseignant, Etudiant, AnneeAcademique
from django.utils import timezone

def seed():
    # 1. Get or Create Universite
    univ, _ = Universite.objects.get_or_create(
        code='UAUBE',
        defaults={'nom': 'Université de l\'Aube', 'ville': 'Ouagadougou', 'statut': 'active'}
    )
    
    # 2. Get or Create Annee
    annee, _ = AnneeAcademique.objects.get_or_create(
        universite=univ,
        libelle='2024-2025',
        defaults={'debut': '2024-10-01', 'fin': '2025-07-31', 'active': True}
    )

    # 3. Superadmin
    sa, created = Utilisateur.objects.get_or_create(
        email='superadmin@erp.bf',
        defaults={'prenom': 'Super', 'nom': 'Admin', 'role': 'superadmin'}
    )
    sa.set_password('SuperAdmin2024!')
    sa.save()
    print(f"Superadmin checked: {sa.email}")

    # 4. Admin
    adm_user, created = Utilisateur.objects.get_or_create(
        email='admin@u-aube.bf',
        defaults={'prenom': 'Admin', 'nom': 'UAUBE', 'role': 'admin'}
    )
    adm_user.set_password('admin123')
    adm_user.save()
    print(f"Admin checked: {adm_user.email}")

    # 5. Professeur
    prof_user, created = Utilisateur.objects.get_or_create(
        email='traore@prof.bf',
        defaults={'prenom': 'Moussa', 'nom': 'Traoré', 'role': 'professeur'}
    )
    prof_user.set_password('enseignant123')
    prof_user.save()
    
    prof, _ = Enseignant.objects.get_or_create(
        utilisateur=prof_user,
        defaults={
            'nom': 'Traoré', 'prenom': 'Moussa', 'email': 'traore@prof.bf',
            'matricule': 'PR-001', 'universite': univ, 'grade': 'Maître-Assistant'
        }
    )
    print(f"Prof checked: {prof_user.email}")

    # 6. Etudiant
    fil, _ = Filiere.objects.get_or_create(
        universite=univ,
        code='L1-INFO',
        defaults={'nom': 'Licence Informatique', 'niveau': 'Licence', 'duree': 3, 'frais_inscription': 450000}
    )

    etu_user, created = Utilisateur.objects.get_or_create(
        email='m.diallo@etu.bf',
        defaults={'prenom': 'Moussa', 'nom': 'Diallo', 'role': 'etudiant'}
    )
    etu_user.set_password('etudiant123')
    etu_user.save()

    etu, _ = Etudiant.objects.get_or_create(
        utilisateur=etu_user,
        defaults={
            'nom': 'Diallo', 'prenom': 'Moussa', 'email': 'm.diallo@etu.bf',
            'matricule': 'ETU-2024-001', 'universite': univ, 'filiere': fil,
            'annee_academique': annee, 'solde_du': 450000
        }
    )
    print(f"Etudiant checked: {etu_user.email}")

if __name__ == '__main__':
    seed()
