#!/usr/bin/env python
"""
Script pour vérifier les données de test Ouedraogo (enseignant) et Diallo (étudiant)
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur, Etudiant, Enseignant, Matiere, Classe, Note, EmploiDuTemps, SupportCours

def verifier_donnees():
    print("=" * 60)
    print("VÉRIFICATION DES DONNÉES OUEDRAOGO & DIALLO")
    print("=" * 60)
    
    # 1. Vérifier l'enseignant Ouedraogo
    print("\n📋 ENSEIGNANT OUEDRAOGO:")
    try:
        user_ouedraogo = Utilisateur.objects.get(email='j.ouedraogo@uan.bf')
        print(f"✅ Utilisateur trouvé: {user_ouedraogo.prenom} {user_ouedraogo.nom}")
        print(f"   Role: {user_ouedraogo.role}")
        
        enseignant = Enseignant.objects.get(utilisateur=user_ouedraogo)
        print(f"✅ Enseignant trouvé: ID={enseignant.id}")
        
        # Matières enseignées
        matieres = enseignant.matieres.all()
        print(f"\n   📚 Matières enseignées: {matieres.count()}")
        for matiere in matieres:
            print(f"      - {matiere.nom} ({matiere.code})")
            
        # Emplois du temps
        emplois = EmploiDuTemps.objects.filter(enseignant=enseignant)
        print(f"\n   📅 Emplois du temps: {emplois.count()}")
        for emploi in emplois:
            print(f"      - {emploi.jour}: {emploi.heure_debut}-{emploi.heure_fin}")
            
        # Supports de cours
        supports = SupportCours.objects.filter(enseignant=enseignant)
        print(f"\n   📄 Supports de cours: {supports.count()}")
        for support in supports:
            print(f"      - {support.titre}")
            
    except Utilisateur.DoesNotExist:
        print("❌ Utilisateur j.ouedraogo@uan.bf non trouvé!")
    except Enseignant.DoesNotExist:
        print("❌ Enseignant non trouvé pour cet utilisateur!")
    
    # 2. Vérifier l'étudiant Diallo
    print("\n\n📋 ÉTUDIANT DIALLO:")
    try:
        user_diallo = Utilisateur.objects.get(email='m.diallo@etu.bf')
        print(f"✅ Utilisateur trouvé: {user_diallo.prenom} {user_diallo.nom}")
        print(f"   Role: {user_diallo.role}")
        
        etudiant = Etudiant.objects.get(utilisateur=user_diallo)
        print(f"✅ Étudiant trouvé: ID={etudiant.id}, Matricule={etudiant.matricule}")
        
        if etudiant.classe:
            print(f"   Classe: {etudiant.classe.nom}")
        else:
            print("   ⚠️ Pas de classe assignée!")
            
        # Notes
        notes = Note.objects.filter(etudiant=etudiant)
        print(f"\n   📝 Notes: {notes.count()}")
        for note in notes:
            print(f"      - {note.matiere.nom}: CC={note.note_cc}, Examen={note.note_examen}, Moyenne={note.moyenne}")
            
    except Utilisateur.DoesNotExist:
        print("❌ Utilisateur m.diallo@etu.bf non trouvé!")
    except Etudiant.DoesNotExist:
        print("❌ Étudiant non trouvé pour cet utilisateur!")
    
    # 3. Vérifier la relation enseignant-étudiant
    print("\n\n📋 RELATION ENSEIGNANT-ÉTUDIANT:")
    try:
        enseignant = Enseignant.objects.get(utilisateur__email='j.ouedraogo@uan.bf')
        etudiant = Etudiant.objects.get(utilisateur__email='m.diallo@etu.bf')
        
        # Vérifier si l'étudiant a des notes dans les matières de l'enseignant
        matieres_enseignant = enseignant.matieres.all()
        notes_communes = Note.objects.filter(
            etudiant=etudiant,
            matiere__in=matieres_enseignant
        )
        
        print(f"✅ Notes de Diallo dans les matières de Ouedraogo: {notes_communes.count()}")
        for note in notes_communes:
            print(f"   - {note.matiere.nom}: Moyenne={note.moyenne}")
            
        if notes_communes.count() == 0:
            print("⚠️ Aucune note trouvée! Il faut créer les données de test.")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 4. Statistiques globales
    print("\n\n📊 STATISTIQUES GLOBALES:")
    print(f"   Total utilisateurs: {Utilisateur.objects.count()}")
    print(f"   Total enseignants: {Enseignant.objects.count()}")
    print(f"   Total étudiants: {Etudiant.objects.count()}")
    print(f"   Total matières: {Matiere.objects.count()}")
    print(f"   Total classes: {Classe.objects.count()}")
    print(f"   Total notes: {Note.objects.count()}")
    print(f"   Total emplois du temps: {EmploiDuTemps.objects.count()}")
    print(f"   Total supports: {SupportCours.objects.count()}")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    verifier_donnees()
