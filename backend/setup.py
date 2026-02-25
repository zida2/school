"""
Script de configuration initiale : migrations + superuser + données de base
Exécuter avec : python setup.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    django.setup()

    from django.core.management import call_command

    print("="*60)
    print("🏛️  ERP Universitaire BF – Configuration initiale")
    print("="*60)

    # Migrations
    print("\n📦 Création des tables en base de données...")
    call_command('makemigrations', '--no-input')
    call_command('migrate', '--no-input')
    print("✅ Tables créées avec succès !")

    # Créer les données initiales
    from api.models import Utilisateur, Universite, AnneeAcademique, Filiere

    # Super Admin
    if not Utilisateur.objects.filter(email='superadmin@erp.bf').exists():
        Utilisateur.objects.create_superuser(
            email='superadmin@erp.bf',
            password='SuperAdmin2024!',
            prenom='Super',
            nom='Administrateur',
            role='superadmin',
        )
        print("✅ Super Admin créé : superadmin@erp.bf / SuperAdmin2024!")

    # Université de démonstration
    univ, created = Universite.objects.get_or_create(
        code='UAN',
        defaults={
            'nom': "Université Aube Nouvelle",
            'ville': 'Ouagadougou',
            'adresse': 'Rue 15-873 Ouagadougou, Burkina Faso',
            'telephone': '+226 25 36 20 00',
            'email': 'contact@uan.bf',
            'licence': 'PRO',
            'statut': 'active',
        }
    )
    if created:
        print(f"✅ Université créée : {univ.nom}")

    from datetime import date
    # Année académique
    annee, created = AnneeAcademique.objects.get_or_create(
        universite=univ,
        libelle='2024-2025',
        defaults={
            'debut': date(2024, 9, 1),
            'fin': date(2025, 7, 31),
            'active': True,
        }
    )
    if created:
        print(f"✅ Année académique créée : {annee.libelle}")

    # Admin de l'université
    if not Utilisateur.objects.filter(email='admin@uan.bf').exists():
        admin_user = Utilisateur.objects.create_user(
            email='admin@uan.bf',
            password='Admin2024!',
            prenom='Administrateur',
            nom='UAN',
            role='admin',
        )
        print("✅ Admin UAN créé : admin@uan.bf / Admin2024!")

    # Filières de base
    filieres = [
        {'code': 'INFO-L', 'nom': 'Licence Informatique', 'niveau': 'Licence', 'duree': 3, 'frais_inscription': 350000},
        {'code': 'GESTION-L', 'nom': 'Licence Gestion', 'niveau': 'Licence', 'duree': 3, 'frais_inscription': 300000},
        {'code': 'DROIT-L', 'nom': 'Licence Droit', 'niveau': 'Licence', 'duree': 3, 'frais_inscription': 300000},
    ]
    for f in filieres:
        filiere, created = Filiere.objects.get_or_create(
            universite=univ, code=f['code'],
            defaults={**f, 'universite': univ}
        )
        if created:
            print(f"✅ Filière créée : {filiere.nom}")

    print("\n" + "="*60)
    print("🎉 Configuration terminée avec succès !")
    print("="*60)
    print("\n📋 COMPTES CRÉÉS :")
    print("  Super Admin : superadmin@erp.bf  /  SuperAdmin2024!")
    print("  Admin UAN   : admin@uan.bf        /  Admin2024!")
    print("\n🚀 DÉMARRER LE SERVEUR :")
    print("  python manage.py runserver")
    print("\n🌐 API disponible sur : http://localhost:8000/api/")
    print("🔧 Interface admin   : http://localhost:8000/admin/")
    print("="*60)


if __name__ == '__main__':
    main()
