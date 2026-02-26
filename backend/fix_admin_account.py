#!/usr/bin/env python
"""
Script pour vérifier et corriger le compte admin
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur

def fix_admin_account():
    print("=" * 60)
    print("🔧 VÉRIFICATION ET CORRECTION DU COMPTE ADMIN")
    print("=" * 60)
    print()
    
    try:
        # Chercher le compte admin
        admin = Utilisateur.objects.get(email='admin@uan.bf')
        print(f"✅ Compte admin trouvé: {admin.nom} {admin.prenom}")
        print(f"   Email: {admin.email}")
        print(f"   Rôle: {admin.role}")
        print(f"   Actif: {admin.is_active}")
        print()
        
        # Vérifier le mot de passe
        print("🔍 Vérification du mot de passe...")
        if admin.check_password('admin123'):
            print("✅ Le mot de passe 'admin123' fonctionne correctement!")
            print()
            print("=" * 60)
            print("✅ COMPTE ADMIN OK - AUCUNE CORRECTION NÉCESSAIRE")
            print("=" * 60)
            return True
        else:
            print("❌ Le mot de passe 'admin123' ne fonctionne pas!")
            print()
            print("🔧 Réinitialisation du mot de passe...")
            admin.set_password('admin123')
            admin.save()
            print("✅ Mot de passe réinitialisé à 'admin123'")
            print()
            
            # Vérifier à nouveau
            admin.refresh_from_db()
            if admin.check_password('admin123'):
                print("✅ Vérification: Le mot de passe fonctionne maintenant!")
                print()
                print("=" * 60)
                print("✅ COMPTE ADMIN CORRIGÉ AVEC SUCCÈS")
                print("=" * 60)
                return True
            else:
                print("❌ Erreur: Le mot de passe ne fonctionne toujours pas!")
                return False
                
    except Utilisateur.DoesNotExist:
        print("❌ Compte admin introuvable!")
        print()
        print("🔧 Création du compte admin...")
        
        admin = Utilisateur.objects.create(
            email='admin@uan.bf',
            nom='Administrateur',
            prenom='UAN',
            role='admin',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        admin.set_password('admin123')
        admin.save()
        
        print("✅ Compte admin créé avec succès!")
        print(f"   Email: admin@uan.bf")
        print(f"   Password: admin123")
        print()
        print("=" * 60)
        print("✅ COMPTE ADMIN CRÉÉ AVEC SUCCÈS")
        print("=" * 60)
        return True
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print()
    success = fix_admin_account()
    print()
    
    if success:
        print("🎉 Vous pouvez maintenant vous connecter avec:")
        print("   Email: admin@uan.bf")
        print("   Password: admin123")
    else:
        print("⚠️ Veuillez vérifier les erreurs ci-dessus")
    print()
