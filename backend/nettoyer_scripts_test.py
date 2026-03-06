#!/usr/bin/env python
"""
Script pour supprimer tous les fichiers de test et scripts de création rapide
"""
import os
import sys

# Fichiers à supprimer
fichiers_a_supprimer = [
    'afficher_enseignants.py',
    'afficher_etudiants.py',
    'ajouter_donnees_completes.py',
    'ajouter_donnees_test.py',
    'ajouter_matieres_enseignant.py',
    'ajouter_modeles_classes.py',
    'appliquer_integration.py',
    'appliquer_migrations.py',
    'creer_bureau_executif.py',
    'creer_canaux_defaut.py',
    'creer_classe_l1_info.py',
    'creer_donnees_moussa.py',
    'creer_donnees_services.py',
    'creer_donnees_test_completes.py',
    'fix_admin_account.py',
    'fix_role_professeur.py',
    'fix_users.py',
    'integrer_extensions.py',
    'nettoyer_paiements.py',
    'populate_data.py',
    'preparer_test_collaboratif.py',
    'reorganiser_structure_complete.py',
    'setup.py',
    'students_list.txt',
    'test_ajout_enseignant.py',
    'test_api_enseignants.py',
    'test_api_etudiant.py',
    'test_api_http.py',
    'test_api_sondages.py',
    'test_connexion_admin.py',
    'test_details_etudiant.py',
    'test_details_moussa.py',
    'test_evaluations_complete.py',
    'test_filieres_matieres.py',
    'test_integration_complete.py',
    'test_login_direct.py',
    'test_paiements_etudiants.py',
    'test_saisie_notes.py',
    'test_support_direct.py',
    'tester_notifications_email.py',
    'users_list.txt',
    'verification_complete.py',
    'verifier_avant_creation_donnees.py',
    'verifier_configuration_test.py',
    'verifier_deploiement.py',
    'verifier_donnees_ouedraogo_diallo.py',
    'verifier_donnees.py',
    'verifier_enseignant_ouedraogo.py',
    'verifier_relation_ouedraogo_diallo.py',
    'verifier_stats_enseignant.py',
    'verifier_test_collaboratif.py',
    'verifier_tous_comptes.py',
]

def main():
    print("🗑️  Nettoyage des scripts de test et création rapide...")
    print(f"📋 {len(fichiers_a_supprimer)} fichiers à supprimer\n")
    
    supprimes = 0
    non_trouves = 0
    
    for fichier in fichiers_a_supprimer:
        chemin = os.path.join(os.path.dirname(__file__), fichier)
        if os.path.exists(chemin):
            try:
                os.remove(chemin)
                print(f"✅ Supprimé: {fichier}")
                supprimes += 1
            except Exception as e:
                print(f"❌ Erreur lors de la suppression de {fichier}: {e}")
        else:
            non_trouves += 1
    
    print(f"\n📊 Résumé:")
    print(f"   ✅ Fichiers supprimés: {supprimes}")
    print(f"   ⚠️  Fichiers non trouvés: {non_trouves}")
    print(f"\n✨ Nettoyage terminé!")

if __name__ == '__main__':
    main()
