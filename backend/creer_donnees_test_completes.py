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
    EmploiDuTemps, Note, SupportCours, Evaluation, NoteEvaluation
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
    
    # 1. CRÉER L'EMPLOI DU TEMPS
    print("\n📅 1. Création de l'emploi du temps...")
    
    # Cours du lundi
    emploi1, created = EmploiDuTemps.objects.get_or_create(
        classe=classe,
        matiere=matiere,
        enseignant=prof,
        jour_semaine='Lundi',
        defaults={
            'heure_debut': '08:00',
            'heure_fin': '10:00',
            'salle': 'Amphi A',
            'type_cours': 'CM'
        }
    )
    if created:
        print(f"   ✅ Cours créé: Lundi 08:00-10:00 (CM)")
    
    # Cours du mercredi
    emploi2, created = EmploiDuTemps.objects.get_or_create(
        classe=classe,
        matiere=matiere,
        enseignant=prof,
        jour_semaine='Mercredi',
        defaults={
            'heure_debut': '14:00',
            'heure_fin': '16:00',
            'salle': 'Salle 12',
            'type_cours': 'TD'
        }
    )
    if created:
        print(f"   ✅ Cours créé: Mercredi 14:00-16:00 (TD)")
    
    # Cours du vendredi
    emploi3, created = EmploiDuTemps.objects.get_or_create(
        classe=classe,
        matiere=matiere,
        enseignant=prof,
        jour_semaine='Vendredi',
        defaults={
            'heure_debut': '10:00',
            'heure_fin': '12:00',
            'salle': 'Lab Info 1',
            'type_cours': 'TP'
        }
    )
    if created:
        print(f"   ✅ Cours créé: Vendredi 10:00-12:00 (TP)")
    
    print(f"   📊 Total: {EmploiDuTemps.objects.filter(classe=classe).count()} cours/semaine")
    
    # 2. CRÉER DES ÉVALUATIONS
    print("\n📝 2. Création des évaluations...")
    
    eval1, created = Evaluation.objects.get_or_create(
        matiere=matiere,
        classe=classe,
        enseignant=prof,
        titre='Contrôle Continu 1',
        defaults={
            'type_evaluation': 'CC',
            'date': datetime.now().date() - timedelta(days=15),
            'duree': 60,
            'note_totale': 20,
            'coefficient': 1
        }
    )
    if created:
        print(f"   ✅ Évaluation créée: {eval1.titre}")
    
    eval2, created = Evaluation.objects.get_or_create(
        matiere=matiere,
        classe=classe,
        enseignant=prof,
        titre='Contrôle Continu 2',
        defaults={
            'type_evaluation': 'CC',
            'date': datetime.now().date() - timedelta(days=7),
            'duree': 60,
            'note_totale': 20,
            'coefficient': 1
        }
    )
    if created:
        print(f"   ✅ Évaluation créée: {eval2.titre}")
    
    eval3, created = Evaluation.objects.get_or_create(
        matiere=matiere,
        classe=classe,
        enseignant=prof,
        titre='Examen Final',
        defaults={
            'type_evaluation': 'Examen',
            'date': datetime.now().date() + timedelta(days=30),
            'duree': 120,
            'note_totale': 20,
            'coefficient': 2
        }
    )
    if created:
        print(f"   ✅ Évaluation créée: {eval3.titre}")
    
    # 3. CRÉER DES NOTES POUR L'ÉTUDIANT
    print("\n📊 3. Création des notes...")
    
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
        defaults={
            'note_cc': 16.25,  # Moyenne des CC
            'note_examen': 0,  # Pas encore passé
            'note_tp': 16.0,
            'statut': 'en_attente'
        }
    )
    if created:
        print(f"   ✅ Note finale créée: Moyenne CC = 16.25/20")
    
    # 4. CRÉER DES SUPPORTS DE COURS
    print("\n📚 4. Création des supports de cours...")
    
    support1, created = SupportCours.objects.get_or_create(
        matiere=matiere,
        enseignant=prof,
        titre='Introduction à l\'Informatique - Chapitre 1',
        defaults={
            'type_support': 'cours',
            'description': 'Introduction aux concepts de base',
            'date_publication': datetime.now()
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
            'date_publication': datetime.now() - timedelta(days=5)
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
            'date_publication': datetime.now() - timedelta(days=3)
        }
    )
    if created:
        print(f"   ✅ Support créé: {support3.titre}")
    
    # 5. RÉSUMÉ
    print("\n" + "=" * 60)
    print("✅ DONNÉES DE TEST CRÉÉES AVEC SUCCÈS!")
    print("=" * 60)
    print(f"""
📊 RÉSUMÉ:
   • Emplois du temps: {EmploiDuTemps.objects.filter(classe=classe).count()} cours/semaine
   • Évaluations: {Evaluation.objects.filter(matiere=matiere, classe=classe).count()}
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
