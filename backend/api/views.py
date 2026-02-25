from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
import uuid

from .models import (
    Utilisateur, Universite, AnneeAcademique, Filiere, Matiere,
    Enseignant, Etudiant, Note, Paiement, EmploiDuTemps,
    Presence, SupportCours, Notification, ReclamationNote,
    Evaluation, NoteEvaluation
)
from .serializers import (
    LoginSerializer, UtilisateurSerializer, ChangePasswordSerializer,
    UniversiteSerializer, AnneeAcademiqueSerializer, FiliereSerializer,
    MatiereSerializer, EnseignantSerializer, EnseignantCreateSerializer,
    EtudiantSerializer, EtudiantCreateSerializer, NoteSerializer,
    PaiementSerializer, EmploiDuTempsSerializer, PresenceSerializer,
    SupportCoursSerializer, NotificationSerializer, ReclamationNoteSerializer,
    EvaluationSerializer, NoteEvaluationSerializer
)
from .permissions import IsSuperAdmin, IsAdminOrSuperAdmin, IsEnseignant, IsEtudiant


# ===== AUTH VIEWS =====
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Déconnexion réussie.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Token invalide.'}, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    def get(self, request):
        serializer = UtilisateurSerializer(request.user)
        data = serializer.data

        # Enrichir selon le rôle
        if request.user.role == 'etudiant':
            try:
                data['etudiant'] = EtudiantSerializer(request.user.etudiant).data
            except Etudiant.DoesNotExist:
                pass
        elif request.user.role == 'professeur':
            try:
                data['enseignant'] = EnseignantSerializer(request.user.enseignant).data
            except Enseignant.DoesNotExist:
                pass

        return Response(data)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'detail': 'Mot de passe modifié avec succès.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===== DASHBOARD =====
class DashboardAdminView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]

    def get(self, request):
        # Filtrer par université si admin
        if request.user.role == 'admin':
            try:
                univ = request.user.enseignant.universite
                etudiants_qs = Etudiant.objects.filter(universite=univ)
                enseignants_qs = Enseignant.objects.filter(universite=univ)
                paiements_qs = Paiement.objects.filter(etudiant__universite=univ)
            except:
                etudiants_qs = Etudiant.objects.none()
                enseignants_qs = Enseignant.objects.none()
                paiements_qs = Paiement.objects.none()
        else:
            etudiants_qs = Etudiant.objects.all()
            enseignants_qs = Enseignant.objects.all()
            paiements_qs = Paiement.objects.all()

        total_encaisse = paiements_qs.filter(statut='valide').aggregate(
            t=Sum('montant'))['t'] or 0
        total_impaye = etudiants_qs.aggregate(t=Sum('solde_du'))['t'] or 0

        return Response({
            'total_etudiants': etudiants_qs.count(),
            'total_enseignants': enseignants_qs.count(),
            'total_encaisse': int(total_encaisse),
            'total_impaye': int(total_impaye),
            'total_filieres': Filiere.objects.count(),
            'total_matieres': Matiere.objects.count(),
            'paiements_recents': PaiementSerializer(paiements_qs.order_by('-date_creation')[:10], many=True).data,
            'inscriptions_recentes': EtudiantSerializer(etudiants_qs.order_by('-date_inscription')[:10], many=True).data,
        })


class DashboardProfView(APIView):
    permission_classes = [IsEnseignant]

    def get(self, request):
        try:
            enseignant = request.user.enseignant
            matieres = enseignant.matieres.all()
            etudiants_ids = Etudiant.objects.filter(
                filiere__in=matieres.values('filiere')
            ).values_list('id', flat=True).distinct()

            return Response({
                'nb_matieres': matieres.count(),
                'nb_etudiants': len(etudiants_ids),
                'nb_notes_saisies': Note.objects.filter(
                    matiere__in=matieres, note_cc__isnull=False
                ).count(),
                'matieres': MatiereSerializer(matieres, many=True).data,
            })
        except Enseignant.DoesNotExist:
            return Response({'error': 'Profil enseignant non trouvé'}, status=404)


