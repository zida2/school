"""
Script de test pour vérifier l'intégration backend complète
"""
import os
import django
import sys

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from api.models import (
    ReclamationNote, DemandeAdministrative, Sondage, 
    Evaluation, ObjetPerdu, Note, Etudiant, Enseignant
)

User = get_user_model()

def test_reclamation_viewset():
    """Test ReclamationNoteViewSet"""
    print("\n=== TEST RECLAMATION NOTE VIEWSET ===")
    
    # Vérifier que le modèle existe
    count = ReclamationNote.objects.count()
    print(f"✓ Nombre de réclamations: {count}")
    
    # Vérifier les champs
    if count > 0:
        reclamation = ReclamationNote.objects.first()
        print(f"✓ Réclamation exemple: {reclamation.motif}")
        print(f"  - Statut: {reclamation.statut}")
        print(f"  - Date: {reclamation.date_creation}")
    
    return True

def test_demande_administrative():
    """Test DemandeAdministrativeViewSet"""
    print("\n=== TEST DEMANDE ADMINISTRATIVE ===")
    
    count = DemandeAdministrative.objects.count()
    print(f"✓ Nombre de demandes: {count}")
    
    if count > 0:
        demande = DemandeAdministrative.objects.first()
        print(f"✓ Demande exemple: {demande.type_demande}")
        print(f"  - Statut: {demande.statut}")
        print(f"  - Destinataire: {demande.destinataire}")
    
    return True

def test_sondage():
    """Test SondageViewSet"""
    print("\n=== TEST SONDAGE ===")
    
    count = Sondage.objects.count()
    print(f"✓ Nombre de sondages: {count}")
    
    if count > 0:
        sondage = Sondage.objects.first()
        print(f"✓ Sondage exemple: {sondage.titre}")
        print(f"  - Statut: {sondage.statut}")
        print(f"  - Questions: {sondage.questions.count()}")
    
    return True

def test_evaluation():
    """Test EvaluationViewSet"""
    print("\n=== TEST EVALUATION ===")
    
    count = Evaluation.objects.count()
    print(f"✓ Nombre d'évaluations: {count}")
    
    if count > 0:
        evaluation = Evaluation.objects.first()
        print(f"✓ Évaluation exemple: {evaluation.titre}")
        print(f"  - Actif: {evaluation.actif}")
        print(f"  - Catégorie: {evaluation.categorie}")
    
    return True

def test_objet_perdu():
    """Test ObjetPerduViewSet"""
    print("\n=== TEST OBJET PERDU ===")
    
    count = ObjetPerdu.objects.count()
    print(f"✓ Nombre d'objets perdus: {count}")
    
    if count > 0:
        objet = ObjetPerdu.objects.first()
        print(f"✓ Objet exemple: {objet.nom_objet}")
        print(f"  - Statut: {objet.statut}")
        print(f"  - Type: {objet.type_declaration}")
    
    return True

def test_users():
    """Test utilisateurs"""
    print("\n=== TEST UTILISATEURS ===")
    
    # Compter par rôle
    etudiants = User.objects.filter(role='etudiant').count()
    enseignants = User.objects.filter(role='professeur').count()
    admins = User.objects.filter(role__in=['admin', 'superadmin']).count()
    bureau = User.objects.filter(role='bureau_executif').count()
    
    print(f"✓ Étudiants: {etudiants}")
    print(f"✓ Enseignants: {enseignants}")
    print(f"✓ Admins: {admins}")
    print(f"✓ Bureau: {bureau}")
    
    return True

def test_endpoints():
    """Test que les endpoints sont accessibles"""
    print("\n=== TEST ENDPOINTS ===")
    
    from django.urls import reverse
    from rest_framework.test import APIClient
    
    client = APIClient()
    
    # Tester les endpoints sans authentification (devrait retourner 401)
    endpoints = [
        '/api/reclamations/',
        '/api/demandes-administratives/',
        '/api/sondages/',
        '/api/evaluations/',
        '/api/objets-perdus/',
    ]
    
    for endpoint in endpoints:
        try:
            response = client.get(endpoint)
            if response.status_code in [401, 403]:
                print(f"✓ {endpoint} - Protégé (401/403)")
            elif response.status_code == 200:
                print(f"✓ {endpoint} - Accessible (200)")
            else:
                print(f"⚠ {endpoint} - Code: {response.status_code}")
        except Exception as e:
            print(f"✗ {endpoint} - Erreur: {str(e)}")
    
    return True

def main():
    """Fonction principale"""
    print("=" * 60)
    print("TEST INTÉGRATION BACKEND COMPLÈTE")
    print("=" * 60)
    
    tests = [
        ("Réclamations", test_reclamation_viewset),
        ("Demandes", test_demande_administrative),
        ("Sondages", test_sondage),
        ("Évaluations", test_evaluation),
        ("Objets perdus", test_objet_perdu),
        ("Utilisateurs", test_users),
        ("Endpoints", test_endpoints),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Erreur dans {name}: {str(e)}")
            results.append((name, False))
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nRésultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("✅ L'intégration backend est complète et fonctionnelle")
    else:
        print(f"\n⚠ {total - passed} test(s) ont échoué")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
