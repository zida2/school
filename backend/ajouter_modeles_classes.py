#!/usr/bin/env python
"""
Script pour créer les migrations et appliquer les nouveaux modèles
"""

import os
import subprocess

print("🔄 AJOUT DES MODÈLES CLASSE, INSCRIPTION, ENSEIGNEMENTMATIERE")
print("=" * 60)

# 1. Créer les migrations
print("\n📝 1. Création des migrations...")
result = subprocess.run(['python', 'manage.py', 'makemigrations'], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(f"❌ Erreur: {result.stderr}")
    exit(1)

# 2. Appliquer les migrations
print("\n📊 2. Application des migrations...")
result = subprocess.run(['python', 'manage.py', 'migrate'], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(f"❌ Erreur: {result.stderr}")
    exit(1)

print("\n✅ Modèles ajoutés avec succès!")
print("\nVous pouvez maintenant exécuter: python reorganiser_structure_complete.py")