class DashboardEtudiantView(APIView):
    permission_classes = [IsEtudiant]

    def get(self, request):
        try:
            etudiant = request.user.etudiant
            notes = Note.objects.filter(etudiant=etudiant, publie=True)
            notes_s1 = notes.filter(matiere__semestre=1)
            notes_s2 = notes.filter(matiere__semestre=2)

            def calc_moy(qs):
                total_coef = 0
                total_points = 0
                for n in qs:
                    if n.moyenne is not None:
                        total_coef += n.matiere.coefficient
                        total_points += n.moyenne * n.matiere.coefficient
                return round(total_points / total_coef, 2) if total_coef > 0 else None

            return Response({
                'etudiant': EtudiantSerializer(etudiant).data,
                'notes_s1': NoteSerializer(notes_s1, many=True).data,
                'notes_s2': NoteSerializer(notes_s2, many=True).data,
                'moyenne_s1': calc_moy(notes_s1),
                'moyenne_s2': calc_moy(notes_s2),
                'paiements': PaiementSerializer(
                    etudiant.paiements.filter(statut='valide').order_by('-date_paiement'), many=True
                ).data,
            })
        except Etudiant.DoesNotExist:
            return Response({'error': 'Profil étudiant non trouvé'}, status=404)


# ===== UNIVERSITÉ =====
class UniversiteViewSet(viewsets.ModelViewSet):
    queryset = Universite.objects.all()
    serializer_class = UniversiteSerializer
    permission_classes = [IsSuperAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'code', 'ville']


# ===== ANNÉE ACADÉMIQUE =====
class AnneeAcademiqueViewSet(viewsets.ModelViewSet):
    queryset = AnneeAcademique.objects.all()
    serializer_class = AnneeAcademiqueSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    @action(detail=True, methods=['post'])
    def activer(self, request, pk=None):
        annee = self.get_object()
        AnneeAcademique.objects.filter(universite=annee.universite).update(active=False)
        annee.active = True
        annee.save()
        return Response({'detail': f'Année {annee.libelle} activée.'})


# ===== FILIÈRE =====
class FiliereViewSet(viewsets.ModelViewSet):
    queryset = Filiere.objects.all()
    serializer_class = FiliereSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'code']


# ===== MATIÈRE =====
class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.select_related('filiere', 'enseignant').all()
    serializer_class = MatiereSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'code']


# ===== ENSEIGNANT =====
class EnseignantViewSet(viewsets.ModelViewSet):
    queryset = Enseignant.objects.select_related('universite').all()
    serializer_class = EnseignantSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['prenom', 'nom', 'email', 'matricule']

    def get_serializer_class(self):
        if self.action == 'create':
            return EnseignantCreateSerializer
        return EnseignantSerializer

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        enseignant = self.get_object()
        if enseignant.utilisateur:
            enseignant.utilisateur.set_password('enseignant123')
            enseignant.utilisateur.save()
        return Response({'detail': 'Mot de passe réinitialisé : enseignant123'})


