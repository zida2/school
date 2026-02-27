#!/usr/bin/env python
"""
Script de réorganisation complète de la structure hiérarchique
Crée les relations correctes entre Admin -> Prof -> Étudiant
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import (
    Utilisateur, Etudiant, Enseignant, Filiere, Matiere
)
from django.contrib.auth.hashers import make_password

def reorganiser_structure():
    print("🔄 RÉORGANISATION DE LA STRUCTURE HIÉRARCHIQUE")
    print("=" * 60)
    
    # 1. CRÉER/METTRE À JOUR LA FILIÈRE INFORMATIQUE
    print("\n📚 1. Configuration de la filière Informatique...")
    filiere_info, created = Filiere.objects.get_or_create(
        code='L1-INFO',
        defaults={
            'nom': 'Licence 1 Informatique',
            'niveau': 'L1',
            'description': 'Formation en informatique fondamentale'
        }
    )
    if created:
        print(f"   ✅ Filière créée: {filiere_info.nom}")
    else:
        print(f"   ℹ️  Filière existante: {filiere_info.nom}")
    
    # 2. CRÉER/METTRE À JOUR LA CLASSE L1 INFO
    print("\n🏫 2. Configuration de la classe L1 INFO...")
    classe_l1, created = Classe.objects.get_or_create(
        code='L1-INFO-A',
        defaults={
            'nom': 'L1 Informatique - Groupe A',
            'filiere': filiere_info,
            'niveau': 'L1',
            'annee_academique': '2025-2026'
        }
    )
    if created:
        print(f"   ✅ Classe créée: {classe_l1.nom}")
    else:
        classe_l1.filiere = filiere_info
        classe_l1.save()
        print(f"   ℹ️  Classe existante: {classe_l1.nom}")
    
    # 3. CRÉER/METTRE À JOUR LA MATIÈRE INFORMATIQUE
    print("\n📖 3. Configuration de la matière Informatique...")
    matiere_info, created = Matiere.objects.get_or_create(
        code='INFO-101',
        defaults={
            'nom': 'Introduction à l\'Informatique',
            'description': 'Cours d\'introduction aux concepts de base de l\'informatique',
            'credits': 6,
            'coefficient': 3
        }
    )
    if created:
        print(f"   ✅ Matière créée: {matiere_info.nom}")
    else:
        print(f"   ℹ️  Matière existante: {matiere_info.nom}")
    
    # 4. CONFIGURER L'ADMINISTRATEUR
    print("\n👔 4. Configuration de l'Administrateur...")
    try:
        admin = Utilisateur.objects.get(email='admin@uan.bf')
        admin.role = 'admin'
        admin.nom = 'ADMIN'
        admin.prenom = 'Système'
        admin.save()
        print(f"   ✅ Admin configuré: {admin.get_full_name()}")
    except Utilisateur.DoesNotExist:
        admin = Utilisateur.objects.create(
            email='admin@uan.bf',
            password=make_password('admin123'),
            role='admin',
            nom='ADMIN',
            prenom='Système',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        print(f"   ✅ Admin créé: {admin.get_full_name()}")
    
    # 5. CONFIGURER LE PROFESSEUR OUEDRAOGO
    print("\n👨‍🏫 5. Configuration du Prof Ouedraogo...")
    try:
        user_prof = Utilisateur.objects.get(email='j.ouedraogo@uan.bf')
        user_prof.role = 'enseignant'
        user_prof.nom = 'OUEDRAOGO'
        user_prof.prenom = 'Jean'
        user_prof.save()
    except Utilisateur.DoesNotExist:
        user_prof = Utilisateur.objects.create(
            email='j.ouedraogo@uan.bf',
            password=make_password('enseignant123'),
            role='enseignant',
            nom='OUEDRAOGO',
            prenom='Jean',
            is_active=True
        )
    
    # Créer/mettre à jour le profil enseignant
    enseignant, created = Enseignant.objects.get_or_create(
        utilisateur=user_prof,
        defaults={
            'specialite': 'Informatique',
            'grade': 'Maître Assistant',
            'departement': 'Informatique et Mathématiques'
        }
    )
    if not created:
        enseignant.specialite = 'Informatique'
        enseignant.grade = 'Maître Assistant'
        enseignant.departement = 'Informatique et Mathématiques'
        enseignant.save()
    
    print(f"   ✅ Enseignant configuré: {user_prof.get_full_name()}")
    print(f"      Spécialité: {enseignant.specialite}")
    
    # Assigner la matière au professeur
    enseignement, created = EnseignementMatiere.objects.get_or_create(
        enseignant=enseignant,
        matiere=matiere_info,
        classe=classe_l1,
        defaults={
            'annee_academique': '2025-2026',
            'semestre': 1
        }
    )
    if created:
        print(f"   ✅ Matière assignée: {matiere_info.nom} -> {user_prof.get_full_name()}")
    else:
        print(f"   ℹ️  Matière déjà assignée: {matiere_info.nom}")
    
    # 6. CONFIGURER L'ÉTUDIANT MOUSSA DIALLO
    print("\n👨‍🎓 6. Configuration de l'étudiant Moussa Diallo...")
    try:
        user_etudiant = Utilisateur.objects.get(email='m.diallo@etu.bf')
        user_etudiant.role = 'etudiant'
        user_etudiant.nom = 'DIALLO'
        user_etudiant.prenom = 'Moussa'
        user_etudiant.save()
    except Utilisateur.DoesNotExist:
        user_etudiant = Utilisateur.objects.create(
            email='m.diallo@etu.bf',
            password=make_password('etudiant123'),
            role='etudiant',
            nom='DIALLO',
            prenom='Moussa',
            is_active=True
        )
    
    # Créer/mettre à jour le profil étudiant
    etudiant, created = Etudiant.objects.get_or_create(
        utilisateur=user_etudiant,
        defaults={
            'matricule': 'ETU2025001',
            'date_naissance': '2005-03-15',
            'lieu_naissance': 'Ouagadougou',
            'nationalite': 'Burkinabè',
            'adresse': 'Ouaga 2000',
            'telephone': '+226 70 12 34 56'
        }
    )
    if not created:
        etudiant.matricule = 'ETU2025001'
        etudiant.save()
    
    print(f"   ✅ Étudiant configuré: {user_etudiant.get_full_name()}")
    print(f"      Matricule: {etudiant.matricule}")
    
    # Inscrire l'étudiant dans la classe
    inscription, created = Inscription.objects.get_or_create(
        etudiant=etudiant,
        classe=classe_l1,
        defaults={
            'annee_academique': '2025-2026',
            'statut': 'actif'
        }
    )
    if created:
        print(f"   ✅ Inscription créée: {classe_l1.nom}")
    else:
        inscription.statut = 'actif'
        inscription.save()
        print(f"   ℹ️  Inscription existante: {classe_l1.nom}")
    
    # 7. CONFIGURER LE BUREAU EXÉCUTIF
    print("\n🏛️ 7. Configuration du Bureau Exécutif...")
    try:
        user_bureau = Utilisateur.objects.get(email='bureau@uan.bf')
        user_bureau.role = 'bureau'
        user_bureau.nom = 'BUREAU'
        user_bureau.prenom = 'Exécutif'
        user_bureau.save()
    except Utilisateur.DoesNotExist:
        user_bureau = Utilisateur.objects.create(
            email='bureau@uan.bf',
            password=make_password('bureau123'),
            role='bureau',
            nom='BUREAU',
            prenom='Exécutif',
            is_active=True
        )
    
    # Le bureau est aussi un étudiant
    etudiant_bureau, created = Etudiant.objects.get_or_create(
        utilisateur=user_bureau,
        defaults={
            'matricule': 'BUR2025001',
            'date_naissance': '2004-06-20',
            'lieu_naissance': 'Bobo-Dioulasso',
            'nationalite': 'Burkinabè',
            'adresse': 'Secteur 15',
            'telephone': '+226 70 98 76 54'
        }
    )
    
    # Inscrire le membre du bureau dans la classe
    inscription_bureau, created = Inscription.objects.get_or_create(
        etudiant=etudiant_bureau,
        classe=classe_l1,
        defaults={
            'annee_academique': '2025-2026',
            'statut': 'actif'
        }
    )
    
    print(f"   ✅ Bureau configuré: {user_bureau.get_full_name()}")
    print(f"      Matricule: {etudiant_bureau.matricule}")
    print(f"      Note: Le bureau est aussi inscrit comme étudiant")
    
    # 8. RÉSUMÉ DE LA STRUCTURE
    print("\n" + "=" * 60)
    print("✅ STRUCTURE HIÉRARCHIQUE CONFIGURÉE")
    print("=" * 60)
    print(f"""
