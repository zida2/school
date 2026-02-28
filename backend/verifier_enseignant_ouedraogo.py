#!/usr/bin/env python
"""
Vérifier si l'utilisateur j.ouedraogo@uan.bf a un objet enseignant associé
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur, Enseignant

# Trouver l'utilisateur
try:
    user = Utilisateur.objects.get(email='j.ouedraogo@uan.bf')
    print(f"✅ Utilisateur trouvé: {user.prenom} {user.nom}")
    print(f"   ID: {user.id}")
    print(f"   Role: {user.role}")
    
    # Vérifier s'il a un enseignant associé
    if hasattr(user, 'enseignant'):
        print(f"✅ Enseignant associé trouvé: {user.enseignant}")
        print(f"   ID: {user.enseignant.id}")
        print(f"   Matricule: {user.enseignant.matricule}")
    else:
        print("❌ PAS d'enseignant associé!")
        
        # Chercher un enseignant avec le même email
        try:
            enseignant = Enseignant.objects.get(email='j.ouedraogo@uan.bf')
            print(f"\n⚠️  Enseignant trouvé avec le même email mais pas lié:")
            print(f"   ID: {enseignant.id}")
            print(f"   Matricule: {enseignant.matricule}")
            print(f"   Utilisateur: {enseignant.utilisateur}")
            
            # Lier l'enseignant à l'utilisateur
            print("\n🔧 Liaison de l'enseignant à l'utilisateur...")
            enseignant.utilisateur = user
            enseignant.save()
            print("✅ Liaison effectuée!")
            
        except Enseignant.DoesNotExist:
            print("❌ Aucun enseignant trouvé avec cet email")
            
except Utilisateur.DoesNotExist:
    print("❌ Utilisateur non trouvé")
