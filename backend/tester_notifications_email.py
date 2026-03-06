#!/usr/bin/env python
"""
Script pour tester le système de notifications email
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from api.models import Utilisateur, NotificationEmail, PreferenceNotification
from api.email_service import (
    creer_notification_email,
    notifier_nouvelle_note,
    notifier_nouvelle_evaluation,
    notifier_absence
)

def main():
    print("🧪 Test du système de notifications email\n")
    
    # 1. Vérifier les modèles
    print("1️⃣ Vérification des modèles...")
    nb_notifs = NotificationEmail.objects.count()
    nb_prefs = PreferenceNotification.objects.count()
    print(f"   ✅ {nb_notifs} notifications email dans la base")
    print(f"   ✅ {nb_prefs} préférences de notification dans la base\n")
    
    # 2. Créer des préférences par défaut pour tous les utilisateurs
    print("2️⃣ Création des préférences par défaut...")
    utilisateurs = Utilisateur.objects.all()
    created_count = 0
    for user in utilisateurs:
        pref, created = PreferenceNotification.objects.get_or_create(
            utilisateur=user,
            defaults={
                'activer_email': True,
                'notif_nouvelle_note': True,
                'notif_nouvelle_evaluation': True,
                'notif_absence': True,
                'notif_nouveau_support': True,
                'notif_emploi_modifie': True,
                'notif_demande_traitee': True,
                'notif_message_canal': True,
                'notif_annonce_officielle': True
            }
        )
        if created:
            created_count += 1
    print(f"   ✅ {created_count} nouvelles préférences créées")
    print(f"   ✅ Total: {PreferenceNotification.objects.count()} préférences\n")
    
    # 3. Tester la création d'une notification
    print("3️⃣ Test de création d'une notification...")
    try:
        admin = Utilisateur.objects.filter(role='admin').first()
        if admin:
            notif = creer_notification_email(
                destinataire=admin,
                sujet="Test de notification",
                contenu="Ceci est un test du système de notifications email.",
                type_notification='autre'
            )
            print(f"   ✅ Notification créée: ID={notif.id}")
            print(f"   📧 Destinataire: {notif.destinataire.email}")
            print(f"   📝 Sujet: {notif.sujet}\n")
        else:
            print("   ⚠️ Aucun admin trouvé pour le test\n")
    except Exception as e:
        print(f"   ❌ Erreur: {e}\n")
    
    # 4. Afficher les statistiques
    print("4️⃣ Statistiques:")
    print(f"   📊 Total notifications: {NotificationEmail.objects.count()}")
    print(f"   ✉️ Envoyées: {NotificationEmail.objects.filter(envoye=True).count()}")
    print(f"   ⏳ En attente: {NotificationEmail.objects.filter(envoye=False).count()}")
    print(f"   👥 Utilisateurs avec préférences: {PreferenceNotification.objects.count()}")
    
    # 5. Afficher les types de notifications disponibles
    print("\n5️⃣ Types de notifications disponibles:")
    types = [
        ('nouvelle_note', 'Nouvelle note publiée'),
        ('nouvelle_evaluation', 'Nouvelle évaluation disponible'),
        ('absence', 'Absence enregistrée'),
        ('nouveau_support', 'Nouveau support de cours'),
        ('emploi_modifie', 'Emploi du temps modifié'),
        ('demande_traitee', 'Demande administrative traitée'),
        ('message_canal', 'Nouveau message dans un canal'),
        ('annonce_officielle', 'Nouvelle annonce officielle'),
        ('autre', 'Autre notification')
    ]
    for code, libelle in types:
        print(f"   • {code}: {libelle}")
    
    print("\n✅ Test terminé!")
    print("\n📝 Prochaines étapes:")
    print("   1. Configurer les paramètres EMAIL dans .env")
    print("   2. Intégrer les appels de notification dans les ViewSets")
    print("   3. Créer l'interface frontend de préférences")

if __name__ == '__main__':
    main()
