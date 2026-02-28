#!/usr/bin/env python
"""
Script pour créer les canaux de communication par défaut
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Canal

def creer_canaux():
    print("🔧 Création des canaux de communication...")
    
    canaux_data = [
        {
            'nom': 'Annonces Officielles',
            'description': 'Canal officiel pour les annonces de l\'administration',
            'type_canal': 'officiel',
            'actif': True
        },
        {
            'nom': 'Informations Académiques',
            'description': 'Informations sur les cours, examens et emplois du temps',
            'type_canal': 'officiel',
            'actif': True
        },
        {
            'nom': 'Discussion Générale',
            'description': 'Canal de discussion pour tous les étudiants',
            'type_canal': 'etudiant',
            'actif': True
        },
        {
            'nom': 'Entraide Étudiants',
            'description': 'Canal d\'entraide et de partage entre étudiants',
            'type_canal': 'etudiant',
            'actif': True
        },
    ]
    
    for data in canaux_data:
        canal, created = Canal.objects.get_or_create(
            nom=data['nom'],
            defaults=data
        )
        if created:
            print(f"  ✅ Canal créé: {canal.nom} ({canal.get_type_canal_display()})")
        else:
            print(f"  ⚠️  Canal existe déjà: {canal.nom}")
    
    print(f"\n📊 Total: {Canal.objects.count()} canaux")
    print("  - Canaux officiels:", Canal.objects.filter(type_canal='officiel').count())
    print("  - Canaux étudiants:", Canal.objects.filter(type_canal='etudiant').count())

if __name__ == '__main__':
    creer_canaux()
