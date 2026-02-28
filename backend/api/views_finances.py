"""
Vues pour la gestion financière
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta

from .models import (
    Etudiant, Paiement, RappelPaiement, LettreRappel,
    Notification, Utilisateur, Filiere
)
from .serializers import (
    RappelPaiementSerializer, LettreRappelSerializer,
    StatistiquesFinancieresSerializer, EtudiantSerializer
)
from .permissions import IsAdminOrSuperAdmin


class GestionFinanciereViewSet(viewsets.ViewSet):
    """
    ViewSet pour la gestion financière globale
    """
    permission_classes = [IsAdminOrSuperAdmin]
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """
        Statistiques financières globales
        """
        # Total encaissé
        total_encaisse = Paiement.objects.filter(statut='valide').aggregate(
            total=Sum('montant')
        )['total'] or 0
        
        # Total impayé
        total_impaye = Etudiant.objects.aggregate(
            total=Sum('solde_du')
        )['total'] or 0
        
        # Taux de recouvrement
        total_attendu = total_encaisse + total_impaye
        taux_recouvrement = (total_encaisse / total_attendu * 100) if total_attendu > 0 else 0
        
        # Nombre d'étudiants
        nb_etudiants_total = Etudiant.objects.count()
        nb_etudiants_a_jour = Etudiant.objects.filter(solde_du=0).count()
        nb_etudiants_impayes = nb_etudiants_total - nb_etudiants_a_jour
        
        # Statistiques par filière
        filieres = Filiere.objects.all()
        stats_filieres = []
        
        for filiere in filieres:
            etudiants_filiere = Etudiant.objects.filter(filiere=filiere)
            encaisse_filiere = Paiement.objects.filter(
                etudiant__filiere=filiere,
                statut='valide'
            ).aggregate(total=Sum('montant'))['total'] or 0
            
            impaye_filiere = etudiants_filiere.aggregate(
                total=Sum('solde_du')
            )['total'] or 0
            
            total_filiere = encaisse_filiere + impaye_filiere
            taux_filiere = (encaisse_filiere / total_filiere * 100) if total_filiere > 0 else 0
            
            stats_filieres.append({
                'filiere_id': filiere.id,
                'filiere_nom': filiere.nom,
                'filiere_code': filiere.code,
                'encaisse': int(encaisse_filiere),
                'impaye': int(impaye_filiere),
                'taux': round(taux_filiere, 1),
                'nb_etudiants': etudiants_filiere.count(),
                'nb_impayes': etudiants_filiere.filter(solde_du__gt=0).count()
            })
        
        data = {
            'total_encaisse': int(total_encaisse),
            'total_impaye': int(total_impaye),
            'taux_recouvrement': round(taux_recouvrement, 1),
            'nb_etudiants_total': nb_etudiants_total,
            'nb_etudiants_a_jour': nb_etudiants_a_jour,
            'nb_etudiants_impayes': nb_etudiants_impayes,
            'statistiques_par_filiere': stats_filieres
        }
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def liste_impayes(self, request):
        """
        Liste des étudiants en situation d'impayé
        """
        # Filtres
        filiere_id = request.query_params.get('filiere')
        niveau = request.query_params.get('niveau')
        montant_min = request.query_params.get('montant_min')
        
        # Query de base
        etudiants = Etudiant.objects.filter(solde_du__gt=0).select_related(
            'filiere', 'universite', 'annee_academique', 'utilisateur'
        )
        
        # Appliquer les filtres
        if filiere_id:
            etudiants = etudiants.filter(filiere_id=filiere_id)
        if niveau:
            etudiants = etudiants.filter(niveau=niveau)
        if montant_min:
            etudiants = etudiants.filter(solde_du__gte=montant_min)
        
        # Ordonner par montant dû (décroissant)
        etudiants = etudiants.order_by('-solde_du')
        
        # Enrichir avec informations de rappels
        data = []
        for etudiant in etudiants:
            dernier_rappel = etudiant.rappels_paiement.order_by('-date_envoi').first()
            
            data.append({
                'id': etudiant.id,
                'matricule': etudiant.matricule,
                'nom': etudiant.get_full_name(),
                'email': etudiant.email,
                'telephone': etudiant.telephone,
                'filiere': etudiant.filiere.nom if etudiant.filiere else None,
                'niveau': etudiant.niveau,
                'solde_du': int(etudiant.solde_du),
                'frais_inscription': int(etudiant.filiere.frais_inscription) if etudiant.filiere else 0,
                'dernier_rappel': {
                    'type': dernier_rappel.get_type_rappel_display() if dernier_rappel else None,
                    'date': dernier_rappel.date_envoi.strftime('%d/%m/%Y') if dernier_rappel else None,
                    'lu': dernier_rappel.lu if dernier_rappel else None
                } if dernier_rappel else None,
                'nb_rappels': etudiant.rappels_paiement.count()
            })
        
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def envoyer_rappel(self, request, pk=None):
        """
        Envoyer un rappel de paiement à un étudiant
        """
        try:
            etudiant = Etudiant.objects.get(pk=pk)
        except Etudiant.DoesNotExist:
            return Response(
                {'error': 'Étudiant non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier qu'il y a bien un impayé
        if etudiant.solde_du <= 0:
            return Response(
                {'error': 'Cet étudiant n\'a pas d\'impayé'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Déterminer le type de rappel
        nb_rappels = etudiant.rappels_paiement.count()
        if nb_rappels == 0:
            type_rappel = 'rappel_1'
            message = f"Bonjour {etudiant.prenom},\n\nNous vous rappelons amicalement que vous avez un solde restant de {int(etudiant.solde_du)} FCFA à régler.\n\nMerci de régulariser votre situation dans les meilleurs délais.\n\nCordialement,\nL'Administration"
        elif nb_rappels == 1:
            type_rappel = 'rappel_2'
            message = f"Bonjour {etudiant.prenom},\n\nCeci est un deuxième rappel concernant votre solde impayé de {int(etudiant.solde_du)} FCFA.\n\nNous vous prions de bien vouloir régulariser votre situation rapidement.\n\nCordialement,\nL'Administration"
        elif nb_rappels == 2:
            type_rappel = 'rappel_3'
            message = f"Bonjour {etudiant.prenom},\n\nCeci est un dernier rappel avant mesures administratives.\n\nVotre solde impayé de {int(etudiant.solde_du)} FCFA doit être réglé dans les 7 jours.\n\nPassé ce délai, des mesures administratives seront prises.\n\nCordialement,\nL'Administration"
        else:
            type_rappel = 'mesure'
            message = f"Bonjour {etudiant.prenom},\n\nEn raison du non-règlement de votre solde de {int(etudiant.solde_du)} FCFA, des mesures administratives ont été prises.\n\nVeuillez vous présenter au service financier dans les plus brefs délais.\n\nCordialement,\nL'Administration"
        
        # Créer le rappel
        rappel = RappelPaiement.objects.create(
            etudiant=etudiant,
            type_rappel=type_rappel,
            montant_du=etudiant.solde_du,
            envoye_par=request.user,
            message=message
        )
        
        # Créer une notification pour l'étudiant
        if etudiant.utilisateur:
            Notification.objects.create(
                utilisateur=etudiant.utilisateur,
                titre=f"Rappel de paiement - {rappel.get_type_rappel_display()}",
                message=message,
                type='warning',
                lue=False
            )
        
        return Response({
            'detail': f'Rappel envoyé avec succès à {etudiant.get_full_name()}',
            'rappel': RappelPaiementSerializer(rappel).data
        })
    
    @action(detail=True, methods=['post'])
    def generer_lettre(self, request, pk=None):
        """
        Générer une lettre de rappel officielle
        """
        try:
            etudiant = Etudiant.objects.get(pk=pk)
        except Etudiant.DoesNotExist:
            return Response(
                {'error': 'Étudiant non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        type_lettre = request.data.get('type_lettre', 'rappel_amiable')
        
        # Générer le contenu de la lettre
        date_str = timezone.now().strftime('%d/%m/%Y')
        
        if type_lettre == 'rappel_amiable':
            contenu = f"""
