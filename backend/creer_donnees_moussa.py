#!/usr/bin/env python
"""
Créer des données de test pour Moussa Diallo
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import (
    Etudiant, DemandeAdministrative, ObjetPerdu, Publication, Utilisateur
)

def main():
    print("🚀 Création des données pour Moussa Diallo...")
    
    # Récupérer Moussa Diallo
    etudiant = Etudiant.objects.filter(utilisateur__email='m.diallo@etu.bf').first()
    if not etudiant:
        print("❌ Étudiant m.diallo@etu.bf non trouvé")
        return
    
    print(f"✅ Étudiant: {etudiant.get_full_name()}")
    
    # 1. DEMANDES
    print("\n📨 Création de demandes...")
    demandes_data = [
        {
            'etudiant': etudiant,
            'type_demande': 'attestation',
            'objet': 'Demande d\'attestation de scolarité',
            'description': 'Je souhaite obtenir une attestation de scolarité pour ma demande de bourse.',
            'statut': 'en_attente'
        },
        {
            'etudiant': etudiant,
            'type_demande': 'releve',
            'objet': 'Demande de relevé de notes',
            'description': 'J\'ai besoin d\'un relevé de notes du semestre précédent pour mon dossier.',
            'statut': 'en_traitement'
        },
        {
            'etudiant': etudiant,
            'type_demande': 'certificat',
            'objet': 'Certificat de scolarité',
            'description': 'Certificat de scolarité pour l\'année en cours.',
            'statut': 'termine'
        }
    ]
    
    for data in demandes_data:
        demande, created = DemandeAdministrative.objects.get_or_create(
            etudiant=data['etudiant'],
            objet=data['objet'],
            defaults=data
        )
        if created:
            print(f"  ✅ Demande créée: {data['objet']}")
        else:
            print(f"  ⚠️  Demande existe déjà: {data['objet']}")
    
    # 2. OBJETS PERDUS
    print("\n🔍 Création d\'objets perdus...")
    objets_data = [
        {
            'declarant': etudiant.utilisateur,
            'type_declaration': 'perdu',
            'nom_objet': 'Calculatrice scientifique',
            'description': 'Calculatrice Casio FX-991 avec étui noir',
            'lieu': 'Salle de TD B12',
            'date_perte': (datetime.now() - timedelta(days=3)).date(),
            'contact': etudiant.utilisateur.email,
            'statut': 'actif'
        },
        {
            'declarant': etudiant.utilisateur,
            'type_declaration': 'trouve',
            'nom_objet': 'Stylo bleu',
            'description': 'Stylo bleu marque BIC',
            'lieu': 'Bibliothèque',
            'date_perte': (datetime.now() - timedelta(days=1)).date(),
            'contact': etudiant.utilisateur.email,
            'statut': 'actif'
        }
    ]
    
    for data in objets_data:
        objet, created = ObjetPerdu.objects.get_or_create(
            declarant=data['declarant'],
            nom_objet=data['nom_objet'],
            defaults=data
        )
        if created:
            print(f"  ✅ Objet créé: {data['nom_objet']}")
        else:
            print(f"  ⚠️  Objet existe déjà: {data['nom_objet']}")
    
    # 3. PUBLIER LES PUBLICATIONS
    print("\n📰 Publication des publications...")
    publications = Publication.objects.all()
    for pub in publications:
        if pub.statut != 'publie':
            pub.statut = 'publie'
            pub.date_publication = datetime.now()
            pub.save()
            print(f"  ✅ Publication publiée: {pub.titre}")
    
    print("\n✅ Données créées avec succès pour Moussa Diallo!")
    print("\nRésumé:")
    print(f"  - {DemandeAdministrative.objects.filter(etudiant=etudiant).count()} demandes")
    print(f"  - {ObjetPerdu.objects.filter(declarant=etudiant.utilisateur).count()} objets perdus")
    print(f"  - {Publication.objects.filter(statut='publie').count()} publications publiées")

if __name__ == '__main__':
    main()
