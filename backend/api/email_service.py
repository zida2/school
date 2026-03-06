"""
Service d'envoi de notifications par email
"""
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import NotificationEmail, PreferenceNotification


def creer_notification_email(destinataire, type_notification, sujet, contenu, lien=''):
    """
    Créer une notification email
    """
    notification = NotificationEmail.objects.create(
        destinataire=destinataire,
        type_notification=type_notification,
        sujet=sujet,
        contenu=contenu,
        lien=lien
    )
    return notification


def envoyer_notification_email(notification):
    """
    Envoyer une notification email
    """
    try:
        # Vérifier les préférences de l'utilisateur
        try:
            prefs = notification.destinataire.preferences_notification
            if not prefs.activer_emails:
                notification.erreur = "Emails désactivés par l'utilisateur"
                notification.save()
                return False
            
            # Vérifier si ce type de notification est activé
            type_field = notification.type_notification
            if hasattr(prefs, type_field) and not getattr(prefs, type_field):
                notification.erreur = f"Type de notification {type_field} désactivé"
                notification.save()
                return False
                
        except PreferenceNotification.DoesNotExist:
            # Créer les préférences par défaut
            PreferenceNotification.objects.create(utilisateur=notification.destinataire)
        
        # Construire le message
        message = f"{notification.contenu}\n\n"
        if notification.lien:
            frontend_url = getattr(settings, 'FRONTEND_URL', 'https://school-wheat-six.vercel.app')
            message += f"Lien: {frontend_url}{notification.lien}\n\n"
        message += "---\nCeci est un email automatique de l'UAN, merci de ne pas répondre."
        
        # Envoyer l'email
        send_mail(
            subject=f"[UAN] {notification.sujet}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.destinataire.email],
            fail_silently=False,
        )
        
        # Marquer comme envoyé
        notification.envoye = True
        notification.date_envoi = timezone.now()
        notification.save()
        
        return True
        
    except Exception as e:
        notification.erreur = str(e)
        notification.save()
        return False


def envoyer_notification_immediate(destinataire, type_notification, sujet, contenu, lien=''):
    """
    Créer et envoyer immédiatement une notification
    """
    notification = creer_notification_email(destinataire, type_notification, sujet, contenu, lien)
    return envoyer_notification_email(notification)


def envoyer_notifications_en_attente():
    """
    Envoyer toutes les notifications en attente
    Peut être appelé par un cron job
    """
    notifications = NotificationEmail.objects.filter(envoye=False, erreur='')
    count_success = 0
    count_error = 0
    
    for notification in notifications:
        if envoyer_notification_email(notification):
            count_success += 1
        else:
            count_error += 1
    
    return count_success, count_error


# ===== FONCTIONS SPÉCIFIQUES =====

def notifier_nouvelle_note(etudiant, note):
    """
    Notifier un étudiant qu'une nouvelle note a été publiée
    """
    sujet = f"Nouvelle note - {note.matiere.nom}"
    contenu = f"""Bonjour {etudiant.prenom},

Une nouvelle note a été publiée pour la matière {note.matiere.nom}.

Note: {note.valeur}/{note.note_sur}
Type: {note.get_type_note_display()}
Semestre: {note.semestre}

Connectez-vous pour voir les détails.
"""
    lien = f"/dashboard-etudiant#notes"
    
    return envoyer_notification_immediate(
        etudiant.utilisateur,
        'nouvelle_note',
        sujet,
        contenu,
        lien
    )


def notifier_nouvelle_evaluation(etudiants, evaluation):
    """
    Notifier les étudiants d'une nouvelle évaluation
    """
    sujet = f"Nouvelle évaluation - {evaluation.matiere.nom}"
    contenu = f"""Bonjour,

Une nouvelle évaluation a été programmée:

Matière: {evaluation.matiere.nom}
Titre: {evaluation.titre}
Date: {evaluation.date_evaluation.strftime('%d/%m/%Y')}
Durée: {evaluation.duree} minutes
Salle: {evaluation.salle}

Bonne préparation!
"""
    lien = f"/dashboard-etudiant#evaluations"
    
    results = []
    for etudiant in etudiants:
        result = envoyer_notification_immediate(
            etudiant.utilisateur,
            'nouvelle_evaluation',
            sujet,
            contenu,
            lien
        )
        results.append(result)
    
    return results