# ===== ÉTUDIANT =====
class EtudiantViewSet(viewsets.ModelViewSet):
    queryset = Etudiant.objects.select_related('filiere', 'universite', 'annee_academique').all()
    serializer_class = EtudiantSerializer
    permission_classes = [IsEnseignant]  # Enseignants peuvent voir les étudiants
    filter_backends = [filters.SearchFilter]
    search_fields = ['prenom', 'nom', 'email', 'matricule']

    def get_queryset(self):
        """Filtrer les étudiants selon le rôle de l'utilisateur"""
        user = self.request.user
        queryset = super().get_queryset()
        
        # Si enseignant, ne montrer que les étudiants de ses filières
        if user.role == 'professeur' and hasattr(user, 'enseignant'):
            # Récupérer les filières où l'enseignant enseigne
            matieres = user.enseignant.matieres.all()
            filieres_ids = matieres.values_list('filiere_id', flat=True).distinct()
            queryset = queryset.filter(filiere_id__in=filieres_ids)
        
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return EtudiantCreateSerializer
        return EtudiantSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        filiere = self.request.query_params.get('filiere')
        statut = self.request.query_params.get('statut')
        niveau = self.request.query_params.get('niveau')
        if filiere:
            qs = qs.filter(filiere_id=filiere)
        if statut:
            qs = qs.filter(statut=statut)
        if niveau:
            qs = qs.filter(niveau=niveau)
        return qs

    @action(detail=True, methods=['post'])
    def bloquer(self, request, pk=None):
        etudiant = self.get_object()
        etudiant.statut = 'bloque'
        etudiant.save()
        if etudiant.utilisateur:
            etudiant.utilisateur.is_active = False
            etudiant.utilisateur.save()
        return Response({'detail': f'Étudiant {etudiant.matricule} bloqué.'})

    @action(detail=True, methods=['post'])
    def debloquer(self, request, pk=None):
        etudiant = self.get_object()
        etudiant.statut = 'inscrit'
        etudiant.save()
        if etudiant.utilisateur:
            etudiant.utilisateur.is_active = True
            etudiant.utilisateur.save()
        return Response({'detail': f'Étudiant {etudiant.matricule} débloqué.'})

    @action(detail=True, methods=['get'])
    def bulletin(self, request, pk=None):
        etudiant = self.get_object()
        notes = Note.objects.filter(etudiant=etudiant, publie=True).select_related('matiere')
        notes_s1 = notes.filter(matiere__semestre=1)
        notes_s2 = notes.filter(matiere__semestre=2)

        def calc_moy(qs):
            total_coef = sum(n.matiere.coefficient for n in qs if n.moyenne is not None)
            total_pts = sum(n.moyenne * n.matiere.coefficient for n in qs if n.moyenne is not None)
            return round(total_pts / total_coef, 2) if total_coef else None

        m1, m2 = calc_moy(notes_s1), calc_moy(notes_s2)
        def mention(m):
            if m is None: return '—'
            if m >= 16: return 'Très Bien'
            if m >= 14: return 'Bien'
            if m >= 12: return 'Assez Bien'
            if m >= 10: return 'Passable'
            return 'Ajourné'

        return Response({
            'etudiant': EtudiantSerializer(etudiant).data,
            'notes_s1': NoteSerializer(notes_s1, many=True).data,
            'notes_s2': NoteSerializer(notes_s2, many=True).data,
            'moyenne_s1': m1,
            'moyenne_s2': m2,
            'mention_s1': mention(m1),
            'mention_s2': mention(m2),
        })

    @action(detail=True, methods=['get'])
    def paiements(self, request, pk=None):
        etudiant = self.get_object()
        pays = etudiant.paiements.all()
        return Response(PaiementSerializer(pays, many=True).data)


