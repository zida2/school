#!/usr/bin/env python
"""
Script de vérification complète du système
"""
import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur, Enseignant, Etudiant, Filiere, Matiere, Note

print("\n" + "="*70)
print(" VÉRIFICATION COMPLÈTE DU SYSTÈME UniERP BF Premium")
print("="*70)

# 1. Base de données
print("\n📊 BASE DE DONNÉES:")
print(f"   ✅ Utilisateurs: {Utilisateur.objects.count()}")
print(f"   ✅ Enseignants: {Enseignant.objects.count()}")
print(f"   ✅ Étudiants: {Etudiant.objects.count()}")
print(f"   ✅ Filières: {Filiere.objects.count()}")
print(f"   ✅ Matières: {Matiere.objects.count()}")
print(f"   ✅ Notes: {Note.objects.count()}")

# 2. Comptes de test
print("\n👥 COMPTES DE TEST:")
comptes = [
    ('superadmin@erp.bf', 'superadmin'),
    ('admin@uan.bf', 'admin'),
    ('j.ouedraogo@uan.bf', 'professeur'),
    ('m.diallo@etu.bf', 'etudiant'),
]

for email, role in comptes:
    try:
        user = Utilisateur.objects.get(email=email)
        status = "✅" if user.role == role else "⚠️"
        print(f"   {status} {email} ({user.role})")
    except Utilisateur.DoesNotExist:
        print(f"   ❌ {email} - NON TROUVÉ")

# 3. Enseignants avec matières
print("\n👨‍🏫 ENSEIGNANTS:")
for ens in Enseignant.objects.all():
    nb_matieres = ens.matieres.count()
    print(f"   ✅ {ens.prenom} {ens.nom} - {nb_matieres} matière(s)")

# 4. Étudiants L1 Info
print("\n🎓 ÉTUDIANTS L1 INFORMATIQUE:")
l1_info = Etudiant.objects.filter(niveau='L1', filiere__nom__icontains='Informatique')
print(f"   ✅ {l1_info.count()} étudiant(s) trouvé(s)")
for etu in l1_info[:3]:
    nb_notes = Note.objects.filter(etudiant=etu).count()
    print(f"      - {etu.prenom} {etu.nom} ({etu.email}) - {nb_notes} notes")

# 5. Test API HTTP
print("\n🌐 TEST API HTTP:")
API_BASE = 'http://127.0.0.1:8000/api'

try:
    # Test connexion
    response = requests.post(f'{API_BASE}/auth/login/', 
                            json={'email': 'admin@uan.bf', 'password': 'Admin2024!'},
                            timeout=5)
    
    if response.status_code == 200:
        print("   ✅ Connexion admin réussie")
        token = response.json().get('access')
        
        # Test récupération enseignants
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{API_BASE}/enseignants/', headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'results' in data:
                enseignants = data['results']
            else:
                enseignants = data
            print(f"   ✅ API enseignants: {len(enseignants)} enseignant(s)")
        else:
            print(f"   ❌ API enseignants: Erreur {response.status_code}")
        
        # Test récupération étudiants
        response = requests.get(f'{API_BASE}/etudiants/', headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'results' in data:
                etudiants = data['results']
            else:
                etudiants = data
            print(f"   ✅ API étudiants: {len(etudiants)} étudiant(s)")
        else:
            print(f"   ❌ API étudiants: Erreur {response.status_code}")
            
    else:
        print(f"   ❌ Connexion échouée: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("   ❌ SERVEUR NON DÉMARRÉ!")
    print("      → Exécuter: python manage.py runserver")
except Exception as e:
    print(f"   ❌ Erreur: {str(e)}")

# 6. Résumé
print("\n" + "="*70)
print(" RÉSUMÉ")
print("="*70)

total_users = Utilisateur.objects.count()
total_ens = Enseignant.objects.count()
total_etu = Etudiant.objects.count()
total_notes = Note.objects.count()

if total_users >= 4 and total_ens >= 2 and total_etu >= 10 and total_notes >= 60:
    print("\n✅ SYSTÈME OPÉRATIONNEL")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("   1. Démarrer le backend: python manage.py runserver")
    print("   2. Ouvrir index.html dans le navigateur")
    print("   3. Se connecter avec admin@uan.bf / Admin2024!")
    print("   4. Tester les fonctionnalités:")
    print("      - Liste des étudiants avec boutons d'action")
    print("      - Liste des enseignants")
    print("      - Ajout d'enseignant")
    print("      - Recherche et filtres")
else:
    print("\n⚠️ DONNÉES INCOMPLÈTES")
    print("   → Exécuter: python creer_classe_l1_info.py")

print("\n" + "="*70 + "\n")