📊 HIÉRARCHIE:
   👔 Admin: {admin.get_full_name()} ({admin.email})
      └─ 👨‍🏫 Prof: {user_prof.get_full_name()} ({user_prof.email})
         └─ 📖 Matière: {matiere_info.nom}
            └─ 🏫 Classe: {classe_l1.nom}
               ├─ 👨‍🎓 Étudiant: {user_etudiant.get_full_name()} ({user_etudiant.email})
               └─ 🏛️ Bureau: {user_bureau.get_full_name()} ({user_bureau.email})

📚 FILIÈRE: {filiere_info.nom}
🏫 CLASSE: {classe_l1.nom}
📖 MATIÈRE: {matiere_info.nom} (Code: {matiere_info.code})
👨‍🏫 ENSEIGNANT: {user_prof.get_full_name()} - {enseignant.specialite}
👨‍🎓 ÉTUDIANTS INSCRITS: {Inscription.objects.filter(classe=classe_l1, statut='actif').count()}

🔐 COMPTES DE CONNEXION:
   • Admin: admin@uan.bf / admin123
   • Prof: j.ouedraogo@uan.bf / enseignant123
   • Étudiant: m.diallo@etu.bf / etudiant123
   • Bureau: bureau@uan.bf / bureau123
    """)
    
    print("✅ Réorganisation terminée avec succès!")
    return True

if __name__ == '__main__':
    try:
        reorganiser_structure()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
