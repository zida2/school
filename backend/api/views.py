from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import update_session_auth_hash
from django.db import models
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
import uuid

from .models import (
    Utilisateur, Universite, AnneeAcademique, Filiere, Matiere,
    Enseignant, Etudiant, Note, Paiement, EmploiDuTemps,
    Presence, SupportCours, Notification, ReclamationNote,
    Evaluation, NoteEvaluation, MembreBureau, Publication,
    Sondage, QuestionSondage, OptionQuestion, ReponseSondage,
    Evenement, InscriptionEvenement, MessageBureau,
    DemandeAdministrative, ObjetPerdu, Classe, Inscription, EnseignementMatiere
)
from .serializers import (
    LoginSerializer, UtilisateurSerializer, ChangePasswordSerializer,
    UniversiteSerializer, AnneeAcademiqueSerializer, FiliereSerializer,
    MatiereSerializer, EnseignantSerializer, EnseignantCreateSerializer,
    EtudiantSerializer, EtudiantCreateSerializer, NoteSerializer,
    PaiementSerializer, EmploiDuTempsSerializer, PresenceSerializer,
    SupportCoursSerializer, NotificationSerializer, ReclamationNoteSerializer,
    EvaluationSerializer, NoteEvaluationSerializer, MembreBureauSerializer,
    PublicationSerializer, SondageSerializer, QuestionSondageSerializer,
    OptionQuestionSerializer, ReponseSondageSerializer, EvenementSerializer,
    InscriptionEvenementSerializer, MessageBureauSerializer,
    DemandeAdministrativeSerializer, ObjetPerduSerializer,
    ClasseSerializer, InscriptionSerializer, EnseignementMatiereSerializer,
    EnseignementMatiereCreateSerializer
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
        elif request.user.role in ['professeur', 'enseignant']:
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
            
            # Compter les étudiants qui ont des notes dans les matières de l'enseignant
            etudiants_ids = Note.objects.filter(
                matiere__in=matieres
            ).values_list('etudiant_id', flat=True).distinct()
            
            # Compter les cours de la semaine
            from datetime import datetime, timedelta
            today = datetime.now().date()
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            
            cours_semaine = EmploiDuTemps.objects.filter(
                matiere__in=matieres
            ).count()

            return Response({
                'nb_matieres': matieres.count(),
                'nb_etudiants': len(etudiants_ids),
                'nb_notes_saisies': Note.objects.filter(
                    matiere__in=matieres
                ).exclude(note_cc__isnull=True, note_examen__isnull=True).count(),
                'nb_cours_semaine': cours_semaine,
                'matieres': MatiereSerializer(matieres, many=True).data,
            })
        except Enseignant.DoesNotExist:
            return Response({'error': 'Profil enseignant non trouvé'}, status=404)


class DashboardEtudiantView(APIView):
    permission_classes = [IsEtudiant]

    def get(self, request):
        try:
            etudiant = request.user.etudiant
            notes = Note.objects.filter(etudiant=etudiant, publie=True).select_related('matiere')
            
            # Calculer la moyenne générale
            total_coef = 0
            total_points = 0
            for n in notes:
                if n.moyenne is not None:
                    total_coef += n.matiere.coefficient
                    total_points += n.moyenne * n.matiere.coefficient
            moyenne_generale = round(total_points / total_coef, 2) if total_coef > 0 else 0

            # Calculer le taux de présence (si vous avez un modèle Presence)
            # Pour l'instant, on met une valeur par défaut
            taux_presence = 85

            # Calculer le solde dû
            frais_inscription = etudiant.filiere.frais_inscription if etudiant.filiere else 0
            montant_paye = etudiant.paiements.filter(statut='valide').aggregate(
                total=models.Sum('montant')
            )['total'] or 0
            solde_du = frais_inscription - montant_paye

            # Sérialiser les notes avec le nom de la matière
            notes_data = []
            for note in notes:
                notes_data.append({
                    'id': note.id,
                    'matiere_nom': note.matiere.nom,
                    'coefficient': note.matiere.coefficient,
                    'note_cc': note.note_cc,
                    'note_examen': note.note_examen,
                    'moyenne': note.moyenne,
                    'statut': note.statut,
                    'publie': note.publie
                })

            return Response({
                'etudiant': EtudiantSerializer(etudiant).data,
                'notes': notes_data,
                'total_matieres': notes.count(),
                'moyenne_generale': moyenne_generale,
                'taux_presence': taux_presence,
                'solde_du': solde_du,
                'paiements': PaiementSerializer(
                    etudiant.paiements.filter(statut='valide').order_by('-date_paiement')[:5], 
                    many=True
                ).data,
            })
        except Etudiant.DoesNotExist:
            return Response({'error': 'Profil étudiant non trouvé'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


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
    
    def get_permissions(self):
        # Lecture autorisée pour tous les utilisateurs authentifiés
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        # Modification réservée aux admins
        return [IsAdminOrSuperAdmin()]

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
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'code']
    
    def get_permissions(self):
        # Lecture autorisée pour tous les utilisateurs authentifiés
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        # Modification réservée aux admins
        return [IsAdminOrSuperAdmin()]


# ===== MATIÈRE =====
class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.select_related('filiere', 'enseignant').all()
    serializer_class = MatiereSerializer
    permission_classes = [IsAuthenticated]  # Accessible à tous les utilisateurs authentifiés
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
        if user.role in ['professeur', 'enseignant'] and hasattr(user, 'enseignant'):
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
            except Exception as e:
                print(f"Erreur filtre étudiant: {e}")
                qs = qs.none()
        # Enseignant voit les notes de ses matières
        elif self.request.user.role in ['professeur', 'enseignant']:
            try:
                if not hasattr(self.request.user, 'enseignant'):
                    print(f"Utilisateur {self.request.user.email} n'a pas d'enseignant associé")
                    qs = qs.none()
                else:
                    qs = qs.filter(matiere__enseignant=self.request.user.enseignant)
            except Exception as e:
                print(f"Erreur filtre enseignant: {e}")
                qs = qs.none()

        return qs

    def perform_create(self, serializer):
        serializer.save(saisie_par=self.request.user)

    @action(detail=False, methods=['post'])
    def publier(self, request):
        """Publier les notes d'une matière et notifier les étudiants"""
        matiere_id = request.data.get('matiere_id')
        annee_id = request.data.get('annee_academique_id')
        
        # Compter toutes les notes de cette matière
        total_notes = Note.objects.filter(
            matiere_id=matiere_id,
            annee_academique_id=annee_id
        ).count()
        
        # Trouver les notes non publiées
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
        
        # Message personnalisé selon le résultat
        if count == 0:
            if total_notes > 0:
                message = f'✅ Toutes les notes ({total_notes}) sont déjà publiées.'
            else:
                message = '⚠️ Aucune note trouvée pour cette matière.'
        else:
            message = f'✅ {count} note(s) publiée(s) et {count} notification(s) envoyée(s).'
        
        return Response({
            'detail': message,
            'count': count,
            'total': total_notes
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
        elif self.request.user.role in ['professeur', 'enseignant']:
            try:
                qs = qs.filter(matiere__enseignant=self.request.user.enseignant)
            except: qs = qs.none()

        return qs


# ===== PRÉSENCE =====
class PresenceViewSet(viewsets.ModelViewSet):
    queryset = Presence.objects.select_related('etudiant', 'emploi').all()
    serializer_class = PresenceSerializer
    permission_classes = [IsAuthenticated]  # Accessible à tous (bureau peut consulter)

    def get_queryset(self):
        qs = super().get_queryset()
        # Bureau et admin peuvent tout voir
        if self.request.user.role in ('bureau', 'bureau_executif', 'admin', 'superadmin'):
            pass  # Pas de filtre
        # Enseignant voit ses cours
        elif self.request.user.role in ('enseignant', 'professeur'):
            qs = qs.filter(emploi__enseignant__utilisateur=self.request.user)
        # Étudiant voit ses présences
        elif self.request.user.role == 'etudiant':
            qs = qs.filter(etudiant__utilisateur=self.request.user)
        
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
        elif self.request.user.role in ['professeur', 'enseignant']:
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


# ===== RÉCLAMATION NOTE =====
class ReclamationNoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les réclamations sur les notes
    """
    queryset = ReclamationNote.objects.select_related(
        'note', 'note__etudiant', 'note__matiere', 'note__matiere__enseignant'
    ).all()
    serializer_class = ReclamationNoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        # Étudiant: voir uniquement ses réclamations
        if user.role == 'etudiant':
            try:
                qs = qs.filter(note__etudiant=user.etudiant)
            except:
                qs = qs.none()
        
        # Enseignant: voir les réclamations sur ses matières
        elif user.role in ['professeur', 'enseignant']:
            try:
                qs = qs.filter(note__matiere__enseignant=user.enseignant)
            except:
                qs = qs.none()
        
        # Admin: voir toutes les réclamations
        elif user.role in ['admin', 'superadmin']:
            pass
        
        else:
            qs = qs.none()
        
        # Filtres
        statut = self.request.query_params.get('statut')
        if statut:
            qs = qs.filter(statut=statut)
        
        return qs.order_by('-date_creation')
    
    def perform_create(self, serializer):
        """Créer une réclamation (étudiant uniquement)"""
        if self.request.user.role != 'etudiant':
            raise permissions.PermissionDenied("Seuls les étudiants peuvent créer des réclamations")
        
        serializer.save()
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def traiter(self, request, pk=None):
        """
        Traiter une réclamation (enseignant ou admin)
        """
        reclamation = self.get_object()
        user = request.user
        
        # Vérifier les permissions
        if user.role in ['professeur', 'enseignant']:
            try:
                if reclamation.note.matiere.enseignant != user.enseignant:
                    return Response(
                        {'error': 'Vous ne pouvez traiter que les réclamations de vos matières'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except:
                return Response(
                    {'error': 'Enseignant non trouvé'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif user.role not in ['admin', 'superadmin']:
            return Response(
                {'error': 'Non autorisé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Récupérer les données
        statut = request.data.get('statut')  # 'resolue' ou 'rejetee'
        reponse = request.data.get('reponse_enseignant', '')
        corriger_note = request.data.get('corriger_note', False)
        nouvelle_note_cc = request.data.get('nouvelle_note_cc')
        nouvelle_note_examen = request.data.get('nouvelle_note_examen')
        
        if statut not in ['resolue', 'rejetee']:
            return Response(
                {'error': 'Statut invalide. Utilisez "resolue" ou "rejetee"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mettre à jour la réclamation
        reclamation.statut = statut
        reclamation.reponse_enseignant = reponse
        reclamation.date_traitement = timezone.now()
        reclamation.save()
        
        # Si correction de note demandée et acceptée
        if corriger_note and statut == 'resolue':
            note = reclamation.note
            
            if nouvelle_note_cc is not None:
                note.note_cc = float(nouvelle_note_cc)
            
            if nouvelle_note_examen is not None:
                note.note_examen = float(nouvelle_note_examen)
            
            # Recalculer la moyenne
            if note.note_cc is not None and note.note_examen is not None:
                note.moyenne = (note.note_cc + note.note_examen) / 2
            elif note.note_cc is not None:
                note.moyenne = note.note_cc
            elif note.note_examen is not None:
                note.moyenne = note.note_examen
            
            note.save()
            
            return Response({
                'detail': 'Réclamation traitée et note corrigée',
                'reclamation': ReclamationNoteSerializer(reclamation).data,
                'note_corrigee': {
                    'note_cc': note.note_cc,
                    'note_examen': note.note_examen,
                    'moyenne': note.moyenne
                }
            })
        
        return Response({
            'detail': f'Réclamation {statut}',
            'reclamation': ReclamationNoteSerializer(reclamation).data
        })


# ===== ÉVALUATION =====
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.select_related('matiere', 'annee_academique').all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        matiere = self.request.query_params.get('matiere')
        annee = self.request.query_params.get('annee_academique')
        categorie = self.request.query_params.get('categorie')
        
        if matiere: qs = qs.filter(matiere_id=matiere)
        if annee: qs = qs.filter(annee_academique_id=annee)
        if categorie: qs = qs.filter(categorie=categorie)
        
        # Enseignant ne voit que les évaluations de ses matières
        if self.request.user.role in ['professeur', 'enseignant']:
            try:
                qs = qs.filter(matiere__enseignant=self.request.user.enseignant)
            except: qs = qs.none()
        
        # Étudiant voit les évaluations actives de ses matières
        elif self.request.user.role == 'etudiant':
            try:
                etudiant = self.request.user.etudiant
                qs = qs.filter(
                    matiere__filiere=etudiant.filiere,
                    actif=True
                )
            except: qs = qs.none()
        
        return qs
    
    def get_permissions(self):
        # Seuls les enseignants peuvent créer/modifier/supprimer
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEnseignant()]
        return [IsAuthenticated()]
    
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
    
    @action(detail=True, methods=['post'])
    def repondre(self, request, pk=None):
        """
        Répondre à un questionnaire d'évaluation
        """
        evaluation = self.get_object()
        user = request.user
        
        # Vérifier que l'utilisateur est étudiant
        if user.role != 'etudiant':
            return Response(
                {'error': 'Seuls les étudiants peuvent répondre aux évaluations'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifier que l'évaluation est active
        if not evaluation.actif:
            return Response(
                {'error': 'Cette évaluation n\'est plus active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier que l'étudiant n'a pas déjà répondu
        try:
            etudiant = user.etudiant
            if NoteEvaluation.objects.filter(evaluation=evaluation, etudiant=etudiant).exists():
                return Response(
                    {'error': 'Vous avez déjà répondu à cette évaluation'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'Étudiant non trouvé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Récupérer les réponses
        reponses = request.data.get('reponses', {})
        commentaire = request.data.get('commentaire', '')
        
        if not reponses:
            return Response(
                {'error': 'Aucune réponse fournie'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer la note d'évaluation
        note_eval = NoteEvaluation.objects.create(
            evaluation=evaluation,
            etudiant=etudiant,
            reponses=reponses,
            commentaire=commentaire
        )
        
        return Response({
            'detail': 'Évaluation soumise avec succès',
            'evaluation': NoteEvaluationSerializer(note_eval).data
        })
    
    @action(detail=True, methods=['get'])
    def resultats(self, request, pk=None):
        """
        Obtenir les résultats d'une évaluation (anonymes)
        """
        evaluation = self.get_object()
        user = request.user
        
        # Seuls admin et l'enseignant concerné peuvent voir les résultats
        if user.role in ['professeur', 'enseignant']:
            try:
                if evaluation.matiere and evaluation.matiere.enseignant != user.enseignant:
                    return Response(
                        {'error': 'Non autorisé'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except:
                return Response(
                    {'error': 'Enseignant non trouvé'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif user.role not in ['admin', 'superadmin']:
            return Response(
                {'error': 'Non autorisé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Calculer les statistiques (anonymes)
        notes = NoteEvaluation.objects.filter(evaluation=evaluation)
        total_reponses = notes.count()
        
        # Agréger les réponses
        resultats = {
            'total_participants': total_reponses,
            'questions': []
        }
        
        # Extraire les questions du premier questionnaire
        if total_reponses > 0:
            premiere_note = notes.first()
            if premiere_note and premiere_note.reponses:
                for question_key, _ in premiere_note.reponses.items():
                    # Collecter toutes les réponses pour cette question
                    reponses_question = []
                    for note in notes:
                        if note.reponses and question_key in note.reponses:
                            reponses_question.append(note.reponses[question_key])
                    
                    # Calculer la moyenne si numérique
                    if reponses_question and isinstance(reponses_question[0], (int, float)):
                        moyenne = sum(reponses_question) / len(reponses_question)
                        resultats['questions'].append({
                            'question': question_key,
                            'type': 'numerique',
                            'moyenne': round(moyenne, 2),
                            'min': min(reponses_question),
                            'max': max(reponses_question)
                        })
                    else:
                        resultats['questions'].append({
                            'question': question_key,
                            'type': 'texte',
                            'reponses': reponses_question
                        })
        
        # Commentaires (anonymes)
        commentaires = notes.exclude(commentaire='').values_list('commentaire', flat=True)
        resultats['commentaires'] = list(commentaires)
        
        return Response(resultats)


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
        if self.request.user.role in ['professeur', 'enseignant']:
            try:
                qs = qs.filter(evaluation__matiere__enseignant=self.request.user.enseignant)
            except: qs = qs.none()
        
        # Étudiant voit ses propres notes
        elif self.request.user.role == 'etudiant':
            try:
                qs = qs.filter(etudiant=self.request.user.etudiant)
            except: qs = qs.none()
        
        return qs



# ===== BUREAU EXÉCUTIF =====
class MembreBureauViewSet(viewsets.ModelViewSet):
    queryset = MembreBureau.objects.select_related('utilisateur', 'etudiant').all()
    serializer_class = MembreBureauSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        actif = self.request.query_params.get('actif')
        if actif is not None:
            qs = qs.filter(actif=actif.lower() == 'true')
        return qs


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.select_related('auteur').all()
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['titre', 'contenu']
    
    def get_queryset(self):
        qs = super().get_queryset()
        categorie = self.request.query_params.get('categorie')
        statut = self.request.query_params.get('statut')
        
        if categorie:
            qs = qs.filter(categorie=categorie)
        if statut:
            qs = qs.filter(statut=statut)
        
        # Les non-membres du bureau ne voient que les publications publiées
        if self.request.user.role != 'bureau_executif':
            qs = qs.filter(statut='publie')
        
        return qs
    
    @action(detail=True, methods=['post'])
    def publier(self, request, pk=None):
        publication = self.get_object()
        publication.statut = 'publie'
        publication.date_publication = timezone.now()
        publication.save()
        return Response({'detail': 'Publication publiée avec succès'})
    
    @action(detail=True, methods=['post'])
    def incrementer_vues(self, request, pk=None):
        publication = self.get_object()
        publication.vues += 1
        publication.save()
        return Response({'vues': publication.vues})


class SondageViewSet(viewsets.ModelViewSet):
    queryset = Sondage.objects.select_related('createur').all()
    serializer_class = SondageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        statut = self.request.query_params.get('statut')
        
        if statut:
            qs = qs.filter(statut=statut)
        
        # Les non-membres du bureau ne voient que les sondages actifs
        if self.request.user.role != 'bureau_executif':
            qs = qs.filter(statut='actif')
        
        return qs
    
    @action(detail=True, methods=['get'])
    def resultats(self, request, pk=None):
        sondage = self.get_object()
        questions = sondage.questions.all()
        
        resultats = []
        for question in questions:
            if question.type_question in ['choix_unique', 'choix_multiple']:
                options_stats = []
                for option in question.options.all():
                    nb_reponses = option.reponses.count()
                    options_stats.append({
                        'option': option.texte,
                        'nb_reponses': nb_reponses
                    })
                resultats.append({
                    'question': question.texte,
                    'type': question.type_question,
                    'options': options_stats
                })
            elif question.type_question == 'note':
                reponses = question.reponses.filter(note__isnull=False)
                moyenne = reponses.aggregate(avg=__import__('django.db.models', fromlist=['Avg']).Avg('note'))['avg']
                resultats.append({
                    'question': question.texte,
                    'type': question.type_question,
                    'moyenne': round(moyenne, 2) if moyenne else 0,
                    'nb_reponses': reponses.count()
                })
        
        return Response({
            'sondage': SondageSerializer(sondage).data,
            'resultats': resultats
        })
    
    @action(detail=True, methods=['post'])
    def repondre(self, request, pk=None):
        """
        Répondre à un sondage
        """
        sondage = self.get_object()
        user = request.user
        
        # Vérifier que l'utilisateur est étudiant
        if user.role != 'etudiant':
            return Response(
                {'error': 'Seuls les étudiants peuvent répondre aux sondages'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifier que le sondage est actif
        if sondage.statut != 'actif':
            return Response(
                {'error': 'Ce sondage n\'est plus actif'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier que l'étudiant n'a pas déjà répondu
        try:
            etudiant = user.etudiant
            if ReponseSondage.objects.filter(sondage=sondage, etudiant=etudiant).exists():
                return Response(
                    {'error': 'Vous avez déjà répondu à ce sondage'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'Étudiant non trouvé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Récupérer les réponses
        reponses = request.data.get('reponses', [])
        
        if not reponses:
            return Response(
                {'error': 'Aucune réponse fournie'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer les réponses
        reponses_creees = []
        for reponse_data in reponses:
            question_id = reponse_data.get('question_id')
            option_id = reponse_data.get('option_id')
            reponse_texte = reponse_data.get('reponse_texte', '')
            
            try:
                question = sondage.questions.get(id=question_id)
                
                reponse = ReponseSondage.objects.create(
                    sondage=sondage,
                    question=question,
                    etudiant=etudiant,
                    option_id=option_id if option_id else None,
                    reponse_texte=reponse_texte
                )
                reponses_creees.append(reponse)
            except Exception as e:
                return Response(
                    {'error': f'Erreur lors de la création de la réponse: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response({
            'detail': 'Réponses enregistrées avec succès',
            'nombre_reponses': len(reponses_creees)
        })


class QuestionSondageViewSet(viewsets.ModelViewSet):
    queryset = QuestionSondage.objects.select_related('sondage').all()
    serializer_class = QuestionSondageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        sondage = self.request.query_params.get('sondage')
        if sondage:
            qs = qs.filter(sondage_id=sondage)
        return qs


class OptionQuestionViewSet(viewsets.ModelViewSet):
    queryset = OptionQuestion.objects.select_related('question').all()
    serializer_class = OptionQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        question = self.request.query_params.get('question')
        if question:
            qs = qs.filter(question_id=question)
        return qs


class ReponseSondageViewSet(viewsets.ModelViewSet):
    queryset = ReponseSondage.objects.select_related('sondage', 'question', 'etudiant').all()
    serializer_class = ReponseSondageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        sondage = self.request.query_params.get('sondage')
        
        if sondage:
            qs = qs.filter(sondage_id=sondage)
        
        # Les étudiants ne voient que leurs propres réponses
        if self.request.user.role == 'etudiant':
            try:
                qs = qs.filter(etudiant=self.request.user.etudiant)
            except:
                qs = qs.none()
        
        return qs
    
    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'etudiant'):
            serializer.save(etudiant=user.etudiant)
        else:
            serializer.save()


class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.select_related('organisateur').all()
    serializer_class = EvenementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['titre', 'description', 'lieu']
    
    def get_queryset(self):
        qs = super().get_queryset()
        statut = self.request.query_params.get('statut')
        type_evenement = self.request.query_params.get('type')
        
        if statut:
            qs = qs.filter(statut=statut)
        if type_evenement:
            qs = qs.filter(type_evenement=type_evenement)
        
        return qs
    
    @action(detail=True, methods=['post'])
    def inscrire(self, request, pk=None):
        evenement = self.get_object()
        
        if not hasattr(request.user, 'etudiant'):
            return Response(
                {'error': 'Seuls les étudiants peuvent s\'inscrire'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifier la capacité
        if evenement.capacite_max:
            nb_inscrits = evenement.inscriptions.filter(statut='confirme').count()
            if nb_inscrits >= evenement.capacite_max:
                return Response(
                    {'error': 'Événement complet'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        inscription, created = InscriptionEvenement.objects.get_or_create(
            evenement=evenement,
            etudiant=request.user.etudiant,
            defaults={'statut': 'confirme'}
        )
        
        if not created:
            return Response(
                {'error': 'Vous êtes déjà inscrit à cet événement'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'detail': 'Inscription réussie',
            'inscription': InscriptionEvenementSerializer(inscription).data
        })
    
    @action(detail=True, methods=['post'])
    def desinscrire(self, request, pk=None):
        evenement = self.get_object()
        
        if not hasattr(request.user, 'etudiant'):
            return Response(
                {'error': 'Seuls les étudiants peuvent se désinscrire'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            inscription = InscriptionEvenement.objects.get(
                evenement=evenement,
                etudiant=request.user.etudiant
            )
            inscription.statut = 'annule'
            inscription.save()
            return Response({'detail': 'Désinscription réussie'})
        except InscriptionEvenement.DoesNotExist:
            return Response(
                {'error': 'Vous n\'êtes pas inscrit à cet événement'},
                status=status.HTTP_404_NOT_FOUND
            )


class InscriptionEvenementViewSet(viewsets.ModelViewSet):
    queryset = InscriptionEvenement.objects.select_related('evenement', 'etudiant').all()
    serializer_class = InscriptionEvenementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        evenement = self.request.query_params.get('evenement')
        
        if evenement:
            qs = qs.filter(evenement_id=evenement)
        
        # Les étudiants ne voient que leurs propres inscriptions
        if self.request.user.role == 'etudiant':
            try:
                qs = qs.filter(etudiant=self.request.user.etudiant)
            except:
                qs = qs.none()
        
        return qs


class MessageBureauViewSet(viewsets.ModelViewSet):
    queryset = MessageBureau.objects.select_related('expediteur', 'destinataire').all()
    serializer_class = MessageBureauSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        # Seuls les membres du bureau peuvent voir les messages
        if user.role != 'bureau_executif':
            return qs.none()
        
        # Filtrer les messages envoyés ou reçus par l'utilisateur
        qs = qs.filter(
            Q(expediteur=user) | Q(destinataire=user) | Q(groupe=True)
        )
        
        return qs
    
    @action(detail=True, methods=['post'])
    def marquer_lu(self, request, pk=None):
        message = self.get_object()
        if message.destinataire == request.user or message.groupe:
            message.lu = True
            message.save()
            return Response({'detail': 'Message marqué comme lu'})
        return Response(
            {'error': 'Non autorisé'},
            status=status.HTTP_403_FORBIDDEN
        )


class DemandeAdministrativeViewSet(viewsets.ModelViewSet):
    queryset = DemandeAdministrative.objects.select_related('etudiant', 'traite_par').all()
    serializer_class = DemandeAdministrativeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        # Étudiant: voir uniquement ses demandes
        if user.role == 'etudiant':
            try:
                qs = qs.filter(etudiant=user.etudiant)
            except:
                qs = qs.none()
        
        # Enseignant: voir les demandes qui lui sont adressées
        elif user.role in ['professeur', 'enseignant']:
            try:
                qs = qs.filter(
                    destinataire='professeur',
                    professeur=user.enseignant
                )
            except:
                qs = qs.none()
        
        # Admin: voir les demandes administratives
        elif user.role in ['admin', 'superadmin']:
            qs = qs.filter(destinataire='administration')
        
        # Bureau: voir toutes les demandes
        elif user.role in ['bureau', 'bureau_executif']:
            pass  # Voir toutes les demandes
        
        else:
            qs = qs.none()
        
        # Filtres
        statut = self.request.query_params.get('statut')
        if statut:
            qs = qs.filter(statut=statut)
        
        type_demande = self.request.query_params.get('type')
        if type_demande:
            qs = qs.filter(type_demande=type_demande)
        
        return qs.order_by('-date_creation')
    
    @action(detail=True, methods=['post'])
    def traiter(self, request, pk=None):
        demande = self.get_object()
        
        # Seuls les admins et le bureau peuvent traiter
        if request.user.role not in ['admin', 'superadmin', 'bureau_executif']:
            return Response(
                {'error': 'Non autorisé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        statut = request.data.get('statut')
        commentaire = request.data.get('commentaire_admin', '')
        
        if statut not in ['approuve', 'rejete', 'termine']:
            return Response(
                {'error': 'Statut invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        demande.statut = statut
        demande.commentaire_admin = commentaire
        demande.traite_par = request.user
        demande.date_traitement = timezone.now()
        demande.save()
        
        return Response({
            'detail': f'Demande {statut}',
            'demande': DemandeAdministrativeSerializer(demande).data
        })
    
    @action(detail=True, methods=['post'])
    def repondre(self, request, pk=None):
        """
        Répondre à une demande
        """
        demande = self.get_object()
        user = request.user
        
        # Vérifier les permissions
        if user.role in ['professeur', 'enseignant']:
            try:
                if demande.professeur != user.enseignant:
                    return Response(
                        {'error': 'Vous ne pouvez répondre qu\'aux demandes qui vous sont adressées'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except:
                return Response(
                    {'error': 'Enseignant non trouvé'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif user.role not in ['admin', 'superadmin', 'bureau_executif']:
            return Response(
                {'error': 'Non autorisé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Récupérer les données
        statut = request.data.get('statut')  # 'en_cours', 'traitee', 'rejetee'
        reponse = request.data.get('reponse', '')
        
        if statut not in ['en_cours', 'traitee', 'rejetee']:
            return Response(
                {'error': 'Statut invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mettre à jour la demande
        demande.statut = statut
        demande.reponse = reponse
        demande.traite_par = user
        demande.date_traitement = timezone.now()
        demande.save()
        
        return Response({
            'detail': f'Demande {statut}',
            'demande': DemandeAdministrativeSerializer(demande).data
        })


class ObjetPerduViewSet(viewsets.ModelViewSet):
    queryset = ObjetPerdu.objects.select_related('declarant').all()
    serializer_class = ObjetPerduSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom_objet', 'description', 'lieu']
    
    def get_queryset(self):
        qs = super().get_queryset()
        type_declaration = self.request.query_params.get('type')
        statut = self.request.query_params.get('statut')
        
        if type_declaration:
            qs = qs.filter(type_declaration=type_declaration)
        if statut:
            qs = qs.filter(statut=statut)
        
        return qs
    
    @action(detail=True, methods=['post'])
    def marquer_recupere(self, request, pk=None):
        objet = self.get_object()
        objet.statut = 'recupere'
        objet.save()
        return Response({'detail': 'Objet marqué comme récupéré'})
    
    @action(detail=True, methods=['patch'])
    def changer_statut(self, request, pk=None):
        """
        Changer le statut d'un objet perdu
        """
        objet = self.get_object()
        user = request.user
        
        # Seuls admin et bureau peuvent changer le statut
        if user.role not in ['admin', 'superadmin', 'bureau_executif']:
            return Response(
                {'error': 'Non autorisé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        nouveau_statut = request.data.get('statut')
        
        if nouveau_statut not in ['actif', 'recupere', 'archive']:
            return Response(
                {'error': 'Statut invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        objet.statut = nouveau_statut
        objet.save()
        
        return Response({
            'detail': f'Statut changé en {nouveau_statut}',
            'objet': ObjetPerduSerializer(objet).data
        })


# ===== DASHBOARD BUREAU EXÉCUTIF =====
class DashboardBureauView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'bureau_executif':
            return Response(
                {'error': 'Accès réservé au Bureau Exécutif'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Statistiques Bureau
        nb_publications = Publication.objects.filter(statut='publie').count()
        nb_sondages_actifs = Sondage.objects.filter(statut='actif').count()
        nb_evenements_planifies = Evenement.objects.filter(statut='planifie').count()
        nb_demandes_en_attente = DemandeAdministrative.objects.filter(statut='en_attente').count()
        nb_messages_non_lus = MessageBureau.objects.filter(
            Q(destinataire=request.user, lu=False) | Q(groupe=True, lu=False)
        ).count()
        
        # Données récentes Bureau
        publications_recentes = Publication.objects.filter(statut='publie').order_by('-date_publication')[:5]
        evenements_prochains = Evenement.objects.filter(
            statut='planifie',
            date_debut__gte=timezone.now()
        ).order_by('date_debut')[:5]
        
        # Données Étudiant (car les membres du bureau sont des étudiants)
        etudiant_data = {}
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

            etudiant_data = {
                'etudiant': EtudiantSerializer(etudiant).data,
                'notes_s1': NoteSerializer(notes_s1, many=True).data,
                'notes_s2': NoteSerializer(notes_s2, many=True).data,
                'moyenne_s1': calc_moy(notes_s1),
                'moyenne_s2': calc_moy(notes_s2),
                'paiements': PaiementSerializer(
                    etudiant.paiements.filter(statut='valide').order_by('-date_paiement')[:5], many=True
                ).data,
                'solde_du': etudiant.solde_du,
            }
        except Etudiant.DoesNotExist:
            pass
        
        return Response({
            # Données Bureau
            'nb_publications': nb_publications,
            'nb_sondages_actifs': nb_sondages_actifs,
            'nb_evenements_planifies': nb_evenements_planifies,
            'nb_demandes_en_attente': nb_demandes_en_attente,
            'nb_messages_non_lus': nb_messages_non_lus,
            'publications_recentes': PublicationSerializer(publications_recentes, many=True).data,
            'evenements_prochains': EvenementSerializer(evenements_prochains, many=True).data,
            # Données Étudiant
            **etudiant_data
        })


# ===== CLASSE =====
class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.select_related('filiere').all()
    serializer_class = ClasseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrSuperAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        qs = super().get_queryset()
        filiere = self.request.query_params.get('filiere')
        niveau = self.request.query_params.get('niveau')
        annee = self.request.query_params.get('annee_academique')
        
        if filiere:
            qs = qs.filter(filiere_id=filiere)
        if niveau:
            qs = qs.filter(niveau=niveau)
        if annee:
            qs = qs.filter(annee_academique=annee)
        
        return qs


# ===== INSCRIPTION =====
class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.select_related('etudiant', 'classe').all()
    serializer_class = InscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrSuperAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        qs = super().get_queryset()
        classe = self.request.query_params.get('classe')
        etudiant = self.request.query_params.get('etudiant')
        statut = self.request.query_params.get('statut')
        
        if classe:
            qs = qs.filter(classe_id=classe)
        if etudiant:
            qs = qs.filter(etudiant_id=etudiant)
        if statut:
            qs = qs.filter(statut=statut)
        
        return qs


# ===== ENSEIGNEMENT MATIÈRE =====
class EnseignementMatiereViewSet(viewsets.ModelViewSet):
    queryset = EnseignementMatiere.objects.select_related(
        'enseignant', 'matiere', 'classe', 'classe__filiere'
    ).all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrSuperAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnseignementMatiereCreateSerializer
        return EnseignementMatiereSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        enseignant = self.request.query_params.get('enseignant')
        matiere = self.request.query_params.get('matiere')
        classe = self.request.query_params.get('classe')
        annee = self.request.query_params.get('annee_academique')
        
        if enseignant:
            qs = qs.filter(enseignant_id=enseignant)
        if matiere:
            qs = qs.filter(matiere_id=matiere)
        if classe:
            qs = qs.filter(classe_id=classe)
        if annee:
            qs = qs.filter(annee_academique=annee)
        
        # Enseignant voit seulement ses assignations
        if self.request.user.role in ['professeur', 'enseignant']:
            try:
                qs = qs.filter(enseignant=self.request.user.enseignant)
            except:
                qs = qs.none()
        
        return qs
    
    @action(detail=False, methods=['get'])
    def par_enseignant(self, request):
        """Liste tous les enseignants avec leurs assignations"""
        enseignants = Enseignant.objects.all()
        result = []
        
        for ens in enseignants:
            enseignements = self.get_queryset().filter(enseignant=ens)
            result.append({
                'enseignant': EnseignantSerializer(ens).data,
                'enseignements': EnseignementMatiereSerializer(enseignements, many=True).data,
                'nb_classes': enseignements.values('classe').distinct().count(),
                'nb_matieres': enseignements.values('matiere').distinct().count(),
            })
        
        return Response(result)
