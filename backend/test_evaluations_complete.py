#!/usr/bin/env python3
"""
Test complet du système d'évaluations et notes
"""

import os
import django
import sys

# Configuration Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import (
    Utilisateur, Enseignant, Etudiant, Matiere, Filiere, 
    AnneeAcademique, Evaluation, NoteEvaluation
)
from datetime import date

def test_evaluations():
    print("=" * 60)
    print("TEST SYSTÈME D'ÉVALUATIONS ET NOTES")
    print("=" * 60)
    
    # 1. Récupérer un enseignant
    enseignant = Enseignant.objects.first()
    if not enseignant:
        print("❌ Aucun enseignant trouvé")
        return
    
    print(f"\n✅ Enseignant: {enseignant.prenom} {enseignant.nom}")
    
    # 2. Récupérer une matière de cet enseignant
    matiere = enseignant.matieres.first()
    if not matiere:
        print("❌ Aucune matière trouvée pour cet enseignant")
        return
    
    print(f"✅ Matière: {matiere.nom} (Filière: {matiere.filiere.nom})")
    
    # 3. Récupérer l'année académique active
    annee = AnneeAcademique.objects.filter(active=True).first()
    if not annee:
        annee = AnneeAcademique.objects.first()
    
    print(f"✅ Année académique: {annee.annee}")
    
    # 4. Créer des évaluations de test
    print("\n" + "=" * 60)
    print("CRÉATION DES ÉVALUATIONS")
    print("=" * 60)
    
    evaluations_data = [
        {
            'titre': 'Devoir 1 - Introduction',
            'type_evaluation': 'devoir',
            'categorie': 'cc',
            'coefficient': 1,
            'note_sur': 20,
            'date_evaluation': date(2026, 3, 1),
            'description': 'Premier devoir sur les bases'
        },
        {
            'titre': 'Interrogation 1',
            'type_evaluation': 'interrogation',
            'categorie': 'cc',
            'coefficient': 1,
            'note_sur': 10,
            'date_evaluation': date(2026, 3, 15),
            'description': 'Test rapide sur le chapitre 1'
        },
        {
            'titre': 'TP 1 - Pratique',
            'type_evaluation': 'tp',
            'categorie': 'cc',
            'coefficient': 2,
            'note_sur': 20,
            'date_evaluation': date(2026, 3, 20),
            'description': 'Travaux pratiques en laboratoire'
        },
        {
            'titre': 'Examen Final',
            'type_evaluation': 'examen',
            'categorie': 'examen',
            'coefficient': 1,
            'note_sur': 20,
            'date_evaluation': date(2026, 6, 15),
            'description': 'Examen de fin de semestre'
        }
    ]
    
    evaluations_creees = []
    for eval_data in evaluations_data:
        # Vérifier si l'évaluation existe déjà
        eval_existante = Evaluation.objects.filter(
            matiere=matiere,
            annee_academique=annee,
            titre=eval_data['titre']
        ).first()
        
        if eval_existante:
            print(f"⚠️  Évaluation existe déjà: {eval_data['titre']}")
            evaluations_creees.append(eval_existante)
        else:
            evaluation = Evaluation.objects.create(
                matiere=matiere,
                annee_academique=annee,
                cree_par=enseignant.utilisateur,
                **eval_data
            )
            evaluations_creees.append(evaluation)
            print(f"✅ Créée: {evaluation.titre} ({evaluation.type_evaluation}, {evaluation.categorie.upper()})")
    
    # 5. Récupérer les étudiants de la filière
    etudiants = Etudiant.objects.filter(filiere=matiere.filiere)[:5]
    print(f"\n✅ {etudiants.count()} étudiants trouvés dans la filière")
    
    # 6. Générer les notes vides pour chaque évaluation
    print("\n" + "=" * 60)
    print("GÉNÉRATION DES NOTES VIDES")
    print("=" * 60)
    
    for evaluation in evaluations_creees:
        for etudiant in etudiants:
            note, created = NoteEvaluation.objects.get_or_create(
                evaluation=evaluation,
                etudiant=etudiant,
                defaults={'saisie_par': enseignant.utilisateur}
            )
            if created:
                print(f"✅ Note créée: {etudiant.prenom} {etudiant.nom} - {evaluation.titre}")
    
    # 7. Saisir quelques notes de test
    print("\n" + "=" * 60)
    print("SAISIE DES NOTES DE TEST")
    print("=" * 60)
    
    import random
    for evaluation in evaluations_creees:
        notes = NoteEvaluation.objects.filter(evaluation=evaluation)
        for note in notes[:3]:  # Saisir 3 notes par évaluation
            if not note.note:  # Si pas déjà saisie
                # Générer une note aléatoire
                note_valeur = round(random.uniform(8, 18), 2)
                note.note = note_valeur
                note.saisie_par = enseignant.utilisateur
                note.save()
                print(f"✅ Note saisie: {note.etudiant.prenom} {note.etudiant.nom} - {evaluation.titre}: {note_valeur}/{evaluation.note_sur}")
    
    # 8. Calculer les moyennes CC et Examen pour un étudiant
    print("\n" + "=" * 60)
    print("CALCUL DES MOYENNES")
    print("=" * 60)
    
    etudiant_test = etudiants.first()
    print(f"\nÉtudiant: {etudiant_test.prenom} {etudiant_test.nom}")
    print("-" * 60)
    
    # Notes CC
    notes_cc = NoteEvaluation.objects.filter(
        etudiant=etudiant_test,
        evaluation__matiere=matiere,
        evaluation__categorie='cc',
        note__isnull=False,
        absent=False
    )
    
    if notes_cc.exists():
        total_points_cc = 0
        total_coef_cc = 0
        print("\nNotes CC:")
        for note in notes_cc:
            # Convertir la note sur 20
            note_sur_20 = (float(note.note) / float(note.evaluation.note_sur)) * 20
            points = note_sur_20 * note.evaluation.coefficient
            total_points_cc += points
            total_coef_cc += note.evaluation.coefficient
            print(f"  - {note.evaluation.titre}: {note.note}/{note.evaluation.note_sur} "
                  f"(sur 20: {note_sur_20:.2f}) × coef {note.evaluation.coefficient} = {points:.2f} pts")
        
        moyenne_cc = total_points_cc / total_coef_cc if total_coef_cc > 0 else 0
        print(f"\n📊 Moyenne CC: {moyenne_cc:.2f}/20")
    else:
        moyenne_cc = 0
        print("\n⚠️  Aucune note CC saisie")
    
    # Notes Examen
    notes_examen = NoteEvaluation.objects.filter(
        etudiant=etudiant_test,
        evaluation__matiere=matiere,
        evaluation__categorie='examen',
        note__isnull=False,
        absent=False
    )
    
    if notes_examen.exists():
        total_points_examen = 0
        total_coef_examen = 0
        print("\nNotes Examen:")
        for note in notes_examen:
            # Convertir la note sur 20
            note_sur_20 = (float(note.note) / float(note.evaluation.note_sur)) * 20
            points = note_sur_20 * note.evaluation.coefficient
            total_points_examen += points
            total_coef_examen += note.evaluation.coefficient
            print(f"  - {note.evaluation.titre}: {note.note}/{note.evaluation.note_sur} "
                  f"(sur 20: {note_sur_20:.2f}) × coef {note.evaluation.coefficient} = {points:.2f} pts")
        
        moyenne_examen = total_points_examen / total_coef_examen if total_coef_examen > 0 else 0
        print(f"\n📊 Moyenne Examen: {moyenne_examen:.2f}/20")
    else:
        moyenne_examen = 0
        print("\n⚠️  Aucune note Examen saisie")
    
    # Moyenne finale
    if moyenne_cc > 0 or moyenne_examen > 0:
        moyenne_finale = (moyenne_cc * 0.4) + (moyenne_examen * 0.6)
        print(f"\n🎯 MOYENNE FINALE: {moyenne_finale:.2f}/20")
        print(f"   Formule: ({moyenne_cc:.2f} × 40%) + ({moyenne_examen:.2f} × 60%)")
        
        if moyenne_finale >= 10:
            print(f"   ✅ VALIDÉ")
        else:
            print(f"   ❌ AJOURNÉ")
    
    # 9. Statistiques globales
    print("\n" + "=" * 60)
    print("STATISTIQUES GLOBALES")
    print("=" * 60)
    
    total_evaluations = Evaluation.objects.filter(
        matiere=matiere,
        annee_academique=annee
    ).count()
    
    total_notes = NoteEvaluation.objects.filter(
        evaluation__matiere=matiere,
        evaluation__annee_academique=annee
    ).count()
    
    notes_saisies = NoteEvaluation.objects.filter(
        evaluation__matiere=matiere,
        evaluation__annee_academique=annee,
        note__isnull=False
    ).count()
    
    notes_absents = NoteEvaluation.objects.filter(
        evaluation__matiere=matiere,
        evaluation__annee_academique=annee,
        absent=True
    ).count()
    
    print(f"\n📊 Matière: {matiere.nom}")
    print(f"   - Évaluations créées: {total_evaluations}")
    print(f"   - Notes totales: {total_notes}")
    print(f"   - Notes saisies: {notes_saisies} ({notes_saisies/total_notes*100:.1f}%)")
    print(f"   - Absences: {notes_absents}")
    
    print("\n" + "=" * 60)
    print("✅ TEST TERMINÉ AVEC SUCCÈS")
    print("=" * 60)

if __name__ == '__main__':
    test_evaluations()
