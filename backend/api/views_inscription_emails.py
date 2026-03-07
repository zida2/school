"""
Fonctions d'envoi d'emails pour les inscriptions
"""
from .email_service import envoyer_notification_immediate
from .models import Utilisateur


def envoyer_email_validation_communication(demande, utilisateur, password):
    """Envoyer email de validation pour le service Communication"""
    try:
        sujet = "Accès Service Communication - UniERP"
        contenu = f"""Bonjour {demande.prenom} {demande.nom},

Votre demande d'accès au Service Communication a été validée !

Voici vos identifiants de connexion :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email : {demande.email}
🔑 Mot de passe : {password}
📢 Service : Communication
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANT : Veuillez changer votre mot de passe lors de votre première connexion.

Vous pouvez vous connecter à votre espace :
👉 https://school-wheat-six.vercel.app/connexion-communication.html

Bienvenue dans l'équipe !

Cordialement,
L'équipe UniERP BF"""
        
        envoyer_notification_immediate(
            destinataire=utilisateur,
            type_notification='inscription',
            sujet=sujet,
            contenu=contenu,
            lien='/connexion-communication.html'
        )
        return True
    except Exception as e:
        print(f"Erreur envoi email communication: {e}")
        return False


def envoyer_email_validation_academique(demande, utilisateur, password):
    """Envoyer email de validation pour le service Académique"""
    try:
        sujet = "Accès Service Académique - UniERP"
        contenu = f"""Bonjour {demande.prenom} {demande.nom},

Votre demande d'accès au Service Académique a été validée !

Voici vos identifiants de connexion :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email : {demande.email}
🔑 Mot de passe : {password}
📚 Service : Académique
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANT : Veuillez changer votre mot de passe lors de votre première connexion.

Vous pouvez vous connecter à votre espace :
👉 https://school-wheat-six.vercel.app/connexion-academique.html

Bienvenue dans l'équipe !

Cordialement,
L'équipe UniERP BF"""
        
        envoyer_notification_immediate(
            destinataire=utilisateur,
            type_notification='inscription',
            sujet=sujet,
            contenu=contenu,
            lien='/connexion-academique.html'
        )
        return True
    except Exception as e:
        print(f"Erreur envoi email académique: {e}")
        return False


def envoyer_email_validation_comptabilite(demande, utilisateur, password):
    """Envoyer email de validation pour le service Comptabilité"""
    try:
        sujet = "Accès Service Comptabilité - UniERP"
        contenu = f"""Bonjour {demande.prenom} {demande.nom},

Votre demande d'accès au Service Comptabilité a été validée !

Voici vos identifiants de connexion :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email : {demande.email}
🔑 Mot de passe : {password}
💰 Service : Comptabilité
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANT : Veuillez changer votre mot de passe lors de votre première connexion.

Vous pouvez vous connecter à votre espace :
👉 https://school-wheat-six.vercel.app/connexion-comptabilite.html

Bienvenue dans l'équipe !

Cordialement,
L'équipe UniERP BF"""
        
        envoyer_notification_immediate(
            destinataire=utilisateur,
            type_notification='inscription',
            sujet=sujet,
            contenu=contenu,
            lien='/connexion-comptabilite.html'
        )
        return True
    except Exception as e:
        print(f"Erreur envoi email comptabilité: {e}")
        return False


def envoyer_email_rejet_service(demande, service_nom, commentaire=''):
    """Envoyer email de rejet pour un service administratif"""
    try:
        sujet = f"Demande d'accès {service_nom} - Statut"
        contenu = f"""Bonjour {demande.prenom} {demande.nom},

Nous avons examiné votre demande d'accès au Service {service_nom}.

Malheureusement, nous ne pouvons pas donner suite à votre demande pour le moment.

{f"Motif : {commentaire}" if commentaire else ""}

Pour plus d'informations, vous pouvez contacter l'administration.

Cordialement,
L'équipe UniERP BF"""
        
        # Créer ou récupérer un utilisateur temporaire pour l'email
        try:
            utilisateur_temp = Utilisateur.objects.get(email=demande.email)
        except Utilisateur.DoesNotExist:
            utilisateur_temp = Utilisateur(
                email=demande.email,
                prenom=demande.prenom,
                nom=demande.nom,
                role='communication',  # Role par défaut
                is_active=False
            )
            utilisateur_temp.save()
        
        envoyer_notification_immediate(
            destinataire=utilisateur_temp,
            type_notification='inscription',
            sujet=sujet,
            contenu=contenu
        )
        return True
    except Exception as e:
        print(f"Erreur envoi email rejet {service_nom}: {e}")
        return False
