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
    SupportCoursViewSet, NotificationViewSet,
    EvaluationViewSet, NoteEvaluationViewSet,
)

router = DefaultRouter()
router.register(r'universites', UniversiteViewSet, basename='universite')
router.register(r'annees', AnneeAcademiqueViewSet, basename='annee')
router.register(r'filieres', FiliereViewSet, basename='filiere')
router.register(r'matieres', MatiereViewSet, basename='matiere')
router.register(r'enseignants', EnseignantViewSet, basename='enseignant')
router.register(r'etudiants', EtudiantViewSet, basename='etudiant')
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')
router.register(r'notes-evaluations', NoteEvaluationViewSet, basename='note-evaluation')
router.register(r'paiements', PaiementViewSet, basename='paiement')
router.register(r'emplois-du-temps', EmploiDuTempsViewSet, basename='emploi')
router.register(r'presences', PresenceViewSet, basename='presence')
router.register(r'supports', SupportCoursViewSet, basename='support')
router.register(r'notifications', NotificationViewSet, basename='notification')

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

    # Réclamations notes
    path('reclamations/', views.reclamations_list, name='reclamations-list'),
    path('reclamations/<int:pk>/', views.reclamation_detail, name='reclamation-detail'),

    # Resources
    path('', include(router.urls)),
]
