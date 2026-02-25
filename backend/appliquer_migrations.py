"""
Script pour appliquer les migrations du modèle ReclamationNote
Exécuter avec : python appliquer_migrations.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    django.setup()
    
    from django.core.management import call_command
    
    print("="*60)
    print("🔄 Application des migrations")
    print("="*60)
    
    print("\n📦 Création des migrations...")
    call_command('makemigrations', '--no-input')
    
    print("\n📦 Application des migrations...")
    call_command('migrate', '--no-input')
    
    print("\n" + "="*60)
    print("✅ Migrations appliquées avec succès!")
    print("="*60)
    print("\n🚀 Vous pouvez maintenant démarrer le serveur:")
    print("   python manage.py runserver")
    print("="*60)

if __name__ == '__main__':
    main()
