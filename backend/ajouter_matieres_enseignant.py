"""
Script pour ajouter des matières aux enseignants
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    django.setup()
    
    from api.models import Enseignant, Matiere, Filiere, Universite, AnneeAcademique
    
    print("="*60)
    print("📚 Ajout de matières aux enseignants")
    print("="*60)
    
    # Récupérer les données
    univ = Universite.objects.first()
    filiere_info = Filiere.objects.get(code='INFO-L')
    filiere_gestion = Filiere.objects.get(code='GESTION-L')
    
    # Récupérer les enseignants
    ens_ouedraogo = Enseignant.objects.get(email='j.ouedraogo@uan.bf')
    ens_sawadogo = Enseignant.objects.get(email='m.sawadogo@uan.bf')
    
    # Créer des matières pour Jean Ouedraogo (Informatique)
    matieres_info = [
        {
            'code': 'INFO-101',
            'nom': 'Introduction à la Programmation',
            'credits': 6,
            'coefficient': 3,
            'semestre': 1,
            'niveau': 'L1',
            'filiere': filiere_info,
            'enseignant': ens_ouedraogo
        },
        {
            'code': 'INFO-102',
            'nom': 'Algorithmique',
            'credits': 6,
            'coefficient': 3,
            'semestre': 1,
            'niveau': 'L1',
            'filiere': filiere_info,
            'enseignant': ens_ouedraogo
        },
        {
            'code': 'INFO-201',
            'nom': 'Structures de Données',
            'credits': 6,
            'coefficient': 3,
            'semestre': 2,
            'niveau': 'L2',
            'filiere': filiere_info,
            'enseignant': ens_ouedraogo
        },
    ]
    
    # Créer des matières pour Marie Sawadogo (Gestion)
    matieres_gestion = [
        {
            'code': 'GEST-101',
            'nom': 'Introduction à la Gestion',
            'credits': 6,
            'coefficient': 3,
            'semestre': 1,
            'niveau': 'L1',
            'filiere': filiere_gestion,
            'enseignant': ens_sawadogo
        },
        {
            'code': 'GEST-102',
            'nom': 'Comptabilité Générale',
            'credits': 6,
            'coefficient': 3,
            'semestre': 1,
            'niveau': 'L1',
            'filiere': filiere_gestion,
            'enseignant': ens_sawadogo
        },
    ]
    
    # Créer les matières
    for data in matieres_info + matieres_gestion:
        matiere, created = Matiere.objects.get_or_create(
            filiere=data['filiere'],
            code=data['code'],
            defaults=data
        )
        if created:
            print(f"✅ Matière créée : {matiere.code} - {matiere.nom} ({matiere.enseignant.get_full_name()})")
        else:
            print(f"ℹ️  Matière existe : {matiere.code} - {matiere.nom}")
    
    print("\n" + "="*60)
    print("🎉 Matières ajoutées avec succès !")
    print("="*60)
    
    # Afficher le résumé
    print(f"\n📊 RÉSUMÉ :")
    print(f"  Jean Ouedraogo : {ens_ouedraogo.matieres.count()} matière(s)")
    for m in ens_ouedraogo.matieres.all():
        print(f"    - {m.code}: {m.nom}")
    
    print(f"\n  Marie Sawadogo : {ens_sawadogo.matieres.count()} matière(s)")
    for m in ens_sawadogo.matieres.all():
        print(f"    - {m.code}: {m.nom}")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    main()
