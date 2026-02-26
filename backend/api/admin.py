from django.contrib import admin
from .models import (
    Utilisateur, Universite, AnneeAcademique, Filiere, Matiere,
    Enseignant, Etudiant, Note, Paiement, EmploiDuTemps,
    Presence, SupportCours, Notification, MembreBureau,
    Publication, Sondage, QuestionSondage, OptionQuestion,
    ReponseSondage, Evenement, InscriptionEvenement,
    MessageBureau, DemandeAdministrative, ObjetPerdu
)


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ['email', 'prenom', 'nom', 'role', 'is_active', 'date_creation']
    list_filter = ['role', 'is_active']
    search_fields = ['email', 'prenom', 'nom']


@admin.register(Universite)
class UniversiteAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'ville', 'licence', 'statut']
    list_filter = ['licence', 'statut']
    search_fields = ['code', 'nom']


@admin.register(AnneeAcademique)
class AnneeAcademiqueAdmin(admin.ModelAdmin):
    list_display = ['universite', 'libelle', 'debut', 'fin', 'active']
    list_filter = ['active', 'universite']


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'niveau', 'universite', 'actif']
    list_filter = ['niveau', 'actif', 'universite']
    search_fields = ['code', 'nom']


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'filiere', 'enseignant', 'semestre', 'coefficient']
    list_filter = ['semestre', 'filiere']
    search_fields = ['code', 'nom']


@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'prenom', 'nom', 'email', 'grade', 'statut', 'universite']
    list_filter = ['grade', 'statut', 'universite']
    search_fields = ['matricule', 'prenom', 'nom', 'email']


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'prenom', 'nom', 'filiere', 'niveau', 'statut', 'solde_du']
    list_filter = ['statut', 'filiere', 'niveau', 'universite']
    search_fields = ['matricule', 'prenom', 'nom', 'email']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'matiere', 'note_cc', 'note_examen', 'publie']
    list_filter = ['publie', 'matiere__semestre']
    search_fields = ['etudiant__matricule', 'etudiant__nom']


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['numero_recu', 'etudiant', 'montant', 'mode', 'type_paiement', 'statut', 'date_paiement']
    list_filter = ['statut', 'mode', 'type_paiement']
    search_fields = ['numero_recu', 'etudiant__matricule']


@admin.register(EmploiDuTemps)
class EmploiDuTempsAdmin(admin.ModelAdmin):
    list_display = ['matiere', 'jour', 'heure_debut', 'heure_fin', 'salle']
    list_filter = ['jour', 'matiere__filiere']


@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'emploi', 'date_cours', 'present', 'justifie']
    list_filter = ['present', 'date_cours']


@admin.register(SupportCours)
class SupportCoursAdmin(admin.ModelAdmin):
    list_display = ['titre', 'matiere', 'enseignant', 'type_support', 'visible', 'date_depot']
    list_filter = ['type_support', 'visible']
    search_fields = ['titre']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'destinataire', 'type_notif', 'lue', 'date_creation']
    list_filter = ['type_notif', 'lue']



# ===== BUREAU EXÉCUTIF =====
@admin.register(MembreBureau)
class MembreBureauAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'poste', 'date_debut_mandat', 'date_fin_mandat', 'actif']
    list_filter = ['poste', 'actif']
    search_fields = ['utilisateur__prenom', 'utilisateur__nom']


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'statut', 'auteur', 'date_publication', 'vues', 'epingle']
    list_filter = ['categorie', 'statut', 'epingle']
    search_fields = ['titre', 'contenu']


@admin.register(Sondage)
class SondageAdmin(admin.ModelAdmin):
    list_display = ['titre', 'createur', 'date_debut', 'date_fin', 'statut', 'anonyme']
    list_filter = ['statut', 'anonyme']
    search_fields = ['titre', 'description']


@admin.register(QuestionSondage)
class QuestionSondageAdmin(admin.ModelAdmin):
    list_display = ['sondage', 'texte', 'type_question', 'ordre', 'obligatoire']
    list_filter = ['type_question', 'obligatoire']


@admin.register(OptionQuestion)
class OptionQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'texte', 'ordre']


@admin.register(ReponseSondage)
class ReponseSondageAdmin(admin.ModelAdmin):
    list_display = ['sondage', 'question', 'etudiant', 'date_reponse']
    list_filter = ['sondage', 'date_reponse']


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_evenement', 'organisateur', 'date_debut', 'lieu', 'statut', 'capacite_max']
    list_filter = ['type_evenement', 'statut']
    search_fields = ['titre', 'description', 'lieu']


@admin.register(InscriptionEvenement)
class InscriptionEvenementAdmin(admin.ModelAdmin):
    list_display = ['evenement', 'etudiant', 'statut', 'date_inscription', 'present']
    list_filter = ['statut', 'present']


@admin.register(MessageBureau)
class MessageBureauAdmin(admin.ModelAdmin):
    list_display = ['expediteur', 'destinataire', 'sujet', 'groupe', 'date_envoi', 'lu']
    list_filter = ['groupe', 'lu', 'date_envoi']


@admin.register(DemandeAdministrative)
class DemandeAdministrativeAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'type_demande', 'objet', 'statut', 'date_demande', 'traite_par']
    list_filter = ['type_demande', 'statut']
    search_fields = ['etudiant__matricule', 'objet']


@admin.register(ObjetPerdu)
class ObjetPerduAdmin(admin.ModelAdmin):
    list_display = ['nom_objet', 'type_declaration', 'declarant', 'lieu', 'date_perte', 'statut']
    list_filter = ['type_declaration', 'statut']
    search_fields = ['nom_objet', 'description', 'lieu']