# ===== NOTE =====
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.select_related('etudiant', 'matiere').all()
    serializer_class = NoteSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrSuperAdmin() if self.action in ['destroy'] else IsEnseignant()]

    def get_queryset(self):
        qs = super().get_queryset()
        matiere = self.request.query_params.get('matiere')
        etudiant = self.request.query_params.get('etudiant')
        semestre = self.request.query_params.get('semestre')
        annee = self.request.query_params.get('annee_academique')
        filiere = self.request.query_params.get('filiere')

        if matiere: qs = qs.filter(matiere_id=matiere)
        if etudiant: qs = qs.filter(etudiant_id=etudiant)
        if semestre: qs = qs.filter(matiere__semestre=semestre)
        if annee: qs = qs.filter(annee_academique_id=annee)
        if filiere: qs = qs.filter(matiere__filiere_id=filiere)

        # Étudiant ne voit que ses propres notes publiées
        if self.request.user.role == 'etudiant':
            try:
                qs = qs.filter(etudiant=self.request.user.etudiant, publie=True)
            except: qs = qs.none()
        # Enseignant voit les notes de ses matières
        elif self.request.user.role == 'professeur':
            try:
                qs = qs.filter(matiere__enseignant=self.request.user.enseignant)
            except: qs = qs.none()

        return qs

    def perform_create(self, serializer):
        serializer.save(saisie_par=self.request.user)

    @action(detail=False, methods=['post'])
    def publier(self, request):
        """Publier les notes d'une matière et notifier les étudiants"""
        matiere_id = request.data.get('matiere_id')
        annee_id = request.data.get('annee_academique_id')
        
        notes = Note.objects.filter(
            matiere_id=matiere_id,
            annee_academique_id=annee_id,
            publie=False
        )
        
        count = 0
        for note in notes:
            note.publie = True
            note.statut = 'publie'
            note.save()
            count += 1
            
            # Créer notification pour l'étudiant
            if hasattr(note.etudiant, 'utilisateur') and note.etudiant.utilisateur:
                Notification.objects.create(
                    utilisateur=note.etudiant.utilisateur,
                    titre=f"Nouvelles notes - {note.matiere.nom}",
                    message=f"Vos notes pour {note.matiere.nom} sont maintenant disponibles. Veuillez les consulter et les confirmer.",
                    type='note',
                    lue=False
                )
        
        return Response({
            'detail': f'{count} note(s) publiée(s) et {count} notification(s) envoyée(s).'
        })
    
    @action(detail=True, methods=['post'])
    def confirmer(self, request, pk=None):
        """Confirmer une note (action étudiant)"""
        note = self.get_object()
        
        # Vérifier que c'est bien l'étudiant concerné
        if request.user.role == 'etudiant':
            if not hasattr(request.user, 'etudiant') or note.etudiant != request.user.etudiant:
                return Response(
                    {'error': 'Vous ne pouvez confirmer que vos propres notes'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        note.statut = 'confirme'
        note.save()
        
        return Response({'detail': 'Note confirmée avec succès'})
    
    @action(detail=True, methods=['post'])
    def reclamer(self, request, pk=None):
        """Créer une réclamation pour une note"""
        note = self.get_object()
        motif = request.data.get('motif', '')
        
        # Vérifier que c'est bien l'étudiant concerné
        if request.user.role == 'etudiant':
            if not hasattr(request.user, 'etudiant') or note.etudiant != request.user.etudiant:
                return Response(
                    {'error': 'Vous ne pouvez réclamer que vos propres notes'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Créer la réclamation
        reclamation = ReclamationNote.objects.create(
            note=note,
            etudiant=note.etudiant,
            motif=motif,
            statut='en_attente'
        )
        
        note.statut = 'reclame'
        note.save()
        
        # Notifier l'enseignant
        if note.matiere.enseignant and hasattr(note.matiere.enseignant, 'utilisateur'):
            Notification.objects.create(
                utilisateur=note.matiere.enseignant.utilisateur,
                titre=f"Réclamation de note - {note.etudiant.prenom} {note.etudiant.nom}",
                message=f"L'étudiant {note.etudiant.matricule} a réclamé sa note en {note.matiere.nom}",
                type='reclamation',
                lue=False
            )
        
        return Response({
            'detail': 'Réclamation enregistrée avec succès',
            'reclamation_id': reclamation.id
        })


# ===== PAIEMENT =====
class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.select_related('etudiant').all()
    serializer_class = PaiementSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['numero_recu', 'etudiant__matricule', 'etudiant__nom']

    def get_queryset(self):
        qs = super().get_queryset()
        etudiant = self.request.query_params.get('etudiant')
        annee = self.request.query_params.get('annee_academique')
        if etudiant: qs = qs.filter(etudiant_id=etudiant)
        if annee: qs = qs.filter(annee_academique_id=annee)
        return qs

    def perform_create(self, serializer):
        # Générer numéro de reçu auto
        recu = f"REC-{timezone.now().year}-{str(uuid.uuid4())[:6].upper()}"
        paiement = serializer.save(
            enregistre_par=self.request.user,
            numero_recu=recu
        )
        # Mettre à jour le solde
        etudiant = paiement.etudiant
        montant_paye_total = etudiant.paiements.filter(statut='valide').aggregate(
            t=Sum('montant'))['t'] or 0
        frais = etudiant.filiere.frais_inscription
        etudiant.solde_du = max(0, int(frais) - int(montant_paye_total))
        etudiant.save()


# ===== EMPLOI DU TEMPS =====
class EmploiDuTempsViewSet(viewsets.ModelViewSet):
    queryset = EmploiDuTemps.objects.select_related('matiere', 'matiere__filiere', 'matiere__enseignant').all()
    serializer_class = EmploiDuTempsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrSuperAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        filiere = self.request.query_params.get('filiere')
        enseignant = self.request.query_params.get('enseignant')
        annee = self.request.query_params.get('annee_academique')

        if filiere: qs = qs.filter(matiere__filiere_id=filiere)
        if enseignant: qs = qs.filter(matiere__enseignant_id=enseignant)
        if annee: qs = qs.filter(annee_academique_id=annee)

        # Étudiant voit seulement son programme
        if self.request.user.role == 'etudiant':
            try:
                qs = qs.filter(matiere__filiere=self.request.user.etudiant.filiere)
            except: qs = qs.none()
        # Enseignant voit seulement ses cours
        elif self.request.user.role == 'professeur':
            try:
                qs = qs.filter(matiere__enseignant=self.request.user.enseignant)
            except: qs = qs.none()

        return qs


# ===== PRÉSENCE =====
class PresenceViewSet(viewsets.ModelViewSet):
    queryset = Presence.objects.select_related('etudiant', 'emploi').all()
    serializer_class = PresenceSerializer
    permission_classes = [IsEnseignant]

    def get_queryset(self):
        qs = super().get_queryset()
        emploi = self.request.query_params.get('emploi')
        date = self.request.query_params.get('date_cours')
        if emploi: qs = qs.filter(emploi_id=emploi)
        if date: qs = qs.filter(date_cours=date)
        return qs

    def perform_create(self, serializer):
        serializer.save(enregistre_par=self.request.user)

    @action(detail=False, methods=['post'])
    def enregistrer_session(self, request):
        """Enregistrer la présence de tous les étudiants d'un cours d'un coup"""
        emploi_id = request.data.get('emploi_id')
        date_cours = request.data.get('date_cours')
        presences_data = request.data.get('presences', [])

        created = 0
        for p in presences_data:
            Presence.objects.update_or_create(
                etudiant_id=p['etudiant_id'],
                emploi_id=emploi_id,
                date_cours=date_cours,
                defaults={
                    'present': p.get('present', False),
                    'justifie': p.get('justifie', False),
                    'observation': p.get('observation', ''),
                    'enregistre_par': request.user,
                }
            )
            created += 1
        return Response({'detail': f'{created} présences enregistrées.'})


# ===== SUPPORT DE COURS =====
class SupportCoursViewSet(viewsets.ModelViewSet):
    queryset = SupportCours.objects.select_related('matiere', 'enseignant').all()
    serializer_class = SupportCoursSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEnseignant()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'etudiant':
            try:
                qs = qs.filter(matiere__filiere=self.request.user.etudiant.filiere, visible=True)
            except: qs = qs.none()
        elif self.request.user.role == 'professeur':
            try:
                qs = qs.filter(enseignant=self.request.user.enseignant)
            except: qs = qs.none()
        return qs


# ===== NOTIFICATION =====
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(destinataire=self.request.user)

    @action(detail=False, methods=['post'])
    def tout_lire(self, request):
        count = Notification.objects.filter(destinataire=request.user, lue=False).update(lue=True)
        return Response({'detail': f'{count} notification(s) marquée(s) comme lue(s).'})

    @action(detail=True, methods=['post'])
    def lire(self, request, pk=None):
        notif = self.get_object()
        notif.lue = True
        notif.save()
        return Response({'detail': 'Notification lue.'})


# ===== RÉCLAMATIONS NOTES =====
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reclamations_list(request):
    """Liste et création de réclamations de notes"""
    if request.method == 'GET':
        # Filtrer selon le rôle
        if request.user.role == 'etudiant':
            reclamations = ReclamationNote.objects.filter(etudiant=request.user.etudiant)
        elif request.user.role == 'professeur':
            # Réclamations pour les matières de l'enseignant
            reclamations = ReclamationNote.objects.filter(
                note__matiere__enseignant=request.user.enseignant
            )
        else:
            # Admin voit tout
            reclamations = ReclamationNote.objects.all()
        
        serializer = ReclamationNoteSerializer(reclamations, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Seuls les étudiants peuvent créer des réclamations
        if request.user.role != 'etudiant':
            return Response(
                {'error': 'Seuls les étudiants peuvent créer des réclamations'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ReclamationNoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def reclamation_detail(request, pk):
    """Détail, modification et suppression d'une réclamation"""
    try:
        reclamation = ReclamationNote.objects.get(pk=pk)
    except ReclamationNote.DoesNotExist:
        return Response({'error': 'Réclamation non trouvée'}, status=status.HTTP_404_NOT_FOUND)
    
    # Vérifier les permissions
    if request.user.role == 'etudiant' and reclamation.etudiant.utilisateur != request.user:
        return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = ReclamationNoteSerializer(reclamation)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Seuls les enseignants et admins peuvent modifier
        if request.user.role not in ['professeur', 'admin', 'superadmin']:
            return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ReclamationNoteSerializer(reclamation, data=request.data, partial=True)
        if serializer.is_valid():
            if 'statut' in request.data and request.data['statut'] != 'en_attente':
                reclamation.traite_par = request.user
                reclamation.date_traitement = timezone.now()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Seuls les étudiants peuvent supprimer leurs réclamations en attente
        if request.user.role == 'etudiant' and reclamation.statut == 'en_attente':
            reclamation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)


# ===== ÉVALUATION =====
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.select_related('matiere', 'annee_academique').all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsEnseignant]
    
    def get_queryset(self):
        qs = super().get_queryset()
        matiere = self.request.query_params.get('matiere')
        annee = self.request.query_params.get('annee_academique')
        categorie = self.request.query_params.get('categorie')
        
        if matiere: qs = qs.filter(matiere_id=matiere)
        if annee: qs = qs.filter(annee_academique_id=annee)
        if categorie: qs = qs.filter(categorie=categorie)
        
        # Enseignant ne voit que les évaluations de ses matières
        if self.request.user.role == 'professeur':
            try:
                qs = qs.filter(matiere__enseignant=self.request.user.enseignant)
            except: qs = qs.none()
        
        return qs
    
    @action(detail=True, methods=['post'])
    def generer_notes(self, request, pk=None):
        """Générer les notes vides pour tous les étudiants de la matière"""
        evaluation = self.get_object()
        etudiants = Etudiant.objects.filter(
            filiere=evaluation.matiere.filiere,
            annee_academique=evaluation.annee_academique
        )
        
        notes_creees = 0
        for etudiant in etudiants:
            note, created = NoteEvaluation.objects.get_or_create(
                evaluation=evaluation,
                etudiant=etudiant,
                defaults={'saisie_par': request.user}
            )
            if created:
                notes_creees += 1
        
        return Response({
            'message': f'{notes_creees} note(s) générée(s)',
            'total_etudiants': etudiants.count()
        })


# ===== NOTE D'ÉVALUATION =====
class NoteEvaluationViewSet(viewsets.ModelViewSet):
    queryset = NoteEvaluation.objects.select_related('evaluation', 'etudiant').all()
    serializer_class = NoteEvaluationSerializer
    permission_classes = [IsEnseignant]
    
    def get_queryset(self):
        qs = super().get_queryset()
        evaluation = self.request.query_params.get('evaluation')
        etudiant = self.request.query_params.get('etudiant')
        matiere = self.request.query_params.get('matiere')
        
        if evaluation: qs = qs.filter(evaluation_id=evaluation)
        if etudiant: qs = qs.filter(etudiant_id=etudiant)
        if matiere: qs = qs.filter(evaluation__matiere_id=matiere)
        
        # Enseignant ne voit que les notes de ses matières
        if self.request.user.role == 'professeur':
            try:
                qs = qs.filter(evaluation__matiere__enseignant=self.request.user.enseignant)
            except: qs = qs.none()
        
        # Étudiant voit ses propres notes
        elif self.request.user.role == 'etudiant':
            try:
                qs = qs.filter(etudiant=self.request.user.etudiant)
            except: qs = qs.none()
        
        return qs
