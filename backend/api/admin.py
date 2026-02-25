from django.contrib import admin
from .models import (
    Utilisateur, Universite, AnneeAcademique, Filiere, Matiere,
    Enseignant, Etudiant, Note, Paiement, EmploiDuTemps,
    Presence, SupportCours, Notification
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
