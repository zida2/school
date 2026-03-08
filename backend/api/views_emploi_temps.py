"""
Views spécifiques pour la gestion de l'emploi du temps
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import EmploiDuTemps, Classe, Etudiant, Enseignant, Matiere
from .serializers import EmploiDuTempsSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verifier_conflits(request):
    """
    Vérifie les conflits pour un créneau horaire donné
    - Professeur déjà occupé
    - Salle déjà réservée
    - Chevauchement pour la classe
    """
    matiere_id = request.data.get('matiere')
    classe_id = request.data.get('classe')
    jour = request.data.get('jour')
    heure_debut = request.data.get('heure_debut')
    heure_fin = request.data.get('heure_fin')
    emploi_id = request.data.get('emploi_id')  # Pour exclure lors de la modification
    salle = request.data.get('salle')
    
    conflits = []
    
    try:
        # Récupérer la matière et son enseignant
        matiere = Matiere.objects.get(id=matiere_id)
        enseignant = matiere.enseignant
        
        # Construire la requête de base pour les conflits
        query = Q(jour=jour) & (
            Q(heure_debut__lt=heure_fin, heure_fin__gt=heure_debut)
        )
        
        # Exclure l'emploi en cours de modification
        if emploi_id:
            query &= ~Q(id=emploi_id)
        
        # 1. Vérifier si le professeur est déjà occupé
        if enseignant:
            emplois_prof = EmploiDuTemps.objects.filter(
                query & Q(matiere__enseignant=enseignant)
            )
            if emplois_prof.exists():
                conflits.append({
                    'type': 'professeur',
                    'message': f'Le professeur {enseignant.get_full_name()} a déjà un cours à cet horaire',
                    'details': [
                        {
                            'matiere': e.matiere.nom,
                            'horaire': f"{e.heure_debut.strftime('%H:%M')} - {e.heure_fin.strftime('%H:%M')}",
                            'salle': e.salle
                        } for e in emplois_prof
                    ]
                })
        
        # 2. Vérifier si la salle est déjà réservée
        if salle:
            emplois_salle = EmploiDuTemps.objects.filter(
                query & Q(salle=salle)
            )
            if emplois_salle.exists():
                conflits.append({
                    'type': 'salle',
                    'message': f'La salle {salle} est déjà réservée à cet horaire',
                    'details': [
                        {
                            'matiere': e.matiere.nom,
                            'horaire': f"{e.heure_debut.strftime('%H:%M')} - {e.heure_fin.strftime('%H:%M')}",
                            'professeur': e.matiere.enseignant.get_full_name() if e.matiere.enseignant else 'Non assigné'
                        } for e in emplois_salle
                    ]
                })
        
        # 3. Vérifier si la classe a déjà un cours
        if classe_id:
            emplois_classe = EmploiDuTemps.objects.filter(
                query & Q(classe_id=classe_id)
            )
            if emplois_classe.exists():
                conflits.append({
                    'type': 'classe',
                    'message': 'La classe a déjà un cours à cet horaire',
                    'details': [
                        {
                            'matiere': e.matiere.nom,
                            'horaire': f"{e.heure_debut.strftime('%H:%M')} - {e.heure_fin.strftime('%H:%M')}",
                            'salle': e.salle,
                            'professeur': e.matiere.enseignant.get_full_name() if e.matiere.enseignant else 'Non assigné'
                        } for e in emplois_classe
                    ]
                })
        
        return Response({
            'has_conflicts': len(conflits) > 0,
            'conflicts': conflits
        })
        
    except Matiere.DoesNotExist:
        return Response(
            {'error': 'Matière non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Fonction d'envoi d'emails supprimée - l'emploi du temps est visible dans les dashboards


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def emploi_par_classe(request, classe_id):
    """
    Récupère l'emploi du temps d'une classe spécifique
    """
    try:
        classe = Classe.objects.get(id=classe_id)
        emplois = EmploiDuTemps.objects.filter(classe=classe).order_by('jour', 'heure_debut')
        serializer = EmploiDuTempsSerializer(emplois, many=True)
        
        return Response({
            'classe': {
                'id': classe.id,
                'nom': classe.nom,
                'code': classe.code
            },
            'emplois': serializer.data
        })
        
    except Classe.DoesNotExist:
        return Response(
            {'error': 'Classe non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def emploi_par_professeur(request, professeur_id):
    """
    Récupère l'emploi du temps d'un professeur spécifique
    """
    try:
        professeur = Enseignant.objects.get(id=professeur_id)
        emplois = EmploiDuTemps.objects.filter(
            matiere__enseignant=professeur
        ).order_by('jour', 'heure_debut')
        serializer = EmploiDuTempsSerializer(emplois, many=True)
        
        return Response({
            'professeur': {
                'id': professeur.id,
                'nom': professeur.get_full_name(),
                'email': professeur.email
            },
            'emplois': serializer.data
        })
        
    except Enseignant.DoesNotExist:
        return Response(
            {'error': 'Professeur non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
