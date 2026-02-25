"""
Script pour ajouter des données de test
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    django.setup()
    
    from api.models import Utilisateur, Universite, AnneeAcademique, Filiere, Etudiant, Enseignant
    from datetime import date
    
    print("="*60)
    print("📊 Ajout de données de test")
    print("="*60)
    
    # Récupérer les données existantes
    univ = Universite.objects.first()
    annee = AnneeAcademique.objects.first()
    filiere_info = Filiere.objects.get(code='INFO-L')
    filiere_gestion = Filiere.objects.get(code='GESTION-L')
    filiere_droit = Filiere.objects.get(code='DROIT-L')
    
    # Créer des enseignants
    enseignants_data = [
        {
            'matricule': 'ENS-2024-001',
            'prenom': 'Jean',
            'nom': 'Ouedraogo',
            'email': 'j.ouedraogo@uan.bf',
            'telephone': '70123456',
            'specialite': 'Informatique',
            'grade': 'maitre_conferences',
        },
        {
            'matricule': 'ENS-2024-002',
            'prenom': 'Marie',
            'nom': 'Sawadogo',
            'email': 'm.sawadogo@uan.bf',
            'telephone': '76234567',
            'specialite': 'Gestion',
            'grade': 'professeur_titulaire',
        },
    ]
    
    for data in enseignants_data:
        if not Enseignant.objects.filter(email=data['email']).exists():
            # Créer le compte utilisateur
            user = Utilisateur.objects.create_user(
                email=data['email'],
                password='enseignant123',
                prenom=data['prenom'],
                nom=data['nom'],
                role='professeur',
            )
            # Créer l'enseignant
            enseignant = Enseignant.objects.create(
                utilisateur=user,
                universite=univ,
                **data
            )
            print(f"✅ Enseignant créé : {enseignant.prenom} {enseignant.nom}")
    
    # Créer des étudiants
    etudiants_data = [
        {
            'matricule': 'ETU-2024-001',
            'prenom': 'Moussa',
            'nom': 'Diallo',
            'email': 'm.diallo@etu.bf',
            'telephone': '70111111',
            'filiere': filiere_info,
            'niveau': 'L1',
            'date_naissance': date(2003, 5, 15),
        },
        {
            'matricule': 'ETU-2024-002',
            'prenom': 'Fatou',
            'nom': 'Traoré',
            'email': 'f.traore@etu.bf',
            'telephone': '76222222',
            'filiere': filiere_info,
            'niveau': 'L2',
            'date_naissance': date(2002, 8, 20),
        },
        {
            'matricule': 'ETU-2024-003',
            'prenom': 'Ibrahim',
            'nom': 'Kaboré',
            'email': 'i.kabore@etu.bf',
            'telephone': '78333333',
            'filiere': filiere_gestion,
            'niveau': 'L1',
            'date_naissance': date(2003, 12, 10),
        },
        {
            'matricule': 'ETU-2024-004',
            'prenom': 'Aminata',
            'nom': 'Compaoré',
            'email': 'a.compaore@etu.bf',
            'telephone': '70444444',
            'filiere': filiere_gestion,
            'niveau': 'L3',
            'date_naissance': date(2001, 3, 25),
        },
        {
            'matricule': 'ETU-2024-005',
            'prenom': 'Abdoul',
            'nom': 'Zongo',
            'email': 'a.zongo@etu.bf',
            'telephone': '76555555',
            'filiere': filiere_droit,
            'niveau': 'L1',
            'date_naissance': date(2003, 7, 8),
        },
        {
            'matricule': 'ETU-2024-006',
            'prenom': 'Mariam',
            'nom': 'Ouattara',
            'email': 'm.ouattara@etu.bf',
            'telephone': '78666666',
            'filiere': filiere_droit,
            'niveau': 'L2',
            'date_naissance': date(2002, 11, 30),
        },
    ]
    
    for data in etudiants_data:
        if not Etudiant.objects.filter(email=data['email']).exists():
            # Créer le compte utilisateur
            user = Utilisateur.objects.create_user(
                email=data['email'],
                password='etudiant123',
                prenom=data['prenom'],
                nom=data['nom'],
                role='etudiant',
            )
            # Créer l'étudiant
            filiere = data.pop('filiere')
            etudiant = Etudiant.objects.create(
                utilisateur=user,
                universite=univ,
                annee_academique=annee,
                filiere=filiere,
                solde_du=filiere.frais_inscription,
                statut='inscrit',
                **data
            )
            print(f"✅ Étudiant créé : {etudiant.matricule} - {etudiant.prenom} {etudiant.nom}")
    
    print("\n" + "="*60)
    print("🎉 Données de test ajoutées avec succès !")
    print("="*60)
    print(f"\n📊 STATISTIQUES :")
    print(f"  Utilisateurs : {Utilisateur.objects.count()}")
    print(f"  Enseignants  : {Enseignant.objects.count()}")
    print(f"  Étudiants    : {Etudiant.objects.count()}")
    print(f"  Filières     : {Filiere.objects.count()}")
    print("\n🔑 COMPTES DE TEST :")
    print("  Enseignant : j.ouedraogo@uan.bf / enseignant123")
    print("  Étudiant   : m.diallo@etu.bf / etudiant123")
    print("="*60)

if __name__ == '__main__':
    main()
