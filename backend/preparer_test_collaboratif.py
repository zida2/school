#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de préparation pour le test collaboratif
Configure les liens entre Étudiant, Enseignant et Admin
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import (
    Utilisateur, Etudiant, Enseignant, Filiere, Matiere, Note
)
from django.db import transaction

def print_section(title):
    """Affiche un titre de section"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_success(message):
    """Affiche un message de succès"""
    print(f"✅ {message}")

def print_info(message):
    """Affiche un message d'information"""
    print(f"ℹ️  {message}")

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"❌ {message}")

def print_warning(message):
    """Affiche un avertissement"""
    print(f"⚠️  {message}")

@transaction.atomic
def preparer_test_collaboratif():
    """
    Prépare la base de données pour le test collaboratif
    """
    
    print_section("PRÉPARATION DU TEST COLLABORATIF")
    print_info("Configuration des acteurs pour le test en temps réel")
    
    # ========== VÉRIFICATION DES COMPTES ==========
    print_section("1. VÉRIFICATION DES COMPTES")
    
    # Étudiant
    try:
        user_etudiant = Utilisateur.objects.get(email='m.diallo@etu.bf')
        etudiant = user_etudiant.etudiant
        print_success(f"Étudiant trouvé: {etudiant.nom} {etudiant.prenom}")
        print_info(f"   Filière: {etudiant.filiere.nom if etudiant.filiere else 'Non assignée'}")
        print_info(f"   Niveau: {etudiant.niveau}")
    except Utilisateur.DoesNotExist:
        print_error("Compte étudiant m.diallo@etu.bf non trouvé!")
        return False
    except Exception as e:
        print_error(f"Erreur étudiant: {e}")
        return False
    
    # Enseignant
    try:
        user_enseignant = Utilisateur.objects.get(email='j.ouedraogo@uan.bf')
        enseignant = user_enseignant.enseignant
        print_success(f"Enseignant trouvé: {enseignant.nom} {enseignant.prenom}")
        print_info(f"   Spécialité: {enseignant.specialite}")
    except Utilisateur.DoesNotExist:
        print_error("Compte enseignant j.ouedraogo@uan.bf non trouvé!")
        return False
    except Exception as e:
        print_error(f"Erreur enseignant: {e}")
        return False
    
    # Admin
    try:
        user_admin = Utilisateur.objects.get(email='admin@uan.bf')
        print_success(f"Admin trouvé: {user_admin.email}")
        print_info(f"   Rôle: {user_admin.role}")
    except Utilisateur.DoesNotExist:
        print_error("Compte admin admin@uan.bf non trouvé!")
        return False
    
    # Bureau
    try:
        user_bureau = Utilisateur.objects.get(email='bureau@uan.bf')
        print_success(f"Bureau trouvé: {user_bureau.email}")
        print_info(f"   Rôle: {user_bureau.role}")
    except Utilisateur.DoesNotExist:
        print_warning("Compte bureau bureau@uan.bf non trouvé (optionnel)")
    
    # ========== VÉRIFICATION DE LA FILIÈRE ==========
    print_section("2. VÉRIFICATION DE LA FILIÈRE")
    
    if not etudiant.filiere:
        print_error("L'étudiant n'a pas de filière assignée!")
        return False
    
    filiere = etudiant.filiere
    print_success(f"Filière: {filiere.nom}")
    print_info(f"   Code: {filiere.code}")
    print_info(f"   Niveau: {filiere.niveau}")
    
    # ========== VÉRIFICATION DES MATIÈRES ==========
    print_section("3. VÉRIFICATION DES MATIÈRES")
    
    matieres = Matiere.objects.filter(filiere=filiere)
    print_info(f"Matières de la filière {filiere.nom}: {matieres.count()}")
    
    if matieres.count() == 0:
        print_warning("Aucune matière trouvée pour cette filière!")
        print_info("Création de matières de test...")
        
        # Créer des matières de test
        matieres_test = [
            {'nom': 'Programmation', 'code': 'PROG101', 'coefficient': 3},
            {'nom': 'Base de données', 'code': 'BDD101', 'coefficient': 3},
            {'nom': 'Mathématiques', 'code': 'MATH101', 'coefficient': 2},
            {'nom': 'Algorithmique', 'code': 'ALGO101', 'coefficient': 3},
        ]
        
        matieres_creees = []
        for mat_data in matieres_test:
            matiere, created = Matiere.objects.get_or_create(
                code=mat_data['code'],
                filiere=filiere,
                defaults={
                    'nom': mat_data['nom'],
                    'coefficient': mat_data['coefficient']
                }
            )
            matieres_creees.append(matiere)
            if created:
                print_success(f"   Matière créée: {matiere.nom}")
            else:
                print_info(f"   Matière existante: {matiere.nom}")
        
        matieres = matieres_creees
    else:
        for matiere in matieres:
            print_info(f"   - {matiere.nom} (Coef: {matiere.coefficient})")
    
    # ========== ASSIGNATION ENSEIGNANT → MATIÈRES VIA NOTES ==========
    print_section("4. CRÉATION DE NOTES DE TEST (Lien Enseignant-Étudiant)")
    
    notes_creees = 0
    for matiere in matieres[:4]:  # Limiter à 4 matières
        # Vérifier si une note existe déjà
        note_existante = Note.objects.filter(
            etudiant=etudiant,
            matiere=matiere
        ).first()
        
        if not note_existante:
            # Créer une note de test
            import random
            note_cc = random.randint(10, 18)
            note_examen = random.randint(10, 18)
            moyenne = (note_cc + note_examen) / 2
            
            note = Note.objects.create(
                etudiant=etudiant,
                matiere=matiere,
                note_cc=note_cc,
                note_examen=note_examen,
                moyenne=moyenne,
                semestre='S1',
                annee_academique='2024-2025',
                statut='validee'
            )
            print_success(f"   Note créée: {matiere.nom} - CC:{note_cc} Exam:{note_examen} Moy:{moyenne:.2f}")
            print_info(f"      → Enseignant {enseignant.nom} lié à {etudiant.nom} via {matiere.nom}")
            notes_creees += 1
        else:
            print_info(f"   Note existante: {matiere.nom} - Moy:{note_existante.moyenne:.2f}")
    
    if notes_creees > 0:
        print_success(f"{notes_creees} nouvelle(s) note(s) créée(s)")
    
    # Vérifier que l'enseignant apparaîtra dans la liste de l'étudiant
    notes_etudiant = Note.objects.filter(etudiant=etudiant).select_related('matiere')
    matieres_avec_notes = set(n.matiere for n in notes_etudiant)
    
    print_info(f"\n📊 L'étudiant verra l'enseignant {enseignant.nom} pour:")
    for matiere in matieres_avec_notes:
        print_info(f"   - {matiere.nom}")
    
    # ========== RÉSUMÉ FINAL ==========
    print_section("RÉSUMÉ DE LA CONFIGURATION")
    
    print("\n📊 ACTEURS DU TEST:")
    print(f"   👨‍🎓 Étudiant: {etudiant.nom} {etudiant.prenom} (m.diallo@etu.bf)")
    print(f"   👨‍🏫 Enseignant: {enseignant.nom} {enseignant.prenom} (j.ouedraogo@uan.bf)")
    print(f"   👔 Admin: {user_admin.email}")
    
    print("\n🎓 CONFIGURATION:")
    print(f"   Filière: {filiere.nom}")
    print(f"   Matières: {matieres.count()}")
    print(f"   Notes: {Note.objects.filter(etudiant=etudiant).count()}")
    
    print("\n🔗 LIENS:")
    notes_etudiant = Note.objects.filter(etudiant=etudiant).count()
    print(f"   L'étudiant a {notes_etudiant} note(s)")
    print(f"   L'enseignant {enseignant.nom} apparaîtra dans 'Mes enseignants'")
    
    print("\n✅ PRÊT POUR LE TEST COLLABORATIF!")
    print("\n📋 SCÉNARIO DE TEST:")
    print("   1. Étudiant (m.diallo@etu.bf) crée une réclamation sur une note")
    print("   2. Enseignant (j.ouedraogo@uan.bf) voit la réclamation et la traite")
    print("   3. Étudiant voit la réponse et la note corrigée")
    print("   4. Étudiant crée une demande administrative")
    print("   5. Admin (admin@uan.bf) voit la demande et répond")
    print("   6. Étudiant voit la réponse de l'admin")
    
    print("\n🚀 COMMANDES POUR DÉMARRER:")
    print("   Backend:  cd backend && python manage.py runserver")
    print("   Frontend: Ouvrir http://127.0.0.1:8080/index.html")
    
    return True

if __name__ == '__main__':
    try:
        success = preparer_test_collaboratif()
        if success:
            print("\n" + "="*60)
            print("  ✅ CONFIGURATION TERMINÉE AVEC SUCCÈS!")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("  ❌ ERREUR LORS DE LA CONFIGURATION")
            print("="*60)
    except Exception as e:
        print_error(f"Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
