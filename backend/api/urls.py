from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import (
    LoginView, LogoutView, MeView, ChangePasswordView,
    DashboardAdminView, DashboardProfView, DashboardEtudiantView,
    UniversiteViewSet, AnneeAcademiqueViewSet, FiliereViewSet,
    MatiereViewSet, EnseignantViewSet, EtudiantViewSet, NoteViewSet,
    PaiementViewSet, EmploiDuTempsViewSet, PresenceViewSet,
    SupportCoursViewSet, NotificationViewSet, ReclamationNoteViewSet,
    EvaluationViewSet, NoteEvaluationViewSet,
    MembreBureauViewSet, PublicationViewSet, SondageViewSet,
    QuestionSondageViewSet, OptionQuestionViewSet, ReponseSondageViewSet,
    EvenementViewSet, InscriptionEvenementViewSet, MessageBureauViewSet,
    DemandeAdministrativeViewSet, ObjetPerduViewSet, DashboardBureauView
)

router = DefaultRouter()
router.register(r'universites', UniversiteViewSet, basename='universite')
router.register(r'annees', AnneeAcademiqueViewSet, basename='annee')
router.register(r'filieres', FiliereViewSet, basename='filiere')
router.register(r'matieres', MatiereViewSet, basename='matiere')
router.register(r'enseignants', EnseignantViewSet, basename='enseignant')
router.register(r'etudiants', EtudiantViewSet, basename='etudiant')
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'reclamations', ReclamationNoteViewSet, basename='reclamation')
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')
router.register(r'notes-evaluations', NoteEvaluationViewSet, basename='note-evaluation')
router.register(r'paiements', PaiementViewSet, basename='paiement')
router.register(r'emplois-du-temps', EmploiDuTempsViewSet, basename='emploi')
router.register(r'presences', PresenceViewSet, basename='presence')
router.register(r'supports', SupportCoursViewSet, basename='support')
router.register(r'notifications', NotificationViewSet, basename='notification')
# Bureau Exécutif
router.register(r'membres-bureau', MembreBureauViewSet, basename='membre-bureau')
router.register(r'publications', PublicationViewSet, basename='publication')
router.register(r'sondages', SondageViewSet, basename='sondage')
router.register(r'questions-sondage', QuestionSondageViewSet, basename='question-sondage')
router.register(r'options-question', OptionQuestionViewSet, basename='option-question')
router.register(r'reponses-sondage', ReponseSondageViewSet, basename='reponse-sondage')
router.register(r'evenements', EvenementViewSet, basename='evenement')
router.register(r'inscriptions-evenement', InscriptionEvenementViewSet, basename='inscription-evenement')
router.register(r'messages-bureau', MessageBureauViewSet, basename='message-bureau')
router.register(r'demandes-administratives', DemandeAdministrativeViewSet, basename='demande-administrative')
router.register(r'objets-perdus', ObjetPerduViewSet, basename='objet-perdu')

urlpatterns = [
    # Auth
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),

    # Dashboards
    path('dashboard/admin/', DashboardAdminView.as_view(), name='dashboard_admin'),
    path('dashboard/prof/', DashboardProfView.as_view(), name='dashboard_prof'),
    path('dashboard/etudiant/', DashboardEtudiantView.as_view(), name='dashboard_etudiant'),
    path('dashboard/bureau/', DashboardBureauView.as_view(), name='dashboard_bureau'),

    # Resources
    path('', include(router.urls)),
]
