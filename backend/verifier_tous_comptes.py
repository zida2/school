#!/usr/bin/env python
"""
Script pour vérifier tous les comptes de test
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur

def verifier_tous_comptes():
    print("=" * 60)
    print("🔍 VÉRIFICATION DE TOUS LES COMPTES DE TEST")
    print("=" * 60)
    print()
    
    comptes = [
        ('Étudiant', 'm.diallo@etu.bf', 'etudiant123'),
        ('Bureau', 'bureau@uan.bf', 'bureau123'),
        ('Enseignant', 'j.ouedraogo@uan.bf', 'enseignant123'),
        ('Admin', 'admin@uan.bf', 'admin123'),
    ]
    
    tous_ok = True
    
    for role, email, password in comptes:
        print(f"📋 {role}: {email}")
        try:
            user = Utilisateur.objects.get(email=email)
            print(f"   ✅ Compte trouvé: {user.nom} {user.prenom}")
            print(f"   Rôle: {user.role}")
            print(f"   Actif: {user.is_active}")
            
            # Vérifier le mot de passe
            if user.check_password(password):
                print(f"   ✅ Mot de passe '{password}' OK")
            else:
                print(f"   ❌ Mot de passe '{password}' incorrect!")
                print(f"   🔧 Réinitialisation...")
                user.set_password(password)
                user.save()
                print(f"   ✅ Mot de passe réinitialisé")
                tous_ok = False
                
        except Utilisateur.DoesNotExist:
            print(f"   ❌ Compte introuvable!")
            tous_ok = False
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            tous_ok = False
        
        print()
    
    print("=" * 60)
    if tous_ok:
        print("✅ TOUS LES COMPTES SONT OK")
    else:
        print("⚠️ CERTAINS COMPTES ONT ÉTÉ CORRIGÉS")
    print("=" * 60)
    print()
    
    return tous_ok

if __name__ == '__main__':
    print()
    verifier_tous_comptes()
    
    print("📋 COMPTES DE TEST DISPONIBLES:")
    print()
    print("👨‍🎓 Étudiant:")
    print("   Email: m.diallo@etu.bf")
    print("   Password: etudiant123")
    print()
    print("🏛️ Bureau Exécutif:")
    print("   Email: bureau@uan.bf")
    print("   Password: bureau123")
    print()
    print("👨‍🏫 Enseignant:")
    print("   Email: j.ouedraogo@uan.bf")
    print("   Password: enseignant123")
    print()
    print("👔 Administrateur:")
    print("   Email: admin@uan.bf")
    print("   Password: admin123")
    print()
