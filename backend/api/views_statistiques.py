from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from collections import defaultdict

from .models import Etudiant, Filiere
from .permissions import IsAdminOrSuperAdmin


class StatistiquesMarketingViewSet(viewsets.ViewSet):
    """ViewSet pour les statistiques marketing (lycée, ville, filière)"""
    permission_classes = [IsAdminOrSuperAdmin]
    
    @action(detail=False, methods=['get'])
    def par_lycee(self, request):
        """Statistiques par lycée de provenance"""
        stats = Etudiant.objects.exclude(
            Q(lycee_provenance='') | Q(lycee_provenance__isnull=True)
        ).values('lycee_provenance').annotate(
            nombre_etudiants=Count('id')
        ).order_by('-nombre_etudiants')
        
        # Calculer le total
        total = sum(s['nombre_etudiants'] for s in stats)
        
        # Ajouter les pourcentages
        resultats = []
        for stat in stats:
            resultats.append({
                'lycee': stat['lycee_provenance'],
                'nombre_etudiants': stat['nombre_etudiants'],
                'pourcentage': round((stat['nombre_etudiants'] / total * 100), 2) if total > 0 else 0
            })
        
        return Response({
            'total_etudiants': total,
            'nombre_lycees': len(resultats),
            'statistiques': resultats
        })
    
    @action(detail=False, methods=['get'])
    def par_ville(self, request):
        """Statistiques par ville d'origine"""
        stats = Etudiant.objects.exclude(
            Q(ville_origine='') | Q(ville_origine__isnull=True)
        ).values('ville_origine').annotate(
            nombre_etudiants=Count('id')
        ).order_by('-nombre_etudiants')
        
        # Calculer le total
        total = sum(s['nombre_etudiants'] for s in stats)
        
        # Ajouter les pourcentages
        resultats = []
        for stat in stats:
            resultats.append({
                'ville': stat['ville_origine'],
                'nombre_etudiants': stat['nombre_etudiants'],
                'pourcentage': round((stat['nombre_etudiants'] / total * 100), 2) if total > 0 else 0
            })
        
        return Response({
            'total_etudiants': total,
            'nombre_villes': len(resultats),
            'statistiques': resultats
        })
    
    @action(detail=False, methods=['get'])
    def par_filiere(self, request):
        """Statistiques par filière choisie"""
        stats = Filiere.objects.annotate(
            nombre_etudiants=Count('etudiants')
        ).values('id', 'code', 'nom', 'niveau', 'nombre_etudiants').order_by('-nombre_etudiants')
        
        # Calculer le total
        total = sum(s['nombre_etudiants'] for s in stats)
        
        # Ajouter les pourcentages
        resultats = []
        for stat in stats:
            resultats.append({
                'filiere_id': stat['id'],
                'code': stat['code'],
                'nom': stat['nom'],
                'niveau': stat['niveau'],
                'nombre_etudiants': stat['nombre_etudiants'],
                'pourcentage': round((stat['nombre_etudiants'] / total * 100), 2) if total > 0 else 0
            })
        
        return Response({
            'total_etudiants': total,
            'nombre_filieres': len(resultats),
            'statistiques': resultats
        })
    
    @action(detail=False, methods=['get'])
    def croisees_lycee_filiere(self, request):
        """Statistiques croisées: lycée → filière"""
        etudiants = Etudiant.objects.exclude(
            Q(lycee_provenance='') | Q(lycee_provenance__isnull=True)
        ).select_related('filiere')
        
        # Organiser les données
        stats = defaultdict(lambda: defaultdict(int))
        for etudiant in etudiants:
            stats[etudiant.lycee_provenance][etudiant.filiere.nom] += 1
        
        # Formater les résultats
        resultats = []
        for lycee, filieres in stats.items():
            total_lycee = sum(filieres.values())
            resultats.append({
                'lycee': lycee,
                'total_etudiants': total_lycee,
                'filieres': [
                    {
                        'nom': filiere,
                        'nombre': nombre,
                        'pourcentage': round((nombre / total_lycee * 100), 2)
                    }
                    for filiere, nombre in sorted(filieres.items(), key=lambda x: x[1], reverse=True)
                ]
            })
        
        # Trier par nombre total d'étudiants
        resultats.sort(key=lambda x: x['total_etudiants'], reverse=True)
        
        return Response({
            'nombre_lycees': len(resultats),
            'statistiques': resultats
        })
    
    @action(detail=False, methods=['get'])
    def croisees_ville_filiere(self, request):
        """Statistiques croisées: ville → filière"""
        etudiants = Etudiant.objects.exclude(
            Q(ville_origine='') | Q(ville_origine__isnull=True)
        ).select_related('filiere')
        
        # Organiser les données
        stats = defaultdict(lambda: defaultdict(int))
        for etudiant in etudiants:
            stats[etudiant.ville_origine][etudiant.filiere.nom] += 1
        
        # Formater les résultats
        resultats = []
        for ville, filieres in stats.items():
            total_ville = sum(filieres.values())
            resultats.append({
                'ville': ville,
                'total_etudiants': total_ville,
                'filieres': [
                    {
                        'nom': filiere,
                        'nombre': nombre,
                        'pourcentage': round((nombre / total_ville * 100), 2)
                    }
                    for filiere, nombre in sorted(filieres.items(), key=lambda x: x[1], reverse=True)
                ]
            })
        
        # Trier par nombre total d'étudiants
        resultats.sort(key=lambda x: x['total_etudiants'], reverse=True)
        
        return Response({
            'nombre_villes': len(resultats),
            'statistiques': resultats
        })
    
    @action(detail=False, methods=['get'])
    def tableau_bord_complet(self, request):
        """Tableau de bord marketing complet"""
        # Stats par lycée (top 10)
        lycees = Etudiant.objects.exclude(
            Q(lycee_provenance='') | Q(lycee_provenance__isnull=True)
        ).values('lycee_provenance').annotate(
            nombre=Count('id')
        ).order_by('-nombre')[:10]
        
        # Stats par ville (top 10)
        villes = Etudiant.objects.exclude(
            Q(ville_origine='') | Q(ville_origine__isnull=True)
        ).values('ville_origine').annotate(
            nombre=Count('id')
        ).order_by('-nombre')[:10]
        
        # Stats par filière
        filieres = Filiere.objects.annotate(
            nombre=Count('etudiants')
        ).values('nom', 'nombre').order_by('-nombre')
        
        # Totaux
        total_etudiants = Etudiant.objects.count()
        etudiants_avec_lycee = Etudiant.objects.exclude(
            Q(lycee_provenance='') | Q(lycee_provenance__isnull=True)
        ).count()
        etudiants_avec_ville = Etudiant.objects.exclude(
            Q(ville_origine='') | Q(ville_origine__isnull=True)
        ).count()
        
        return Response({
            'totaux': {
                'total_etudiants': total_etudiants,
                'avec_lycee': etudiants_avec_lycee,
                'avec_ville': etudiants_avec_ville,
                'taux_completion_lycee': round((etudiants_avec_lycee / total_etudiants * 100), 2) if total_etudiants > 0 else 0,
                'taux_completion_ville': round((etudiants_avec_ville / total_etudiants * 100), 2) if total_etudiants > 0 else 0,
            },
            'top_lycees': list(lycees),
            'top_villes': list(villes),
            'filieres': list(filieres)
        })
    
    @action(detail=False, methods=['get'])
    def export_donnees(self, request):
        """Exporter toutes les données marketing pour analyse externe"""
        etudiants = Etudiant.objects.select_related('filiere').values(
            'matricule',
            'prenom',
            'nom',
            'email',
            'lycee_provenance',
            'ville_origine',
            'filiere__nom',
            'filiere__code',
            'niveau',
            'statut',
            'date_inscription'
        )
        
        return Response({
            'total': len(etudiants),
            'donnees': list(etudiants)
        })
