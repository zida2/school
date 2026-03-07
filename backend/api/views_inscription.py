from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.db import transaction
from datetime import datetime
import uuid

from .models import DemandeInscription, Etudiant, Utilisateur, Promotion, Classe, Inscription, Universite
from .serializers import DemandeInscriptionSerializer, EtudiantSerializer
from .permissions import IsAdminOrSuperAdmin
from .email_service import envoyer_notification_immediate


class DemandeInscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les demandes d'inscription des étudiants"""
    queryset = DemandeInscription.objects.all()
    serializer_class = DemandeInscriptionSerializer
    
    def get_permissions(self):
        # Création de demande accessible à tous (formulaire public)
        if self.action == 'create':
            return [AllowAny()]
        # Consultation et traitement réservés aux admins
        return [IsAdminOrSuperAdmin()]
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Filtres
        statut = self.request.query_params.get('statut')
        filiere = self.request.query_params.get('filiere')
        annee = self.request.query_params.get('annee_academique')
        
        if statut:
            qs = qs.filter(statut=statut)
        if filiere:
            qs = qs.filter(filiere_demandee_id=filiere)
        if annee:
            qs = qs.filter(annee_academique_id=annee)
        
        return qs
    
    @action(detail=True, methods=['post'])
    def approuver(self, request, pk=None):
        """Approuver une demande et créer le compte étudiant"""
        demande = self.get_object()
        
        if demande.statut != 'en_attente':
            return Response(
                {'error': 'Cette demande a déjà été traitée'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                # Générer matricule unique
                annee = datetime.now().year
                filiere_code = demande.filiere_demandee.code[:3].upper()
                count = Etudiant.objects.filter(
                    matricule__startswith=f"{annee}{filiere_code}"
                ).count() + 1
                matricule = f"{annee}{filiere_code}{count:04d}"
                
                # Créer le compte utilisateur
                password_temp = f"etudiant{annee}"
                utilisateur = Utilisateur.objects.create_user(
                    email=demande.email,
                    password=password_temp,
                    prenom=demande.prenom,
                    nom=demande.nom,
                    role='etudiant'
                )
                
                # Trouver ou créer la promotion
                promotion, created = Promotion.objects.get_or_create(
                    filiere=demande.filiere_demandee,
                    annee_entree=annee,
                    defaults={
                        'code': f"PROMO-{annee}-{filiere_code}",
                        'libelle': f"Promotion {annee} - {demande.filiere_demandee.nom}",
                        'annee_sortie_prevue': annee + demande.filiere_demandee.duree,
                        'effectif_initial': 1
                    }
                )
                
                if not created:
                    promotion.effectif_initial += 1
                    promotion.save()
                
                # Créer l'étudiant
                etudiant = Etudiant.objects.create(
                    utilisateur=utilisateur,
                    universite=demande.filiere_demandee.universite,
                    filiere=demande.filiere_demandee,
                    annee_academique=demande.annee_academique,
                    promotion=promotion,
                    matricule=matricule,
                    prenom=demande.prenom,
                    nom=demande.nom,
                    email=demande.email,
                    telephone=demande.telephone,
                    date_naissance=demande.date_naissance,
                    lieu_naissance=demande.lieu_naissance,
                    genre=demande.genre,
                    niveau=demande.niveau_demande,
                    lycee_provenance=demande.lycee_provenance,
                    ville_origine=demande.ville_origine,
                    serie_bac=demande.serie_bac,
                    annee_bac=demande.annee_bac,
                    mention_bac=demande.mention_bac,
                    solde_du=demande.filiere_demandee.frais_inscription,
                    photo=demande.photo
                )
                
                # Trouver ou créer la classe appropriée
                classe_code = f"{demande.niveau_demande}-{filiere_code}-{annee}"
                classe, created = Classe.objects.get_or_create(
                    code=classe_code,
                    annee_academique=str(annee),
                    defaults={
                        'nom': f"Classe {demande.niveau_demande} {demande.filiere_demandee.nom} {annee}",
                        'filiere': demande.filiere_demandee,
                        'niveau': demande.niveau_demande,
                        'effectif_max': 50
                    }
                )
                
                # Inscrire l'étudiant dans la classe
                Inscription.objects.create(
                    etudiant=etudiant,
                    classe=classe,
                    annee_academique=str(annee),
                    statut='actif'
                )
                
                # Mettre à jour la demande
                demande.statut = 'approuvee'
                demande.date_traitement = timezone.now()
                demande.traite_par = request.user
                demande.etudiant_cree = etudiant
                demande.save()
                
                # Mettre à jour les effectifs
                promotion.update_effectifs()
                
                # Envoyer l'email avec les identifiants
                try:
                    sujet = "Inscription validée - Vos identifiants UniERP"
                    contenu = f"""Bonjour {demande.prenom} {demande.nom},

Votre demande d'inscription a été approuvée avec succès !

Voici vos identifiants de connexion :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email : {demande.email}
🔑 Mot de passe : {password_temp}
🎓 Matricule : {matricule}
🏫 Filière : {demande.filiere_demandee.nom}
📚 Niveau : {demande.niveau_demande}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANT : Pour votre sécurité, veuillez changer votre mot de passe lors de votre première connexion.

Vous pouvez vous connecter à votre espace étudiant via l'application mobile :
👉 https://school-wheat-six.vercel.app/mobile/

Bienvenue à l'université !

Cordialement,
L'équipe UniERP BF"""
                    
                    envoyer_notification_immediate(
                        destinataire=utilisateur,
                        type_notification='inscription',
                        sujet=sujet,
                        contenu=contenu,
                        lien='/mobile/'
                    )
                except Exception as email_error:
                    # Log l'erreur mais ne bloque pas la validation
                    print(f"Erreur envoi email: {email_error}")
                
                return Response({
                    'detail': 'Demande approuvée avec succès',
                    'matricule': matricule,
                    'email': demande.email,
                    'password_temporaire': password_temp,
                    'etudiant': EtudiantSerializer(etudiant).data
                })
        
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de l\'approbation: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def rejeter(self, request, pk=None):
        """Rejeter une demande d'inscription"""
        demande = self.get_object()
        
        if demande.statut != 'en_attente':
            return Response(
                {'error': 'Cette demande a déjà été traitée'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        commentaire = request.data.get('commentaire', '')
        
        demande.statut = 'rejetee'
        demande.date_traitement = timezone.now()
        demande.traite_par = request.user
        demande.commentaire_admin = commentaire
        demande.save()
        
        # Envoyer email de rejet
        try:
            sujet = "Demande d'inscription - Statut"
            contenu = f"""Bonjour {demande.prenom} {demande.nom},

Nous avons examiné votre demande d'inscription pour la filière {demande.filiere_demandee.nom}.

Malheureusement, nous ne pouvons pas donner suite à votre demande pour le moment.

{f"Motif : {commentaire}" if commentaire else ""}

Pour plus d'informations, vous pouvez contacter le service des inscriptions.

Cordialement,
L'équipe UniERP BF"""
            
            # Créer un utilisateur temporaire pour l'email (si pas encore créé)
            try:
                utilisateur_temp = Utilisateur.objects.get(email=demande.email)
            except Utilisateur.DoesNotExist:
                # Créer un utilisateur temporaire juste pour l'email
                utilisateur_temp = Utilisateur(
                    email=demande.email,
                    prenom=demande.prenom,
                    nom=demande.nom,
                    role='etudiant',
                    is_active=False
                )
                utilisateur_temp.save()
            
            envoyer_notification_immediate(
                destinataire=utilisateur_temp,
                type_notification='inscription',
                sujet=sujet,
                contenu=contenu
            )
        except Exception as email_error:
            print(f"Erreur envoi email rejet: {email_error}")
        
        return Response({
            'detail': 'Demande rejetée',
            'commentaire': commentaire
        })
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Statistiques des demandes d'inscription"""
        total = self.get_queryset().count()
        en_attente = self.get_queryset().filter(statut='en_attente').count()
        approuvees = self.get_queryset().filter(statut='approuvee').count()
        rejetees = self.get_queryset().filter(statut='rejetee').count()
        
        # Par filière
        par_filiere = {}
        for demande in self.get_queryset():
            filiere = demande.filiere_demandee.nom
            if filiere not in par_filiere:
                par_filiere[filiere] = {'total': 0, 'en_attente': 0, 'approuvees': 0, 'rejetees': 0}
            par_filiere[filiere]['total'] += 1
            par_filiere[filiere][demande.statut.replace('approuvee', 'approuvees').replace('rejetee', 'rejetees')] += 1
        
        return Response({
            'total': total,
            'en_attente': en_attente,
            'approuvees': approuvees,
            'rejetees': rejetees,
            'taux_approbation': round((approuvees / total * 100), 2) if total > 0 else 0,
            'par_filiere': par_filiere
        })
    
    @action(detail=False, methods=['post'])
    def approuver_masse(self, request):
        """Approuver plusieurs demandes en masse"""
        demande_ids = request.data.get('demande_ids', [])
        
        if not demande_ids:
            return Response(
                {'error': 'Aucune demande sélectionnée'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        demandes = DemandeInscription.objects.filter(
            id__in=demande_ids,
            statut='en_attente'
        )
        
        resultats = {
            'succes': [],
            'echecs': []
        }
        
        for demande in demandes:
            try:
                # Utiliser la même logique que approuver()
                response = self.approuver(request, pk=demande.id)
                if response.status_code == 200:
                    resultats['succes'].append({
                        'id': demande.id,
                        'nom': f"{demande.prenom} {demande.nom}"
                    })
                else:
                    resultats['echecs'].append({
                        'id': demande.id,
                        'nom': f"{demande.prenom} {demande.nom}",
                        'erreur': response.data.get('error', 'Erreur inconnue')
                    })
            except Exception as e:
                resultats['echecs'].append({
                    'id': demande.id,
                    'nom': f"{demande.prenom} {demande.nom}",
                    'erreur': str(e)
                })
        
        return Response({
            'detail': f"{len(resultats['succes'])} demande(s) approuvée(s), {len(resultats['echecs'])} échec(s)",
            'resultats': resultats
        })


class PromotionViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les promotions"""
    queryset = Promotion.objects.all()
    permission_classes = [IsAdminOrSuperAdmin]
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        filiere = self.request.query_params.get('filiere')
        annee = self.request.query_params.get('annee_entree')
        
        if filiere:
            qs = qs.filter(filiere_id=filiere)
        if annee:
            qs = qs.filter(annee_entree=annee)
        
        return qs
    
    @action(detail=True, methods=['get'])
    def etudiants(self, request, pk=None):
        """Liste des étudiants d'une promotion"""
        promotion = self.get_object()
        etudiants = promotion.etudiants.all()
        
        return Response({
            'promotion': {
                'code': promotion.code,
                'libelle': promotion.libelle,
                'annee_entree': promotion.annee_entree,
                'annee_sortie_prevue': promotion.annee_sortie_prevue,
                'effectif_actuel': promotion.effectif_actuel
            },
            'etudiants': EtudiantSerializer(etudiants, many=True).data
        })
    
    @action(detail=True, methods=['post'])
    def update_effectifs(self, request, pk=None):
        """Mettre à jour les effectifs de la promotion"""
        promotion = self.get_object()
        promotion.update_effectifs()
        
        return Response({
            'detail': 'Effectifs mis à jour',
            'effectif_actuel': promotion.effectif_actuel
        })



# ===== DEMANDES INSCRIPTION PROFESSEURS =====
from .models import DemandeInscriptionProfesseur, Enseignant
from .serializers import DemandeInscriptionProfesseurSerializer

class DemandeInscriptionProfesseurViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les demandes d'inscription des professeurs"""
    queryset = DemandeInscriptionProfesseur.objects.all()
    serializer_class = DemandeInscriptionProfesseurSerializer
    
    def get_permissions(self):
        # Création de demande accessible à tous (formulaire public)
        if self.action == 'create':
            return [AllowAny()]
        # Consultation et traitement réservés aux admins
        return [IsAdminOrSuperAdmin()]
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Filtres
        statut = self.request.query_params.get('statut')
        filiere = self.request.query_params.get('filiere')
        
        if statut:
            qs = qs.filter(statut=statut)
        if filiere:
            qs = qs.filter(filiere_enseignee_id=filiere)
        
        return qs
    
    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        """Valider une demande et créer le compte professeur"""
        demande = self.get_object()
        
        if demande.statut != 'en_attente':
            return Response(
                {'error': 'Cette demande a déjà été traitée'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                # Créer l'utilisateur
                password = f"prof{uuid.uuid4().hex[:8]}"
                utilisateur = Utilisateur.objects.create_user(
                    email=demande.email,
                    password=password,
                    prenom=demande.prenom,
                    nom=demande.nom,
                    role='professeur'
                )
                
                # Créer le professeur
                # Récupérer l'université par défaut (la première)
                universite = Universite.objects.first()
                if not universite:
                    raise Exception("Aucune université n'est configurée dans le système")
                
                # Générer un matricule unique
                import random
                matricule = f"PROF{random.randint(10000, 99999)}"
                while Enseignant.objects.filter(matricule=matricule).exists():
                    matricule = f"PROF{random.randint(10000, 99999)}"
                
                enseignant = Enseignant.objects.create(
                    utilisateur=utilisateur,
                    nom=demande.nom,
                    prenom=demande.prenom,
                    email=demande.email,
                    telephone=demande.telephone or '',
                    specialite=demande.filiere_enseignee.nom,
                    universite=universite,
                    matricule=matricule
                )
                
                # Mettre à jour la demande
                demande.statut = 'validee'
                demande.date_traitement = timezone.now()
                demande.traite_par = request.user
                demande.professeur_cree = enseignant
                demande.save()
                
                # Envoyer email avec identifiants
                try:
                    sujet = "Inscription validée - Accès Professeur UniERP"
                    contenu = f"""Bonjour {demande.prenom} {demande.nom},

Votre demande d'inscription en tant qu'enseignant a été validée !

Voici vos identifiants de connexion :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email : {demande.email}
🔑 Mot de passe : {password}
🎓 Spécialité : {demande.filiere_enseignee.nom}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANT : Veuillez changer votre mot de passe lors de votre première connexion.

Vous pouvez vous connecter à votre espace enseignant :
👉 https://school-wheat-six.vercel.app/connexion-professeur.html

Bienvenue dans l'équipe pédagogique !

Cordialement,
L'équipe UniERP BF"""
                    
                    envoyer_notification_immediate(
                        destinataire=utilisateur,
                        type_notification='inscription',
                        sujet=sujet,
                        contenu=contenu,
                        lien='/connexion-professeur.html'
                    )
                except Exception as email_error:
                    print(f"Erreur envoi email professeur: {email_error}")
                
                return Response({
                    'message': 'Demande validée avec succès',
                    'professeur_id': enseignant.id,
                    'email': utilisateur.email,
                    'password_temporaire': password
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def rejeter(self, request, pk=None):
        """Rejeter une demande"""
        demande = self.get_object()
        
        if demande.statut != 'en_attente':
            return Response(
                {'error': 'Cette demande a déjà été traitée'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        commentaire = request.data.get('commentaire', '')
        
        demande.statut = 'rejetee'
        demande.date_traitement = timezone.now()
        demande.traite_par = request.user
        demande.commentaire_admin = commentaire
        demande.save()
        
        # Envoyer email de rejet
        try:
            sujet = "Demande d'inscription enseignant - Statut"
            contenu = f"""Bonjour {demande.prenom} {demande.nom},

Nous avons examiné votre candidature pour un poste d'enseignant.

Malheureusement, nous ne pouvons pas donner suite à votre demande pour le moment.

{f"Motif : {commentaire}" if commentaire else ""}

Nous vous remercions de l'intérêt que vous portez à notre établissement.

Cordialement,
L'équipe UniERP BF"""
            
            try:
                utilisateur_temp = Utilisateur.objects.get(email=demande.email)
            except Utilisateur.DoesNotExist:
                utilisateur_temp = Utilisateur(
                    email=demande.email,
                    prenom=demande.prenom,
                    nom=demande.nom,
                    role='professeur',
                    is_active=False
                )
                utilisateur_temp.save()
            
            envoyer_notification_immediate(
                destinataire=utilisateur_temp,
                type_notification='inscription',
                sujet=sujet,
                contenu=contenu
            )
        except Exception as email_error:
            print(f"Erreur envoi email rejet professeur: {email_error}")
        
        return Response({
            'message': 'Demande rejetée'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def en_attente(self, request):
        """Liste des demandes en attente"""
        demandes = self.get_queryset().filter(statut='en_attente')
        serializer = self.get_serializer(demandes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Statistiques des demandes"""
        total = self.get_queryset().count()
        en_attente = self.get_queryset().filter(statut='en_attente').count()
        validees = self.get_queryset().filter(statut='validee').count()
        rejetees = self.get_queryset().filter(statut='rejetee').count()
        
        return Response({
            'total': total,
            'en_attente': en_attente,
            'validees': validees,
            'rejetees': rejetees
        })



# ===== SERVICES ADMINISTRATIFS =====
from .models import DemandeInscriptionCommunication, DemandeInscriptionAcademique, DemandeInscriptionComptabilite
from .serializers import (
    DemandeInscriptionCommunicationSerializer,
    DemandeInscriptionAcademiqueSerializer,
    DemandeInscriptionComptabiliteSerializer
)
from .views_inscription_emails import (
    envoyer_email_validation_communication,
    envoyer_email_validation_academique,
    envoyer_email_validation_comptabilite,
    envoyer_email_rejet_service
)

# Service Communication
class DemandeInscriptionCommunicationViewSet(viewsets.ModelViewSet):
    queryset = DemandeInscriptionCommunication.objects.all()
    serializer_class = DemandeInscriptionCommunicationSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminOrSuperAdmin()]
    
    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        demande = self.get_object()
        if demande.statut != 'en_attente':
            return Response({'error': 'Demande déjà traitée'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                password = f"comm{uuid.uuid4().hex[:8]}"
                utilisateur = Utilisateur.objects.create_user(
                    email=demande.email,
                    password=password,
                    prenom=demande.prenom,
                    nom=demande.nom,
                    role='communication'
                )
                
                demande.statut = 'validee'
                demande.date_traitement = timezone.now()
                demande.traite_par = request.user
                demande.utilisateur_cree = utilisateur
                demande.save()
                
                return Response({
                    'message': 'Demande validée',
                    'email': utilisateur.email,
                    'password_temporaire': password
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def rejeter(self, request, pk=None):
        demande = self.get_object()
        if demande.statut != 'en_attente':
            return Response({'error': 'Demande déjà traitée'}, status=status.HTTP_400_BAD_REQUEST)
        
        demande.statut = 'rejetee'
        demande.date_traitement = timezone.now()
        demande.traite_par = request.user
        demande.commentaire_admin = request.data.get('commentaire', '')
        demande.save()
        
        return Response({'message': 'Demande rejetée'}, status=status.HTTP_200_OK)


# Service Académique
class DemandeInscriptionAcademiqueViewSet(viewsets.ModelViewSet):
    queryset = DemandeInscriptionAcademique.objects.all()
    serializer_class = DemandeInscriptionAcademiqueSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminOrSuperAdmin()]
    
    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        demande = self.get_object()
        if demande.statut != 'en_attente':
            return Response({'error': 'Demande déjà traitée'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                password = f"acad{uuid.uuid4().hex[:8]}"
                utilisateur = Utilisateur.objects.create_user(
                    email=demande.email,
                    password=password,
                    prenom=demande.prenom,
                    nom=demande.nom,
                    role='academique'
                )
                
                demande.statut = 'validee'
                demande.date_traitement = timezone.now()
                demande.traite_par = request.user
                demande.utilisateur_cree = utilisateur
                demande.save()
                
                return Response({
                    'message': 'Demande validée',
                    'email': utilisateur.email,
                    'password_temporaire': password
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def rejeter(self, request, pk=None):
        demande = self.get_object()
        if demande.statut != 'en_attente':
            return Response({'error': 'Demande déjà traitée'}, status=status.HTTP_400_BAD_REQUEST)
        
        demande.statut = 'rejetee'
        demande.date_traitement = timezone.now()
        demande.traite_par = request.user
        demande.commentaire_admin = request.data.get('commentaire', '')
        demande.save()
        
        return Response({'message': 'Demande rejetée'}, status=status.HTTP_200_OK)


# Service Comptabilité
class DemandeInscriptionComptabiliteViewSet(viewsets.ModelViewSet):
    queryset = DemandeInscriptionComptabilite.objects.all()
    serializer_class = DemandeInscriptionComptabiliteSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminOrSuperAdmin()]
    
    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        demande = self.get_object()
        if demande.statut != 'en_attente':
            return Response({'error': 'Demande déjà traitée'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                password = f"compta{uuid.uuid4().hex[:8]}"
                utilisateur = Utilisateur.objects.create_user(
                    email=demande.email,
                    password=password,
                    prenom=demande.prenom,
                    nom=demande.nom,
                    role='comptabilite'
                )
                
                demande.statut = 'validee'
                demande.date_traitement = timezone.now()
                demande.traite_par = request.user
                demande.utilisateur_cree = utilisateur
                demande.save()
                
                return Response({
                    'message': 'Demande validée',
                    'email': utilisateur.email,
                    'password_temporaire': password
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def rejeter(self, request, pk=None):
        demande = self.get_object()
        if demande.statut != 'en_attente':
            return Response({'error': 'Demande déjà traitée'}, status=status.HTTP_400_BAD_REQUEST)
        
        demande.statut = 'rejetee'
        demande.date_traitement = timezone.now()
        demande.traite_par = request.user
        demande.commentaire_admin = request.data.get('commentaire', '')
        demande.save()
        
        return Response({'message': 'Demande rejetée'}, status=status.HTTP_200_OK)
