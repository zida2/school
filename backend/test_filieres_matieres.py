#!/usr/bin/env python3
"""
Script de test pour les fonctionnalités CRUD des filières et matières
"""
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Filiere, Matiere, Enseignant, Universite

def test_filieres_matieres():
    print("=" * 60)
    print("TEST DES FILIÈRES ET MATIÈRES")
    print("=" * 60)
    
    # Récupérer l'université
    universite = Universite.objects.first()
    if not universite:
        print("❌ Aucune université trouvée")
        return
    
    print(f"\n✅ Université: {universite.nom}")
    
    # 1. FILIÈRES
    print("\n" + "=" * 60)
    print("1. FILIÈRES")
    print("=" * 60)
    
    filieres = Filiere.objects.all()
    print(f"\n📊 Total filières: {filieres.count()}")
    
    for filiere in filieres:
        nb_etudiants = filiere.etudiants.count()
        nb_matieres = filiere.matieres.count()
        print(f"\n📚 {filiere.code} - {filiere.nom}")
        print(f"   Niveau: {filiere.niveau}")
        print(f"   Frais: {filiere.frais_inscription:,} FCFA")
        print(f"   Étudiants: {nb_etudiants}")
        print(f"   Matières: {nb_matieres}")
    
    # 2. MATIÈRES
    print("\n" + "=" * 60)
    print("2. MATIÈRES")
    print("=" * 60)
    
    matieres = Matiere.objects.all()
    print(f"\n📊 Total matières: {matieres.count()}")
    
    # Grouper par filière
    for filiere in filieres:
        matieres_filiere = filiere.matieres.all()
        if matieres_filiere.exists():
            print(f"\n📚 {filiere.nom}")
            for matiere in matieres_filiere:
                enseignant = f"{matiere.enseignant.prenom} {matiere.enseignant.nom}" if matiere.enseignant else "Non assigné"
                print(f"   • {matiere.code} - {matiere.nom}")
                print(f"     Semestre: {matiere.semestre} | Coef: {matiere.coefficient} | Prof: {enseignant}")
    
    # 3. ENSEIGNANTS ET LEURS MATIÈRES
    print("\n" + "=" * 60)
    print("3. ENSEIGNANTS ET LEURS MATIÈRES")
    print("=" * 60)
    
    enseignants = Enseignant.objects.all()
    print(f"\n📊 Total enseignants: {enseignants.count()}")
    
    for enseignant in enseignants:
        matieres_enseignant = enseignant.matieres.all()
        print(f"\n👨‍🏫 {enseignant.prenom} {enseignant.nom}")
        print(f"   Email: {enseignant.email}")
        print(f"   Matières enseignées: {matieres_enseignant.count()}")
        
        if matieres_enseignant.exists():
            for matiere in matieres_enseignant:
                print(f"   • {matiere.code} - {matiere.nom} ({matiere.filiere.nom})")
    
    # 4. STATISTIQUES GLOBALES
    print("\n" + "=" * 60)
    print("4. STATISTIQUES GLOBALES")
    print("=" * 60)
    
    total_filieres = Filiere.objects.count()
    total_matieres = Matiere.objects.count()
    total_enseignants = Enseignant.objects.count()
    matieres_assignees = Matiere.objects.filter(enseignant__isnull=False).count()
    matieres_non_assignees = Matiere.objects.filter(enseignant__isnull=True).count()
    
    print(f"\n📊 Filières: {total_filieres}")
    print(f"📊 Matières: {total_matieres}")
    print(f"   • Assignées: {matieres_assignees}")
    print(f"   • Non assignées: {matieres_non_assignees}")
    print(f"📊 Enseignants: {total_enseignants}")
    
    # 5. VÉRIFICATIONS
    print("\n" + "=" * 60)
    print("5. VÉRIFICATIONS")
    print("=" * 60)
    
    # Vérifier les matières sans filière
    matieres_sans_filiere = Matiere.objects.filter(filiere__isnull=True)
    if matieres_sans_filiere.exists():
        print(f"\n⚠️  {matieres_sans_filiere.count()} matière(s) sans filière:")
        for matiere in matieres_sans_filiere:
            print(f"   • {matiere.code} - {matiere.nom}")
    else:
        print("\n✅ Toutes les matières ont une filière")
    
    # Vérifier les filières sans matières
    filieres_sans_matieres = [f for f in filieres if f.matieres.count() == 0]
    if filieres_sans_matieres:
        print(f"\n⚠️  {len(filieres_sans_matieres)} filière(s) sans matières:")
        for filiere in filieres_sans_matieres:
            print(f"   • {filiere.code} - {filiere.nom}")
    else:
        print("✅ Toutes les filières ont des matières")
    
    print("\n" + "=" * 60)
    print("✅ TEST TERMINÉ")
    print("=" * 60)

if __name__ == '__main__':
    test_filieres_matieres()
