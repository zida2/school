#!/usr/bin/env python
"""
Script de vérification avant création des données de test
Vérifie que tous les prérequis sont en place
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import (
    Utilisateur, Etudiant, Enseignant, Matiere, 
    Classe, Inscription, EnseignementMatiere
)

def verifier_prerequis():
    print("🔍 VÉRIFICATION DES PRÉREQUIS")
    print("=" * 60)
    
    erreurs = []
    warnings = []
    
    # 1. Vérifier Prof Ouedraogo
    print("\n1️⃣ Vérification du Prof Ouedraogo...")
    try:
        prof = Enseignant.objects.get(utilisateur__email='j.ouedraogo@uan.bf')
        print(f"   ✅ Prof trouvé: {prof.utilisateur.prenom} {prof.utilisateur.nom}")
    except Enseignant.DoesNotExist:
        erreurs.append("❌ Prof Ouedraogo (j.ouedraogo@uan.bf) n'existe pas")
        prof = None
    
    # 2. Vérifier Moussa Diallo
    print("\n2️⃣ Vérification de Moussa Diallo...")
    try:
        etudiant = Etudiant.objects.get(utilisateur__email='m.diallo@etu.bf')
        print(f"   ✅ Étudiant trouvé: {etudiant.utilisateur.prenom} {etudiant.utilisateur.nom}")
    except Etudiant.DoesNotExist:
        erreurs.append("❌ Moussa Diallo (m.diallo@etu.bf) n'existe pas")
        etudiant = None
    
    # 3. Vérifier la matière Informatique
    print("\n3️⃣ Vérification de la matière...")
    try:
        matiere = Matiere.objects.get(code='INFO-101')
        print(f"   ✅ Matière trouvée: {matiere.nom} ({matiere.code})")
    except Matiere.DoesNotExist:
        erreurs.append("❌ Matière INFO-101 n'existe pas")
        matiere = None
    
    # 4. Vérifier la classe
    print("\n4️⃣ Vérification de la classe...")
    try:
        classe = Classe.objects.get(code='L1-INFO-A')
        print(f"   ✅ Classe trouvée: {classe.nom} ({classe.code})")
    except Classe.DoesNotExist:
        erreurs.append("❌ Classe L1-INFO-A n'existe pas")
        classe = None
    
    # 5. Vérifier l'enseignement
    if prof and matiere and classe:
        print("\n5️⃣ Vérification de l'enseignement...")
        try:
            enseignement = EnseignementMatiere.objects.get(
                enseignant=prof,
                matiere=matiere,
                classe=classe
            )
            print(f"   ✅ Enseignement trouvé: {prof.utilisateur.nom} enseigne {matiere.nom} à {classe.nom}")
        except EnseignementMatiere.DoesNotExist:
            erreurs.append("❌ Lien enseignement Prof → Matière → Classe manquant")
    
    # 6. Vérifier l'inscription de l'étudiant
    if etudiant and classe:
        print("\n6️⃣ Vérification de l'inscription...")
        try:
            inscription = Inscription.objects.get(
                etudiant=etudiant,
                classe=classe,
                statut='actif'
            )
            print(f"   ✅ Inscription trouvée: {etudiant.utilisateur.nom} inscrit dans {classe.nom}")
        except Inscription.DoesNotExist:
            warnings.append("⚠️  Moussa Diallo n'est pas inscrit dans la classe L1-INFO-A")
    
    # RÉSUMÉ
    print("\n" + "=" * 60)
    if erreurs:
        print("❌ ERREURS CRITIQUES DÉTECTÉES")
        print("=" * 60)
        for erreur in erreurs:
            print(erreur)
        print("\n💡 SOLUTION:")
        print("   Exécutez d'abord: python reorganiser_structure_complete.py")
        return False
    elif warnings:
        print("⚠️  AVERTISSEMENTS")
        print("=" * 60)
        for warning in warnings:
            print(warning)
        print("\n✅ Vous pouvez continuer, mais certaines données peuvent manquer")
        return True
    else:
        print("✅ TOUS LES PRÉREQUIS SONT EN PLACE")
        print("=" * 60)
        print("\n🚀 Vous pouvez maintenant exécuter:")
        print("   python creer_donnees_test_completes.py")
        return True

if __name__ == '__main__':
    try:
        verifier_prerequis()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
