from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
import uuid
import qrcode
from io import BytesIO
from django.core.files import File

from .models import CarteEtudiant, Etudiant
from .serializers import CarteEtudiantSerializer
from .permissions import IsAdminOrSuperAdmin, IsEtudiant


class CarteEtudiantViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les cartes étudiantes numériques"""
    queryset = CarteEtudiant.objects.all()
    serializer_class = CarteEtudiantSerializer
    
    def get_permissions(self):
        if self.action in ['retrieve', 'ma_carte', 'verifier']:
            return [IsAuthenticated()]
        return [IsAdminOrSuperAdmin()]
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Étudiant ne voit que sa propre carte
        if self.request.user.role == 'etudiant':
            try:
                qs = qs.filter(etudiant=self.request.user.etudiant)
            except:
                qs = qs.none()
        
        return qs
    
    @action(detail=False, methods=['get'])
    def ma_carte(self, request):
        """Récupérer la carte de l'étudiant connecté"""
        try:
            etudiant = request.user.etudiant
            carte, created = CarteEtudiant.objects.get_or_create(
                etudiant=etudiant,
                defaults={
                    'numero_carte': self._generer_numero_carte(etudiant),
                    'code_verification': str(uuid.uuid4()),
                    'date_expiration': timezone.now().date() + timedelta(days=365)
                }
            )
            
            # Générer le QR code si pas encore fait
            if not carte.qr_code:
                self._generer_qr_code(carte)
            
            return Response(CarteEtudiantSerializer(carte).data)
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la récupération de la carte: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def generer_carte(self, request):
        """Générer une carte pour un étudiant (admin uniquement)"""
        etudiant_id = request.data.get('etudiant_id')
        
        try:
            etudiant = Etudiant.objects.get(id=etudiant_id)
        except Etudiant.DoesNotExist:
            return Response(
                {'error': 'Étudiant non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier si une carte existe déjà
        if hasattr(etudiant, 'carte_numerique'):
            return Response(
                {'error': 'Une carte existe déjà pour cet étudiant'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer la carte
        carte = CarteEtudiant.objects.create(
            etudiant=etudiant,
            numero_carte=self._generer_numero_carte(etudiant),
            code_verification=str(uuid.uuid4()),
            date_expiration=timezone.now().date() + timedelta(days=365)
        )
        
        # Générer le QR code
        self._generer_qr_code(carte)
        
        return Response(
            CarteEtudiantSerializer(carte).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['post'])
    def generer_toutes_cartes(self, request):
        """Générer des cartes pour tous les étudiants sans carte"""
        etudiants_sans_carte = Etudiant.objects.filter(carte_numerique__isnull=True)
        count = 0
        
        for etudiant in etudiants_sans_carte:
            carte = CarteEtudiant.objects.create(
                etudiant=etudiant,
                numero_carte=self._generer_numero_carte(etudiant),
                code_verification=str(uuid.uuid4()),
                date_expiration=timezone.now().date() + timedelta(days=365)
            )
            self._generer_qr_code(carte)
            count += 1
        
        return Response({
            'detail': f'{count} carte(s) générée(s) avec succès',
            'count': count
        })
    
    @action(detail=True, methods=['post'])
    def renouveler(self, request, pk=None):
        """Renouveler une carte expirée"""
        carte = self.get_object()
        
        # Nouvelle date d'expiration
        carte.date_expiration = timezone.now().date() + timedelta(days=365)
        carte.statut = 'active'
        carte.save()
        
        return Response({
            'detail': 'Carte renouvelée avec succès',
            'nouvelle_expiration': carte.date_expiration
        })
    
    @action(detail=True, methods=['post'])
    def suspendre(self, request, pk=None):
        """Suspendre une carte"""
        carte = self.get_object()
        carte.statut = 'suspendue'
        carte.save()
        
        return Response({'detail': 'Carte suspendue'})
    
    @action(detail=True, methods=['post'])
    def activer(self, request, pk=None):
        """Activer une carte suspendue"""
        carte = self.get_object()
        carte.statut = 'active'
        carte.save()
        
        return Response({'detail': 'Carte activée'})
    
    @action(detail=False, methods=['post'])
    def verifier(self, request):
        """Vérifier la validité d'une carte via son code"""
        code = request.data.get('code_verification')
        
        try:
            carte = CarteEtudiant.objects.get(code_verification=code)
            
            if carte.est_valide:
                return Response({
                    'valide': True,
                    'etudiant': {
                        'nom': carte.etudiant.get_full_name(),
                        'matricule': carte.etudiant.matricule,
                        'filiere': carte.etudiant.filiere.nom,
                        'niveau': carte.etudiant.niveau,
                        'photo': carte.etudiant.photo.url if carte.etudiant.photo else None
                    },
                    'carte': {
                        'numero': carte.numero_carte,
                        'expiration': carte.date_expiration
                    }
                })
            else:
                return Response({
                    'valide': False,
                    'raison': f'Carte {carte.statut}'
                })
        except CarteEtudiant.DoesNotExist:
            return Response({
                'valide': False,
                'raison': 'Code invalide'
            })
    
    def _generer_numero_carte(self, etudiant):
        """Générer un numéro de carte unique"""
        annee = timezone.now().year
        return f"CARTE-{annee}-{etudiant.matricule}"
    
    def _generer_qr_code(self, carte):
        """Générer le QR code pour la carte"""
        # Données à encoder dans le QR code
        qr_data = f"{carte.code_verification}"
        
        # Créer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Générer l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Sauvegarder dans un buffer
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Sauvegarder dans le modèle
        filename = f'qr_{carte.numero_carte}.png'
        carte.qr_code.save(filename, File(buffer), save=True)