RAPPEL AMIABLE

Date: {date_str}

Madame, Monsieur {etudiant.nom} {etudiant.prenom}
Matricule: {etudiant.matricule}

Objet: Rappel de paiement des frais de scolarité

Madame, Monsieur,

Nous vous rappelons que vous avez un solde impayé de {int(etudiant.solde_du)} FCFA au titre des frais de scolarité.

Nous vous prions de bien vouloir régulariser votre situation dans les meilleurs délais.

Pour tout renseignement, veuillez contacter le service financier.

Cordialement,
L'Administration
"""
        elif type_lettre == 'mise_en_demeure':
            contenu = f"""
MISE EN DEMEURE

Date: {date_str}

Madame, Monsieur {etudiant.nom} {etudiant.prenom}
Matricule: {etudiant.matricule}

Objet: Mise en demeure de paiement

Madame, Monsieur,

Malgré nos précédents rappels, nous constatons que votre solde impayé de {int(etudiant.solde_du)} FCFA n'a toujours pas été réglé.

Nous vous mettons en demeure de régulariser votre situation sous 15 jours à compter de la réception de cette lettre.

Passé ce délai, nous serons contraints de prendre des mesures administratives.

Cordialement,
L'Administration
"""
        else:  # convocation
            contenu = f"""
CONVOCATION ADMINISTRATIVE

Date: {date_str}

Madame, Monsieur {etudiant.nom} {etudiant.prenom}
Matricule: {etudiant.matricule}

Objet: Convocation pour régularisation de situation financière

Madame, Monsieur,

Vous êtes convoqué(e) au service financier pour régulariser votre situation concernant un impayé de {int(etudiant.solde_du)} FCFA.

Merci de vous présenter dans les 7 jours avec cette convocation.

L'Administration
"""
        
        # Créer la lettre
        lettre = LettreRappel.objects.create(
            etudiant=etudiant,
            type_lettre=type_lettre,
            contenu=contenu,
            generee_par=request.user
        )
        
        return Response({
            'detail': 'Lettre générée avec succès',
            'lettre': LettreRappelSerializer(lettre).data
        })


class RappelPaiementViewSet(viewsets.ModelViewSet):
    """ViewSet pour les rappels de paiement"""
    queryset = RappelPaiement.objects.select_related('etudiant', 'envoye_par').all()
    serializer_class = RappelPaiementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        # Étudiant voit uniquement ses rappels
        if user.role == 'etudiant':
            try:
                qs = qs.filter(etudiant=user.etudiant)
            except:
                qs = qs.none()
        
        # Admin voit tous les rappels
        elif user.role in ['admin', 'superadmin']:
            pass
        
        else:
            qs = qs.none()
        
        return qs.order_by('-date_envoi')
    
    @action(detail=True, methods=['post'])
    def marquer_lu(self, request, pk=None):
        """Marquer un rappel comme lu"""
        rappel = self.get_object()
        rappel.lu = True
        rappel.date_lecture = timezone.now()
        rappel.save()
        return Response({'detail': 'Rappel marqué comme lu'})


class LettreRappelViewSet(viewsets.ModelViewSet):
    """ViewSet pour les lettres de rappel"""
    queryset = LettreRappel.objects.select_related('etudiant', 'generee_par').all()
    serializer_class = LettreRappelSerializer
    permission_classes = [IsAdminOrSuperAdmin]
