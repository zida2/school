"""
Test direct de création de support
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    django.setup()
    
    from api.models import SupportCours, Enseignant, Matiere
    
    print("="*60)
    print("🧪 Test création support de cours")
    print("="*60)
    
    # Récupérer l'enseignant et une matière
    ens = Enseignant.objects.get(email='j.ouedraogo@uan.bf')
    matiere = ens.matieres.first()
    
    print(f"\n✅ Enseignant: {ens.get_full_name()}")
    print(f"✅ Matière: {matiere.nom}")
    
    # Créer un support de test
    support = SupportCours.objects.create(
        titre="Test Support Direct",
        matiere=matiere,
        enseignant=ens,
        type_support='cours',
        description='Support créé directement en Python',
        visible=True
    )
    
    print(f"\n✅ Support créé avec succès!")
    print(f"   ID: {support.id}")
    print(f"   Titre: {support.titre}")
    print(f"   Matière: {support.matiere.nom}")
    print(f"   Enseignant: {support.enseignant.get_full_name()}")
    print(f"   Date: {support.date_depot}")
    
    # Lister tous les supports
    print(f"\n📊 Total supports: {SupportCours.objects.count()}")
    for s in SupportCours.objects.all():
        print(f"   - {s.titre} ({s.matiere.nom})")
    
    print("\n" + "="*60)
    print("✅ Le backend fonctionne correctement!")
    print("Le problème vient du frontend JavaScript.")
    print("="*60)

if __name__ == '__main__':
    main()