def notifier_absence(etudiant, presence):
    """
    Notifier un étudiant d'une absence signalée
    """
    sujet = f"Absence signalée - {presence.emploi.matiere.nom}"
    contenu = f"""Bonjour {etudiant.prenom},

Une absence a été signalée pour le cours de {presence.emploi.matiere.nom}.

Date: {presence.date_cours.strftime('%d/%m/%Y')}
Justifiée: {'Oui' if presence.justifie else 'Non'}

Si cette absence est justifiée, veuillez fournir un justificatif.
"""
    lien = f"/dashboard-etudiant#absences"
    
    return envoyer_notification_immediate(
        etudiant.utilisateur,
        'absence_signale',
        sujet,
        contenu,
        lien
    )


def notifier_nouveau_support(etudiants, support):
    """
    Notifier les étudiants d'un nouveau support de cours
    """
    sujet = f"Nouveau support - {support.matiere.nom}"
    contenu = f"""Bonjour,

Un nouveau support de cours a été ajouté:

Matière: {support.matiere.nom}
Titre: {support.titre}
Type: {support.get_type_support_display()}

Connectez-vous pour le télécharger.
"""
    lien = f"/dashboard-etudiant#supports"
    
    results = []
    for etudiant in etudiants:
        result = envoyer_notification_immediate(
            etudiant.utilisateur,
            'support_cours',
            sujet,
            contenu,
            lien
        )
        results.append(result)
    
    return results


def notifier_demande_traitee(demande):
    """
    Notifier un étudiant que sa demande a été traitée
    """
    sujet = f"Demande traitée - {demande.get_type_demande_display()}"
    contenu = f"""Bonjour {demande.etudiant.prenom},

Votre demande administrative a été traitée.

Type: {demande.get_type_demande_display()}
Objet: {demande.objet}
Statut: {demande.get_statut_display()}

{f"Commentaire: {demande.commentaire_admin}" if demande.commentaire_admin else ""}

Connectez-vous pour voir les détails.
"""
    lien = f"/dashboard-etudiant#demandes"
    
    return envoyer_notification_immediate(
        demande.etudiant.utilisateur,
        'demande_traitee',
        sujet,
        contenu,
        lien
    )


def notifier_message_canal(utilisateurs, message):
    """
    Notifier les utilisateurs d'un nouveau message dans un canal
    """
    sujet = f"Nouveau message - {message.canal.nom}"
    contenu = f"""Bonjour,

Un nouveau message a été publié dans le canal {message.canal.nom}:

De: {message.expediteur.get_full_name()}
Message: {message.contenu[:200]}{'...' if len(message.contenu) > 200 else ''}

Connectez-vous pour voir le message complet.
"""
    lien = f"/dashboard#communication"
    
    results = []
    for utilisateur in utilisateurs:
        # Ne pas notifier l'expéditeur
        if utilisateur.id != message.expediteur.id:
            result = envoyer_notification_immediate(
                utilisateur,
                'message_canal',
                sujet,
                contenu,
                lien
            )
            results.append(result)
    
    return results


def notifier_annonce_officielle(utilisateurs, message):
    """
    Notifier tous les utilisateurs d'une annonce officielle
    """
    sujet = f"Annonce officielle - {message.canal.nom}"
    contenu = f"""Bonjour,

Une annonce officielle a été publiée:

{message.contenu}

Connectez-vous pour plus d'informations.
"""
    lien = f"/dashboard#communication"
    
    results = []
    for utilisateur in utilisateurs:
        result = envoyer_notification_immediate(
            utilisateur,
            'annonce_officielle',
            sujet,
            contenu,
            lien
        )
        results.append(result)
    
    return results
