"""
Script pour créer une classe L1 Informatique avec enseignant, étudiants et notes
Exécuter avec : python creer_classe_l1_info.py
"""
import os
import sys
import django
from datetime import date
from decimal import Decimal
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    django.setup()
    
    from api.models import (
        Utilisateur, Universite, AnneeAcademique, Filiere, 
        Matiere, Enseignant, Etudiant, Note
    )
    
    print("="*70)
    print("🎓 Création de la classe L1 Informatique avec notes")
    print("="*70)
    
    # Récupérer l'université et l'année académique
    try:
        univ = Universite.objects.get(code='UAN')
        annee = AnneeAcademique.objects.get(universite=univ, libelle='2024-2025')
        filiere = Filiere.objects.get(universite=univ, code='INFO-L')
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("⚠️  Exécutez d'abord: python setup.py")
        return
    
    # 1. Créer un enseignant
    print("\n👨‍🏫 Création de l'enseignant...")
    user_prof, created = Utilisateur.objects.get_or_create(
        email='j.ouedraogo@uan.bf',
        defaults={
            'prenom': 'Jean',
            'nom': 'Ouedraogo',
            'role': 'professeur',
        }
    )
    if created:
        user_prof.set_password('enseignant123')
        user_prof.save()
    
    enseignant, created = Enseignant.objects.get_or_create(
        email='j.ouedraogo@uan.bf',
        defaults={
            'universite': univ,
            'prenom': 'Jean',
            'nom': 'Ouedraogo',
            'telephone': '+226 70 12 34 56',
            'specialite': 'Informatique et Systèmes',
            'grade': 'maitre_assistant',
            'statut': 'actif',
        }
    )
    if created:
        print(f"✅ Enseignant créé: {enseignant.get_full_name()}")
    else:
        print(f"ℹ️  Enseignant existant: {enseignant.get_full_name()}")
    
    # 2. Créer les matières du semestre 1
    print("\n📚 Création des matières du semestre 1...")
    matieres_s1 = [
        {'code': 'INFO101', 'nom': 'Algorithmique et Programmation', 'coefficient': 3, 'credits': 6},
        {'code': 'INFO102', 'nom': 'Architecture des Ordinateurs', 'coefficient': 2, 'credits': 4},
        {'code': 'MATH101', 'nom': 'Mathématiques pour Informatique', 'coefficient': 3, 'credits': 5},
        {'code': 'INFO103', 'nom': 'Systèmes d\'Exploitation', 'coefficient': 2, 'credits': 4},
        {'code': 'INFO104', 'nom': 'Bases de Données', 'coefficient': 2, 'credits': 4},
        {'code': 'ANG101', 'nom': 'Anglais Technique', 'coefficient': 1, 'credits': 2},
    ]
    
    matieres_crees = []
    for m in matieres_s1:
        matiere, created = Matiere.objects.get_or_create(
            filiere=filiere,
            code=m['code'],
            defaults={
                'nom': m['nom'],
                'coefficient': m['coefficient'],
                'credits': m['credits'],
                'semestre': 1,
                'enseignant': enseignant,
            }
        )
        matieres_crees.append(matiere)
        if created:
            print(f"  ✅ {matiere.code} - {matiere.nom} (Coef: {matiere.coefficient})")
        else:
            print(f"  ℹ️  {matiere.code} - {matiere.nom} (existant)")
    
    # 3. Créer des étudiants
    print("\n🎓 Création des étudiants...")
    etudiants_data = [
        {'prenom': 'Moussa', 'nom': 'Diallo', 'email': 'm.diallo@etu.bf'},
        {'prenom': 'Fatima', 'nom': 'Sawadogo', 'email': 'f.sawadogo@etu.bf'},
        {'prenom': 'Ibrahim', 'nom': 'Kaboré', 'email': 'i.kabore@etu.bf'},
        {'prenom': 'Aminata', 'nom': 'Traoré', 'email': 'a.traore@etu.bf'},
        {'prenom': 'Abdoul', 'nom': 'Ouédraogo', 'email': 'a.ouedraogo@etu.bf'},
        {'prenom': 'Mariam', 'nom': 'Compaoré', 'email': 'm.compaore@etu.bf'},
        {'prenom': 'Souleymane', 'nom': 'Zongo', 'email': 's.zongo@etu.bf'},
        {'prenom': 'Aïcha', 'nom': 'Sanogo', 'email': 'a.sanogo@etu.bf'},
        {'prenom': 'Boureima', 'nom': 'Yameogo', 'email': 'b.yameogo@etu.bf'},
        {'prenom': 'Salimata', 'nom': 'Ouattara', 'email': 's.ouattara@etu.bf'},
    ]
    
    etudiants_crees = []
    for idx, etud in enumerate(etudiants_data, 1):
        # Créer l'utilisateur
        user_etud, created = Utilisateur.objects.get_or_create(
            email=etud['email'],
            defaults={
                'prenom': etud['prenom'],
                'nom': etud['nom'],
                'role': 'etudiant',
            }
        )
        if created:
            user_etud.set_password('etudiant123')
            user_etud.save()
        
        # Créer l'étudiant
        matricule = f"UAN2024{idx:04d}"
        etudiant, created = Etudiant.objects.get_or_create(
            email=etud['email'],
            defaults={
                'universite': univ,
                'filiere': filiere,
                'annee_academique': annee,
                'matricule': matricule,
                'prenom': etud['prenom'],
                'nom': etud['nom'],
                'telephone': f'+226 70 {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)}',
                'niveau': 'L1',
                'statut': 'inscrit',
                'utilisateur': user_etud,
            }
        )
        etudiants_crees.append(etudiant)
        if created:
            print(f"  ✅ {etudiant.matricule} - {etudiant.get_full_name()}")
        else:
            print(f"  ℹ️  {etudiant.matricule} - {etudiant.get_full_name()} (existant)")
    
    # 4. Créer les notes pour chaque étudiant
    print("\n📝 Génération des notes du semestre 1...")
    notes_creees = 0
    
    for etudiant in etudiants_crees:
        for matiere in matieres_crees:
            # Générer des notes aléatoires mais réalistes
            # Note CC entre 8 et 18
            note_cc = Decimal(str(round(random.uniform(8, 18), 2)))
            # Note Examen entre 7 et 19
            note_examen = Decimal(str(round(random.uniform(7, 19), 2)))
            
            note, created = Note.objects.get_or_create(
                etudiant=etudiant,
                matiere=matiere,
                annee_academique=annee,
                defaults={
                    'note_cc': note_cc,
                    'note_examen': note_examen,
                    'saisie_par': user_prof,
                    'publie': True,
                }
            )
            
            if created:
                notes_creees += 1
    
    print(f"✅ {notes_creees} notes créées")
    
    # 5. Afficher un résumé
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DE LA CLASSE L1 INFORMATIQUE")
    print("="*70)
    print(f"👨‍🏫 Enseignant: {enseignant.get_full_name()}")
    print(f"   Email: j.ouedraogo@uan.bf / Mot de passe: enseignant123")
    print(f"\n🎓 Étudiants: {len(etudiants_crees)}")
    print(f"   Email: [prenom].[nom]@etu.bf / Mot de passe: etudiant123")
    print(f"\n📚 Matières: {len(matieres_crees)} (Semestre 1)")
    for m in matieres_crees:
        print(f"   • {m.code} - {m.nom} (Coef: {m.coefficient})")
    print(f"\n📝 Notes: {notes_creees} notes saisies")
    
    # Calculer et afficher quelques moyennes
    print("\n📈 Exemples de moyennes:")
    for etudiant in etudiants_crees[:3]:
        notes = Note.objects.filter(etudiant=etudiant, annee_academique=annee)
        total_points = 0
        total_coef = 0
        for note in notes:
            if note.moyenne:
                total_points += note.moyenne * float(note.matiere.coefficient)
                total_coef += note.matiere.coefficient
        
        if total_coef > 0:
            moyenne_generale = round(total_points / total_coef, 2)
            print(f"   • {etudiant.get_full_name()}: {moyenne_generale}/20")
    
    print("\n" + "="*70)
    print("✅ Classe L1 Informatique créée avec succès!")
    print("="*70)
    print("\n🚀 Vous pouvez maintenant:")
    print("   1. Vous connecter en tant qu'enseignant pour voir les notes")
    print("   2. Vous connecter en tant qu'étudiant pour voir vos résultats")
    print("   3. Tester le système de réclamation de notes")
    print("="*70)


if __name__ == '__main__':
    main()
