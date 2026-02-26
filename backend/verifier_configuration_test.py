#!/usr/bin/env python
"""
Script de vérification de la configuration pour le test collaboratif
Vérifie que les liens entre Étudiant, Enseignant et Admin sont corrects
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur, Etudiant, Enseignant, Matiere, Note, Filiere

def verifier_configuration():
    print("=" * 60)
    print("🔍 VÉRIFICATION DE LA CONFIGURATION POUR TEST COLLABORATIF")
    print("=" * 60)
    print()
    
    # 1. Vérifier les comptes
    print("📋 1. VÉRIFICATION DES COMPTES")
    print("-" * 60)
    
    comptes = {
        'Étudiant': 'm.diallo@etu.bf',
        'Enseignant': 'j.ouedraogo@uan.bf',
        'Bureau': 'bureau@uan.bf',
        'Admin': 'admin@uan.bf'
    }
    
    utilisateurs = {}
    for role, email in comptes.items():
        try:
            user = Utilisateur.objects.get(email=email)
            utilisateurs[role] = user
            print(f"✅ {role}: {user.nom} {user.prenom} ({email})")
            print(f"   Rôle: {user.role}")
        except Utilisateur.DoesNotExist:
            print(f"❌ {role}: Compte {email} introuvable!")
            return False
    
    print()
    
    # 2. Vérifier l'étudiant
    print("📋 2. VÉRIFICATION DE L'ÉTUDIANT")
    print("-" * 60)
    
    try:
        etudiant = Etudiant.objects.get(utilisateur=utilisateurs['Étudiant'])
        print(f"✅ Étudiant trouvé: {etudiant.utilisateur.nom} {etudiant.utilisateur.prenom}")
        print(f"   Matricule: {etudiant.matricule}")
        print(f"   Filière: {etudiant.filiere.nom if etudiant.filiere else 'Non assigné'}")
        print(f"   Niveau: {etudiant.niveau}")
    except Etudiant.DoesNotExist:
        print(f"❌ Profil étudiant introuvable pour {utilisateurs['Étudiant'].email}")
        return False
    
    print()
    
    # 3. Vérifier l'enseignant
    print("📋 3. VÉRIFICATION DE L'ENSEIGNANT")
    print("-" * 60)
    
    try:
        enseignant = Enseignant.objects.get(utilisateur=utilisateurs['Enseignant'])
        print(f"✅ Enseignant trouvé: {enseignant.utilisateur.nom} {enseignant.utilisateur.prenom}")
        print(f"   Spécialité: {enseignant.specialite}")
        
        # Vérifier les matières
        matieres = Matiere.objects.filter(enseignant=enseignant)
        print(f"   Matières enseignées: {matieres.count()}")
        for matiere in matieres:
            print(f"      - {matiere.nom} ({matiere.filiere.nom})")
    except Enseignant.DoesNotExist:
        print(f"❌ Profil enseignant introuvable pour {utilisateurs['Enseignant'].email}")
        return False
    
    print()
    
    # 4. Vérifier les notes de l'étudiant
    print("📋 4. VÉRIFICATION DES NOTES")
    print("-" * 60)
    
    notes = Note.objects.filter(etudiant=etudiant)
    print(f"Notes de {etudiant.utilisateur.nom}: {notes.count()}")
    
    notes_avec_enseignant = notes.filter(matiere__enseignant=enseignant)
    print(f"Notes avec l'enseignant {enseignant.utilisateur.nom}: {notes_avec_enseignant.count()}")
    
    if notes_avec_enseignant.count() > 0:
        print("\n✅ LIEN ÉTABLI:")
        for note in notes_avec_enseignant:
            print(f"   - {note.matiere.nom}: CC={note.note_cc}, Examen={note.note_examen}, Moyenne={note.moyenne}")
    else:
        print("\n⚠️ AUCUN LIEN:")
        print(f"   L'étudiant {etudiant.utilisateur.nom} n'a pas de notes avec l'enseignant {enseignant.utilisateur.nom}")
        print("   Les réclamations et demandes ne fonctionneront pas correctement!")
    
    print()
    
    # 5. Résumé
    print("=" * 60)
    print("📊 RÉSUMÉ DE LA CONFIGURATION")
    print("=" * 60)
    
    if notes_avec_enseignant.count() > 0:
        print("✅ Configuration CORRECTE pour le test collaboratif!")
        print()
        print("🎯 FLUX DE TEST POSSIBLES:")
        print("   1. Étudiant crée une réclamation sur une note")
        print("      → Enseignant la voit et peut la traiter")
        print()
        print("   2. Étudiant crée une demande à l'enseignant")
        print("      → Enseignant la voit et peut répondre")
        print()
        print("   3. Étudiant crée une demande à l'admin")
        print("      → Admin la voit et peut répondre")
        print()
        print("   4. Bureau crée des publications/sondages")
        print("      → Étudiant les voit")
        return True
    else:
        print("⚠️ Configuration INCOMPLÈTE!")
        print()
        print("🔧 ACTIONS NÉCESSAIRES:")
        print("   1. Assigner l'enseignant à des matières de la filière de l'étudiant")
        print("   2. Créer des notes pour l'étudiant dans ces matières")
        print()
        print("💡 Exécutez le script de préparation:")
        print("   python backend/preparer_test_collaboratif.py")
        return False

if __name__ == '__main__':
    try:
        success = verifier_configuration()
        print()
        if success:
            print("🎉 Prêt pour le test collaboratif!")
        else:
            print("⚠️ Configuration à compléter avant le test")
        print()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
