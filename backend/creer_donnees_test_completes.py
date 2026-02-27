#!/usr/bin/env python
"""
Script pour créer des données de test complètes
Emploi du temps, notes, supports de cours, etc.
"""

import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import (
    Utilisateur, Etudiant, Enseignant, Matiere, 
    Classe, Inscription, EnseignementMatiere,
    EmploiDuTemps, Note, SupportCours, Evaluation, NoteEvaluation,
    AnneeAcademique, Universite
)

def creer_donnees_test():
    print("🔄 CRÉATION DES DONNÉES DE TEST COMPLÈTES")
    print("=" * 60)
    
    # Récupérer les objets existants
    try:
        prof = Enseignant.objects.get(utilisateur__email='j.ouedraogo@uan.bf')
        etudiant = Etudiant.objects.get(utilisateur__email='m.diallo@etu.bf')
        matiere = Matiere.objects.get(code='INFO-101')
        classe = Classe.objects.get(code='L1-INFO-A')
        enseignement = EnseignementMatiere.objects.get(
            enseignant=prof,
            matiere=matiere,
            classe=classe
        )
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("Assurez-vous d'avoir exécuté reorganiser_structure_complete.py d'abord!")
        return False
    
    # 1. CRÉER L'ANNÉE ACADÉMIQUE
    print("\n📅 1. Création de l'année académique...")
    
    # Récupérer l'université
    try:
        universite = Universite.objects.get(code='UAN')
    except Universite.DoesNotExist:
        print("❌ Erreur: Université UAN n'existe pas")
        print("Exécutez d'abord: python reorganiser_structure_complete.py")
        return False
    
    annee, created = AnneeAcademique.objects.get_or_create(
        universite=universite,
        libelle='2025-2026',
        defaults={
            'debut': datetime.now().date(),
            'fin': datetime.now().date() + timedelta(days=365),
            'active': True
        }
    )
    if created:
        print(f"   ✅ Année académique créée: {annee.libelle}")
    else:
        print(f"   ℹ️  Année académique existante: {annee.libelle}")
    
    # 2. CRÉER L'EMPLOI DU TEMPS
    print("\n📅 2. Création de l'emploi du temps...")
    
    # Cours du lundi
    emploi1, created = EmploiDuTemps.objects.get_or_create(
        matiere=matiere,
        jour='Lundi',
        heure_debut='08:00',
        annee_academique=annee,
        defaults={
            'heure_fin': '10:00',
            'salle': 'Amphi A',
            'semaine': 'toutes'
        }
    )
    if created:
        print(f"   ✅ Cours créé: Lundi 08:00-10:00")
    
    # Cours du mercredi
    emploi2, created = EmploiDuTemps.objects.get_or_create(
        matiere=matiere,
        jour='Mercredi',
        heure_debut='14:00',
        annee_academique=annee,
        defaults={
            'heure_fin': '16:00',
            'salle': 'Salle 12',
            'semaine': 'toutes'
        }
    )
    if created:
        print(f"   ✅ Cours créé: Mercredi 14:00-16:00")
    
    # Cours du vendredi
    emploi3, created = EmploiDuTemps.objects.get_or_create(
        matiere=matiere,
        jour='Vendredi',
        heure_debut='10:00',
        annee_academique=annee,
        defaults={
            'heure_fin': '12:00',
            'salle': 'Lab Info 1',
            'semaine': 'toutes'
        }
    )
    if created:
        print(f"   ✅ Cours créé: Vendredi 10:00-12:00")
    
    print(f"   📊 Total: {EmploiDuTemps.objects.filter(matiere=matiere).count()} cours/semaine")
    
    # 3. CRÉER DES ÉVALUATIONS
    print("\n📝 3. Création des évaluations...")
    
    eval1, created = Evaluation.objects.get_or_create(
        matiere=matiere,
        annee_academique=annee,
        titre='Contrôle Continu 1',
        defaults={
            'type_evaluation': 'devoir',
            'categorie': 'cc',
            'date_evaluation': datetime.now().date() - timedelta(days=15),
            'note_sur': 20.00,
            'coefficient': 1,
            'description': 'Premier contrôle continu',
            'cree_par': prof.utilisateur
        }
    )
    if created:
        print(f"   ✅ Évaluation créée: {eval1.titre}")
    
    eval2, created = Evaluation.objects.get_or_create(
        matiere=matiere,
        annee_academique=annee,
        titre='Contrôle Continu 2',
        defaults={
            'type_evaluation': 'devoir',
            'categorie': 'cc',
            'date_evaluation': datetime.now().date() - timedelta(days=7),
            'note_sur': 20.00,
            'coefficient': 1,
            'description': 'Deuxième contrôle continu',
            'cree_par': prof.utilisateur
        }
    )
    if created:
        print(f"   ✅ Évaluation créée: {eval2.titre}")
    
    eval3, created = Evaluation.objects.get_or_create(
        matiere=matiere,
        annee_academique=annee,
        titre='Examen Final',
        defaults={
            'type_evaluation': 'examen',
            'categorie': 'examen',
            'date_evaluation': datetime.now().date() + timedelta(days=30),
            'note_sur': 20.00,
            'coefficient': 2,
            'description': 'Examen final de fin de semestre',
            'cree_par': prof.utilisateur
        }
    )
    if created:
        print(f"   ✅ Évaluation créée: {eval3.titre}")
    
    # 4. CRÉER DES NOTES POUR L'ÉTUDIANT
    print("\n📊 4. Création des notes...")
    
    # Note CC1
    note_eval1, created = NoteEvaluation.objects.get_or_create(
        evaluation=eval1,
        etudiant=etudiant,
        defaults={
            'note': 15.5,
            'absent': False,
            'commentaire': 'Bon travail'
        }
    )
    if created:
        print(f"   ✅ Note créée: CC1 = 15.5/20")
    
    # Note CC2
    note_eval2, created = NoteEvaluation.objects.get_or_create(
        evaluation=eval2,
        etudiant=etudiant,
        defaults={
            'note': 17.0,
            'absent': False,
            'commentaire': 'Très bien'
        }
    )
    if created:
        print(f"   ✅ Note créée: CC2 = 17.0/20")
    
    # Note finale (moyenne des CC pour l'instant)
    note_finale, created = Note.objects.get_or_create(
        etudiant=etudiant,
        matiere=matiere,
        annee_academique=annee,
        defaults={
            'note_cc': 16.25,  # Moyenne des CC
            'note_examen': None,  # Pas encore passé
            'statut': 'publie',
            'publie': True,
            'saisie_par': prof.utilisateur
        }
    )
    if created:
        print(f"   ✅ Note finale créée: Moyenne CC = 16.25/20")
    
    # 5. CRÉER DES SUPPORTS DE COURS
    print("\n📚 5. Création des supports de cours...")
    
    support1, created = SupportCours.objects.get_or_create(
        matiere=matiere,
        enseignant=prof,
        titre='Introduction à l\'Informatique - Chapitre 1',
        defaults={
            'type_support': 'cours',
            'description': 'Introduction aux concepts de base',
            'visible': True
        }
    )
    if created:
        print(f"   ✅ Support créé: {support1.titre}")
    
    support2, created = SupportCours.objects.get_or_create(
        matiere=matiere,
        enseignant=prof,
        titre='TD 1 - Algorithmique',
        defaults={
            'type_support': 'td',
            'description': 'Exercices sur les algorithmes de base',
            'visible': True
        }
    )
    if created:
        print(f"   ✅ Support créé: {support2.titre}")
    
    support3, created = SupportCours.objects.get_or_create(
        matiere=matiere,
        enseignant=prof,
        titre='TP 1 - Programmation Python',
        defaults={
            'type_support': 'tp',
            'description': 'Introduction à Python',
            'visible': True
        }
    )
    if created:
        print(f"   ✅ Support créé: {support3.titre}")
    
    # 6. RÉSUMÉ
    print("\n" + "=" * 60)
    print("✅ DONNÉES DE TEST CRÉÉES AVEC SUCCÈS!")
    print("=" * 60)
    print(f"""
📊 RÉSUMÉ:
   • Emplois du temps: {EmploiDuTemps.objects.filter(matiere=matiere).count()} cours/semaine
   • Évaluations: {Evaluation.objects.filter(matiere=matiere, annee_academique=annee).count()}
   • Notes: {NoteEvaluation.objects.filter(etudiant=etudiant).count()} notes saisies
   • Supports de cours: {SupportCours.objects.filter(matiere=matiere).count()}
   
👨‍🏫 PROF OUEDRAOGO:
   • Matières enseignées: 1 (Informatique)
   • Étudiants: {Inscription.objects.filter(classe=classe, statut='actif').count()}
   • Cours/semaine: 3
   
👨‍🎓 MOUSSA DIALLO:
   • Classe: {classe.nom}
   • Notes: {NoteEvaluation.objects.filter(etudiant=etudiant).count()}
   • Moyenne CC: 16.25/20
    """)
    
    print("✅ Le dashboard devrait maintenant afficher des données!")
    return True

if __name__ == '__main__':
    try:
        creer_donnees_test()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
