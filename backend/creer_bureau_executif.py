"""
Script pour créer un compte Bureau Exécutif de test
"""
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur, Etudiant, MembreBureau, Universite, Filiere, AnneeAcademique

def creer_bureau_executif():
    print("🔧 Création du compte Bureau Exécutif...")
    
    # Vérifier si l'utilisateur existe déjà
    if Utilisateur.objects.filter(email='bureau@uan.bf').exists():
        print("⚠️ L'utilisateur bureau@uan.bf existe déjà")
        user = Utilisateur.objects.get(email='bureau@uan.bf')
    else:
        # Créer l'utilisateur
        user = Utilisateur.objects.create_user(
            email='bureau@uan.bf',
            password='bureau123',
            prenom='Président',
            nom='Bureau Exécutif',
            role='bureau_executif'
        )
        print(f"✅ Utilisateur créé: {user.email}")
    
    # Créer un étudiant associé si nécessaire
    try:
        universite = Universite.objects.first()
        if not universite:
            print("⚠️ Aucune université trouvée, création d'une université de test...")
            universite = Universite.objects.create(
                nom='Université Aube Nouvelle',
                code='UAN',
                licence='PRO',
                statut='active'
            )
        
        filiere = Filiere.objects.first()
        if not filiere:
            print("⚠️ Aucune filière trouvée, création d'une filière de test...")
            filiere = Filiere.objects.create(
                universite=universite,
                nom='Licence Informatique',
                code='L-INFO',
                niveau='Licence'
            )
        
        # Créer une année académique si nécessaire
        annee_academique = AnneeAcademique.objects.filter(active=True).first()
        if not annee_academique:
            print("⚠️ Aucune année académique active, création d'une année de test...")
            annee_academique = AnneeAcademique.objects.create(
                universite=universite,
                libelle='2024-2025',
                debut=date(2024, 9, 1),
                fin=date(2025, 6, 30),
                active=True
            )
        
        # Vérifier si l'étudiant existe
        if not Etudiant.objects.filter(matricule='BUR2024001').exists():
            etudiant = Etudiant.objects.create(
                utilisateur=user,
                matricule='BUR2024001',
                filiere=filiere,
                universite=universite,
                annee_academique=annee_academique,
                niveau='L3',
                genre='M',
                statut='inscrit'
            )
            print(f"✅ Étudiant créé: {etudiant.matricule}")
        else:
            etudiant = Etudiant.objects.get(matricule='BUR2024001')
            print(f"⚠️ Étudiant existe déjà: {etudiant.matricule}")
        
        # Créer le membre du bureau
        if not MembreBureau.objects.filter(utilisateur=user).exists():
            membre = MembreBureau.objects.create(
                utilisateur=user,
                etudiant=etudiant,
                poste='president',
                date_debut_mandat=date(2024, 9, 1),
                actif=True,
                biographie='Président du Bureau Exécutif des Étudiants'
            )
            print(f"✅ Membre du bureau créé: {membre.get_poste_display()}")
        else:
            print("⚠️ Membre du bureau existe déjà")
    
    except Exception as e:
        print(f"⚠️ Erreur lors de la création de l'étudiant/membre: {e}")
    
    print("\n✅ Configuration terminée!")
    print(f"📧 Email: bureau@uan.bf")
    print(f"🔑 Mot de passe: bureau123")
    print(f"🎭 Rôle: Bureau Exécutif")

if __name__ == '__main__':
    creer_bureau_executif()
