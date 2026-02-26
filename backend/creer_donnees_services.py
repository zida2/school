#!/usr/bin/env python
"""
Script pour créer des données de test pour les services étudiants
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import (
    Utilisateur, Etudiant, Enseignant, Note, Matiere,
    ReclamationNote, Publication, Sondage, QuestionSondage,
    OptionQuestion, DemandeAdministrative, ObjetPerdu,
    MembreBureau
)

def main():
    print("🚀 Création des données de test pour les services...")
    
    # Récupérer un étudiant
    try:
        etudiant = Etudiant.objects.first()
        if not etudiant:
            print("❌ Aucun étudiant trouvé")
            return
        print(f"✅ Étudiant: {etudiant.get_full_name()}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return
    
    # Récupérer une note pour les réclamations
    note = Note.objects.filter(etudiant=etudiant).first()
    
    # 1. RÉCLAMATIONS
    print("\n📢 Création de réclamations...")
    if note:
        reclamations_data = [
            {
                'note': note,
                'etudiant': etudiant,
                'type_probleme': 'note_incorrecte',
                'description': 'Ma note de CC est incorrecte. J\'ai obtenu 15/20 mais il est marqué 12/20.',
                'note_attendue': 'CC: 15/20',
                'statut': 'en_attente'
            },
            {
                'note': note,
                'etudiant': etudiant,
                'type_probleme': 'note_manquante',
                'description': 'Ma note d\'examen n\'a pas été saisie alors que j\'ai bien passé l\'examen.',
                'statut': 'en_cours'
            }
        ]
        
        for data in reclamations_data:
            reclamation, created = ReclamationNote.objects.get_or_create(
                note=data['note'],
                etudiant=data['etudiant'],
                type_probleme=data['type_probleme'],
                defaults=data
            )
            if created:
                print(f"  ✅ Réclamation créée: {data['type_probleme']}")
    else:
        print("  ⚠️ Aucune note trouvée pour créer des réclamations")
    
    # 2. PUBLICATIONS
    print("\n📰 Création de publications...")
    
    # Récupérer ou créer un membre du bureau
    bureau_user = Utilisateur.objects.filter(role='bureau_executif').first()
    if bureau_user and hasattr(bureau_user, 'membre_bureau'):
        auteur = bureau_user.membre_bureau
    else:
        print("  ⚠️ Aucun membre du bureau trouvé, création d'un membre...")
        bureau_user, _ = Utilisateur.objects.get_or_create(
            email='bureau@uan.bf',
            defaults={
                'role': 'bureau_executif',
                'is_active': True
            }
        )
        if not hasattr(bureau_user, 'membre_bureau'):
            auteur = MembreBureau.objects.create(
                utilisateur=bureau_user,
                nom='Bureau',
                prenom='Exécutif',
                poste='president',
                email='bureau@uan.bf'
            )
        else:
            auteur = bureau_user.membre_bureau
    
    publications_data = [
        {
            'titre': 'Rentrée académique 2024-2025',
            'contenu': 'La rentrée académique aura lieu le 15 septembre 2024. Tous les étudiants sont priés de se présenter à 8h pour la cérémonie d\'ouverture.',
            'auteur': bureau_user,
            'date_publication': datetime.now() - timedelta(days=5)
        },
        {
            'titre': 'Journée portes ouvertes',
            'contenu': 'L\'université organise une journée portes ouvertes le 20 octobre. Venez découvrir nos formations et rencontrer les enseignants.',
            'auteur': bureau_user,
            'date_publication': datetime.now() - timedelta(days=2)
        },
        {
            'titre': 'Examens du premier semestre',
            'contenu': 'Les examens du premier semestre se dérouleront du 15 au 25 janvier 2025. Le calendrier détaillé sera publié prochainement.',
            'auteur': bureau_user,
            'date_publication': datetime.now()
        }
    ]
    
    for data in publications_data:
        pub, created = Publication.objects.get_or_create(
            titre=data['titre'],
            defaults=data
        )
        if created:
            print(f"  ✅ Publication créée: {data['titre']}")
    
    # 3. SONDAGES
    print("\n📊 Création de sondages...")
    sondages_data = [
        {
            'titre': 'Satisfaction des cours',
            'description': 'Donnez votre avis sur la qualité des cours dispensés',
            'createur': bureau_user,
            'date_debut': datetime.now() - timedelta(days=3),
            'date_fin': datetime.now() + timedelta(days=7),
            'statut': 'actif'
        },
        {
            'titre': 'Choix de la destination du voyage d\'études',
            'description': 'Votez pour la destination du prochain voyage d\'études',
            'createur': bureau_user,
            'date_debut': datetime.now(),
            'date_fin': datetime.now() + timedelta(days=14),
            'statut': 'actif'
        }
    ]
    
    for data in sondages_data:
        sondage, created = Sondage.objects.get_or_create(
            titre=data['titre'],
            defaults=data
        )
        if created:
            print(f"  ✅ Sondage créé: {data['titre']}")
            
            # Ajouter des questions au sondage
            if 'Satisfaction' in data['titre']:
                question = QuestionSondage.objects.create(
                    sondage=sondage,
                    texte='Comment évaluez-vous la qualité des cours ?',
                    type_question='choix_unique',
                    ordre=1
                )
                for i, option in enumerate(['Excellent', 'Bien', 'Moyen', 'Insuffisant'], 1):
                    OptionQuestion.objects.create(
                        question=question,
                        texte=option,
                        ordre=i
                    )
    
    # 4. DEMANDES ADMINISTRATIVES
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
            'description': 'J\'ai besoin d\'un relevé de notes du semestre précédent.',
            'statut': 'termine'
        }
    ]
    
    for data in demandes_data:
        demande, created = DemandeAdministrative.objects.get_or_create(
            etudiant=data['etudiant'],
            type_demande=data['type_demande'],
            objet=data['objet'],
            defaults=data
        )
        if created:
            print(f"  ✅ Demande créée: {data['type_demande']}")
    
    # 5. OBJETS PERDUS
    print("\n🔍 Création d\'objets perdus...")
    objets_data = [
        {
            'declarant': etudiant.utilisateur,
            'type_declaration': 'perdu',
            'nom_objet': 'Téléphone Samsung Galaxy',
            'description': 'Téléphone noir avec coque bleue',
            'lieu': 'Amphithéâtre A',
            'date_perte': (datetime.now() - timedelta(days=2)).date(),
            'contact': etudiant.email,
            'statut': 'actif'
        },
        {
            'declarant': etudiant.utilisateur,
            'type_declaration': 'trouve',
            'nom_objet': 'Clés USB',
            'description': 'Clé USB rouge 32GB',
            'lieu': 'Bibliothèque',
            'date_perte': (datetime.now() - timedelta(days=1)).date(),
            'contact': etudiant.email,
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
    
    print("\n✅ Données de test créées avec succès!")
    print("\nVous pouvez maintenant tester les services dans l'espace étudiant:")
    print("  - Réclamations")
    print("  - Publications")
    print("  - Sondages")
    print("  - Demandes administratives")
    print("  - Objets perdus")

if __name__ == '__main__':
    main()
