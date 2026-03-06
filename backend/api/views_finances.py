from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from django.utils import timezone

from .models import Paiement, RappelPaiement, LettreRappel, Etudiant
from .serializers import PaiementSerializer, RappelPaiementSerializer, LettreRappelSerializer
from .permissions import IsAdminOrSuperAdmin


class GestionFinanciereViewSet(viewsets.ViewSet):
    """ViewSet pour les statistiques et actions financières globales"""
    permission_classes = [IsAdminOrSuperAdmin]
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Statistiques financières globales"""
        # Total encaissé
        total_encaisse = Paiement.objects.filter(statut='valide').aggregate(
            total=Sum('montant')
        )['total'] or 0
        
        # Total impayé
        total_impaye = Etudiant.objects.aggregate(
            total=Sum('solde_du')
        )['total'] or 0
        
        # Nombre d'étudiants
        nb_etudiants_total = Etudiant.objects.count()
        nb_etudiants_a_jour = Etudiant.objects.filter(solde_du=0).count()
        nb_etudiants_impayes = nb_etudiants_total - nb_etudiants_a_jour
        
        # Taux de recouvrement
        total_attendu = total_encaisse + total_impaye
        taux_recouvrement = (total_encaisse / total_attendu * 100) if total_attendu > 0 else 0
        
        return Response({
            'total_encaisse': int(total_encaisse),
            'total_impaye': int(total_impaye),
            'taux_recouvrement': round(taux_recouvrement, 2),
            'nb_etudiants_total': nb_etudiants_total,
            'nb_etudiants_a_jour': nb_etudiants_a_jour,
            'nb_etudiants_impayes': nb_etudiants_impayes,
        })
    
    @action(detail=False, methods=['get'])
    def etudiants_impayes(self, request):
        """Liste des étudiants avec solde impayé"""
        etudiants = Etudiant.objects.filter(solde_du__gt=0).order_by('-solde_du')
        
        data = []
        for etudiant in etudiants:
            data.append({
                'id': etudiant.id,
                'matricule': etudiant.matricule,
                'nom_complet': etudiant.get_full_name(),
                'filiere': etudiant.filiere.nom if etudiant.filiere else '',
                'niveau': etudiant.niveau,
                'solde_du': int(etudiant.solde_du),
                'email': etudiant.email,
                'telephone': etudiant.telephone,
            })
        
        return Response(data)


class RappelPaiementViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les rappels de paiement"""
    queryset = RappelPaiement.objects.all()
    serializer_class = RappelPaiementSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    def perform_create(self, serializer):
        serializer.save(envoye_par=self.request.user)
    
    @action(detail=False, methods=['post'])
    def envoyer_rappels_masse(self, request):
        """Envoyer des rappels à tous les étudiants avec solde impayé"""
        seuil = request.data.get('seuil_minimum', 0)
        type_rappel = request.data.get('type_rappel', 'notification')
        
        etudiants = Etudiant.objects.filter(solde_du__gt=seuil)
        count = 0
        
        for etudiant in etudiants:
            message = f"Rappel de paiement: Vous avez un solde impayé de {int(etudiant.solde_du)} FCFA. Merci de régulariser votre situation."
            
            RappelPaiement.objects.create(
                etudiant=etudiant,
                type_rappel=type_rappel,
                montant_du=etudiant.solde_du,
                message=message,
                envoye_par=request.user
            )
            count += 1
        
        return Response({
            'detail': f'{count} rappel(s) envoyé(s) avec succès',
            'count': count
        })


class LettreRappelViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les lettres de rappel"""
    queryset = LettreRappel.objects.all()
    serializer_class = LettreRappelSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    def perform_create(self, serializer):
        serializer.save(generee_par=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generer_lettre(self, request):
        """Générer une lettre de rappel pour un étudiant"""
        etudiant_id = request.data.get('etudiant_id')
        type_lettre = request.data.get('type_lettre', 'premier')
        
        try:
            etudiant = Etudiant.objects.get(id=etudiant_id)
        except Etudiant.DoesNotExist:
            return Response(
                {'error': 'Étudiant non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Générer le contenu de la lettre
        contenu = f"""
LETTRE DE RAPPEL - {type_lettre.upper()}

Matricule: {etudiant.matricule}
Nom: {etudiant.get_full_name()}
Filière: {etudiant.filiere.nom if etudiant.filiere else 'N/A'}

Montant dû: {int(etudiant.solde_du)} FCFA

Nous vous rappelons que vous avez un solde impayé. 
Merci de régulariser votre situation dans les plus brefs délais.

Date: {timezone.now().strftime('%d/%m/%Y')}
"""
        
        lettre = LettreRappel.objects.create(
            etudiant=etudiant,
            type_lettre=type_lettre,
            montant_du=etudiant.solde_du,
            contenu=contenu,
            generee_par=request.user
        )
        
        return Response(LettreRappelSerializer(lettre).data)
