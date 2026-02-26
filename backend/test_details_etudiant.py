#!/usr/bin/env python3
"""
Script de test pour vérifier les détails complets d'un étudiant
"""
import os
import django
import sys

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Etudiant, Note, Paiement, Filiere

def test_details_etudiant():
    print("=" * 70)
    print("TEST DES DÉTAILS COMPLETS D'UN ÉTUDIANT")
    print("=" * 70)
    
    # Prendre le premier étudiant
    etudiant = Etudiant.objects.first()
    if not etudiant:
        print("❌ Aucun étudiant trouvé")
        return
    
    print(f"\n👤 ÉTUDIANT: {etudiant.prenom} {etudiant.nom}")
    print(f"   Matricule: {etudiant.matricule}")
    print(f"   Email: {etudiant.email}")
    
    # 1. INFORMATIONS ACADÉMIQUES
    print("\n" + "=" * 70)
    print("1. INFORMATIONS ACADÉMIQUES")
    print("=" * 70)
    
    filiere = etudiant.filiere
    print(f"\n📚 Filière: {filiere.nom if filiere else 'N/A'}")
    print(f"   Code: {filiere.code if filiere else 'N/A'}")
    print(f"   Niveau: {etudiant.niveau}")
    print(f"   Frais inscription: {filiere.frais_inscription:,} FCFA" if filiere else "   Frais: N/A")
    print(f"   Statut: {etudiant.statut}")
    print(f"   Date inscription: {etudiant.date_inscription}")
    
    # 2. NOTES ET PERFORMANCE
    print("\n" + "=" * 70)
    print("2. NOTES ET PERFORMANCE")
    print("=" * 70)
    
    notes = Note.objects.filter(etudiant=etudiant)
    notes_publiees = notes.filter(publie=True)
    
    print(f"\n📝 Total notes: {notes.count()}")
    print(f"   Notes publiées: {notes_publiees.count()}")
    
    if notes_publiees.exists():
        moyennes = [n.moyenne for n in notes_publiees if n.moyenne is not None]
        if moyennes:
            moyenne_generale = sum(moyennes) / len(moyennes)
            notes_reussies = len([m for m in moyennes if m >= 10])
            taux_reussite = (notes_reussies / len(moyennes) * 100)
            
            print(f"\n   📊 Moyenne générale: {moyenne_generale:.2f}/20")
            print(f"   ✅ Notes réussies: {notes_reussies}/{len(moyennes)}")
            print(f"   📈 Taux de réussite: {taux_reussite:.1f}%")
            
            print(f"\n   Détail des notes:")
            for note in notes_publiees:
                statut = "✅ Admis" if (note.moyenne or 0) >= 10 else "❌ Échec"
                print(f"   • {note.matiere.nom}: CC={note.note_cc:.2f}, Examen={note.note_examen:.2f}, Moy={note.moyenne:.2f} {statut}")
    else:
        print("   ⚠️  Aucune note publiée")
    
    # 3. TAUX DE RÉUSSITE DE LA CLASSE
    print("\n" + "=" * 70)
    print("3. TAUX DE RÉUSSITE DE LA CLASSE")
    print("=" * 70)
    
    if filiere:
        etudiants_classe = Etudiant.objects.filter(filiere=filiere, niveau=etudiant.niveau)
        print(f"\n👥 Étudiants dans la classe: {etudiants_classe.count()}")
        
        # Calculer le taux de réussite de la classe
        moyennes_classe = {}
        for etu in etudiants_classe:
            notes_etu = Note.objects.filter(etudiant=etu, publie=True)
            if notes_etu.exists():
                moyennes_etu = [n.moyenne for n in notes_etu if n.moyenne is not None]
                if moyennes_etu:
                    moyennes_classe[etu.id] = sum(moyennes_etu) / len(moyennes_etu)
        
        if moyennes_classe:
            etudiants_reussis = len([m for m in moyennes_classe.values() if m >= 10])
            taux_reussite_classe = (etudiants_reussis / len(moyennes_classe) * 100)
            moyenne_classe = sum(moyennes_classe.values()) / len(moyennes_classe)
            
            print(f"\n   📊 Moyenne de la classe: {moyenne_classe:.2f}/20")
            print(f"   ✅ Étudiants réussis: {etudiants_reussis}/{len(moyennes_classe)}")
            print(f"   📈 Taux de réussite classe: {taux_reussite_classe:.1f}%")
        else:
            print("   ⚠️  Aucune note disponible pour la classe")
    
    # 4. PAIEMENTS
    print("\n" + "=" * 70)
    print("4. SITUATION FINANCIÈRE")
    print("=" * 70)
    
    paiements = Paiement.objects.filter(etudiant=etudiant)
    print(f"\n💰 Total paiements: {paiements.count()}")
    
    if paiements.exists():
        total_paye = sum(p.montant for p in paiements)
        frais_inscription = filiere.frais_inscription if filiere else 0
        solde = frais_inscription - total_paye
        
        print(f"\n   💵 Frais inscription: {frais_inscription:,} FCFA")
        print(f"   ✅ Total payé: {total_paye:,} FCFA")
        print(f"   {'❌ Reste à payer' if solde > 0 else '✅ Solde'}: {abs(solde):,} FCFA")
        
        print(f"\n   Détail des paiements:")
        for p in paiements:
            print(f"   • {p.date_paiement}: {p.montant:,} FCFA ({p.mode}) - {p.type_paiement} [{p.statut}]")
    else:
        print("   ⚠️  Aucun paiement enregistré")
    
    # 5. RÉSUMÉ
    print("\n" + "=" * 70)
    print("5. RÉSUMÉ")
    print("=" * 70)
    
    print(f"\n✅ Informations personnelles: OK")
    print(f"✅ Informations académiques: OK")
    print(f"{'✅' if notes_publiees.exists() else '⚠️ '} Notes: {notes_publiees.count()} publiée(s)")
    print(f"{'✅' if paiements.exists() else '⚠️ '} Paiements: {paiements.count()} enregistré(s)")
    
    print("\n" + "=" * 70)
    print("✅ TEST TERMINÉ")
    print("=" * 70)

if __name__ == '__main__':
    test_details_etudiant()
