from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    Utilisateur, Universite, AnneeAcademique, Filiere, Matiere,
    Enseignant, Etudiant, Note, Paiement, EmploiDuTemps,
    Presence, SupportCours, Notification, ReclamationNote,
    Evaluation, NoteEvaluation, MembreBureau, Publication,
    Sondage, QuestionSondage, OptionQuestion, ReponseSondage,
    Evenement, InscriptionEvenement, MessageBureau,
    DemandeAdministrative, ObjetPerdu, RappelPaiement, LettreRappel
)


# ===== AUTH =====
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Email ou mot de passe incorrect.")
        if not user.is_active:
            raise serializers.ValidationError("Compte désactivé. Contactez l'administration.")
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'prenom': user.prenom,
                'nom': user.nom,
                'role': user.role,
                'full_name': user.get_full_name(),
            }
        }


class UtilisateurSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Utilisateur
        fields = ['id', 'email', 'prenom', 'nom', 'role', 'is_active', 'date_creation', 'full_name']
        read_only_fields = ['date_creation']

    def get_full_name(self, obj):
        return obj.get_full_name()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value


# ===== UNIVERSITÉ =====
class UniversiteSerializer(serializers.ModelSerializer):
    nb_etudiants = serializers.SerializerMethodField()
    nb_enseignants = serializers.SerializerMethodField()

    class Meta:
        model = Universite
        fields = '__all__'

    def get_nb_etudiants(self, obj):
        return obj.etudiants.count()

    def get_nb_enseignants(self, obj):
        return obj.enseignants.count()


# ===== ANNÉE ACADÉMIQUE =====
class AnneeAcademiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnneeAcademique
        fields = '__all__'


# ===== FILIÈRE =====
class FiliereSerializer(serializers.ModelSerializer):
    nb_etudiants = serializers.SerializerMethodField()
    nb_matieres = serializers.SerializerMethodField()
    filiere_code = serializers.CharField(source='code', read_only=True)
    duree_annees = serializers.IntegerField(source='duree', read_only=True)
    frais_annuels = serializers.DecimalField(source='frais_inscription', max_digits=12, decimal_places=0, read_only=True)

    class Meta:
        model = Filiere
        fields = '__all__'

    def get_nb_etudiants(self, obj):
        return obj.etudiants.count()

    def get_nb_matieres(self, obj):
        return obj.matieres.count()


# ===== MATIÈRE =====
class MatiereSerializer(serializers.ModelSerializer):
    filiere_nom = serializers.CharField(source='filiere.nom', read_only=True)
    enseignant_nom = serializers.SerializerMethodField()
    credits_ects = serializers.IntegerField(source='credits', read_only=True)

    class Meta:
        model = Matiere
        fields = '__all__'

    def get_enseignant_nom(self, obj):
        return obj.enseignant.get_full_name() if obj.enseignant else None


# ===== ENSEIGNANT =====
class EnseignantSerializer(serializers.ModelSerializer):
    universite_nom = serializers.CharField(source='universite.nom', read_only=True)
    nb_matieres = serializers.SerializerMethodField()

    class Meta:
        model = Enseignant
        fields = '__all__'

    def get_nb_matieres(self, obj):
        return obj.matieres.count()


class EnseignantCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False, default='enseignant123')
    matricule = serializers.CharField(required=False)

    class Meta:
        model = Enseignant
        fields = '__all__'
        extra_fields = ['password']

    def create(self, validated_data):
        password = validated_data.pop('password', 'enseignant123')
        
        # Générer un matricule automatiquement si non fourni
        if 'matricule' not in validated_data or not validated_data['matricule']:
            from django.utils import timezone
            year = timezone.now().year
            # Compter les enseignants existants pour générer un numéro unique
            count = Enseignant.objects.count() + 1
            validated_data['matricule'] = f"ENS-{year}-{str(count).zfill(3)}"
        
        user = Utilisateur.objects.create_user(
            email=validated_data['email'],
            password=password,
            prenom=validated_data['prenom'],
            nom=validated_data['nom'],
            role='professeur',
        )
        validated_data['utilisateur'] = user
        return super().create(validated_data)


# ===== ÉTUDIANT =====
class EtudiantSerializer(serializers.ModelSerializer):
    filiere_nom = serializers.CharField(source='filiere.nom', read_only=True)
    filiere_code = serializers.CharField(source='filiere.code', read_only=True)
    universite_nom = serializers.CharField(source='universite.nom', read_only=True)
    annee_academique_libelle = serializers.CharField(source='annee_academique.libelle', read_only=True)
    full_name = serializers.SerializerMethodField()
    montant_paye = serializers.SerializerMethodField()

    class Meta:
        model = Etudiant
        fields = '__all__'

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_montant_paye(self, obj):
        return int(obj.paiements.filter(statut='valide').aggregate(
            total=__import__('django.db.models', fromlist=['Sum']).Sum('montant')
        )['total'] or 0)


class EtudiantCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, default='etudiant123')
    matricule = serializers.CharField(required=False)

    class Meta:
        model = Etudiant
        fields = '__all__'
        extra_fields = ['password']

    def create(self, validated_data):
        password = validated_data.pop('password', 'etudiant123')
        
        # Générer le matricule automatiquement s'il n'est pas fourni
        if 'matricule' not in validated_data or not validated_data['matricule']:
            import datetime
            annee = datetime.datetime.now().year
            filiere_code = validated_data.get('filiere').code[:3].upper() if validated_data.get('filiere') else 'ETU'
            # Compter les étudiants existants pour générer un numéro unique
            count = Etudiant.objects.filter(matricule__startswith=f"{annee}{filiere_code}").count() + 1
            validated_data['matricule'] = f"{annee}{filiere_code}{count:04d}"
        
        user = Utilisateur.objects.create_user(
            email=validated_data['email'],
            password=password,
            prenom=validated_data['prenom'],
            nom=validated_data['nom'],
            role='etudiant',
        )
        validated_data['utilisateur'] = user
        frais = validated_data.get('filiere').frais_inscription if validated_data.get('filiere') else 0
        validated_data['solde_du'] = frais
        return super().create(validated_data)


# ===== NOTE =====
class NoteSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    matiere_nom = serializers.CharField(source='matiere.nom', read_only=True)
    matiere_code = serializers.CharField(source='matiere.code', read_only=True)
    coefficient = serializers.IntegerField(source='matiere.coefficient', read_only=True)
    moyenne = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = '__all__'

    def get_etudiant_nom(self, obj):
        return obj.etudiant.get_full_name()

    def get_moyenne(self, obj):
        return obj.moyenne


# ===== ÉVALUATION =====
class EvaluationSerializer(serializers.ModelSerializer):
    matiere_nom = serializers.CharField(source='matiere.nom', read_only=True)
    matiere_code = serializers.CharField(source='matiere.code', read_only=True)
    nb_notes_saisies = serializers.SerializerMethodField()
    nb_etudiants_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Evaluation
        fields = '__all__'
    
    def get_nb_notes_saisies(self, obj):
        return obj.notes.filter(note__isnull=False).count()
    
    def get_nb_etudiants_total(self, obj):
        return obj.notes.count()


# ===== NOTE D'ÉVALUATION =====
class NoteEvaluationSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    etudiant_matricule = serializers.CharField(source='etudiant.matricule', read_only=True)
    evaluation_titre = serializers.CharField(source='evaluation.titre', read_only=True)
    note_sur_20 = serializers.SerializerMethodField()
    
    class Meta:
        model = NoteEvaluation
        fields = '__all__'
    
    def get_etudiant_nom(self, obj):
        return f"{obj.etudiant.prenom} {obj.etudiant.nom}"
    
    def get_note_sur_20(self, obj):
        return obj.note_sur_20


# ===== PAIEMENT =====
class PaiementSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    etudiant_matricule = serializers.CharField(source='etudiant.matricule', read_only=True)

    class Meta:
        model = Paiement
        fields = '__all__'

    def get_etudiant_nom(self, obj):
        return obj.etudiant.get_full_name()


# ===== EMPLOI DU TEMPS =====
class EmploiDuTempsSerializer(serializers.ModelSerializer):
    matiere_nom = serializers.CharField(source='matiere.nom', read_only=True)
    matiere_code = serializers.CharField(source='matiere.code', read_only=True)
    enseignant_nom = serializers.SerializerMethodField()
    filiere_nom = serializers.CharField(source='matiere.filiere.nom', read_only=True)
    filiere_id = serializers.IntegerField(source='matiere.filiere.id', read_only=True)

    class Meta:
        model = EmploiDuTemps
        fields = '__all__'

    def get_enseignant_nom(self, obj):
        return obj.matiere.enseignant.get_full_name() if obj.matiere.enseignant else None


# ===== PRÉSENCE =====
class PresenceSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    etudiant_matricule = serializers.CharField(source='etudiant.matricule', read_only=True)

    class Meta:
        model = Presence
        fields = '__all__'

    def get_etudiant_nom(self, obj):
        return obj.etudiant.get_full_name()


# ===== SUPPORT DE COURS =====
class SupportCoursSerializer(serializers.ModelSerializer):
    matiere_nom = serializers.CharField(source='matiere.nom', read_only=True)
    enseignant_nom = serializers.SerializerMethodField()

    class Meta:
        model = SupportCours
        fields = '__all__'

    def get_enseignant_nom(self, obj):
        return obj.enseignant.get_full_name()


# ===== NOTIFICATION =====
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


# ===== BULLETIN ÉTUDIANT =====
class BulletinSerializer(serializers.Serializer):
    etudiant = EtudiantSerializer()
    notes_s1 = NoteSerializer(many=True)
    notes_s2 = NoteSerializer(many=True)
    moyenne_s1 = serializers.FloatField()
    moyenne_s2 = serializers.FloatField()
    mention_s1 = serializers.CharField()
    mention_s2 = serializers.CharField()


# ===== STATS TABLEAU DE BORD =====
class DashboardStatsSerializer(serializers.Serializer):
    total_etudiants = serializers.IntegerField()
    total_enseignants = serializers.IntegerField()
    total_encaisse = serializers.DecimalField(max_digits=15, decimal_places=0)
    total_impaye = serializers.DecimalField(max_digits=15, decimal_places=0)
    total_filieres = serializers.IntegerField()
    total_matieres = serializers.IntegerField()
    paiements_recents = PaiementSerializer(many=True)
    inscriptions_recentes = EtudiantSerializer(many=True)


# ===== RÉCLAMATION NOTE =====
class ReclamationNoteSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.CharField(source='etudiant.get_full_name', read_only=True)
    etudiant_matricule = serializers.CharField(source='etudiant.matricule', read_only=True)
    matiere_nom = serializers.CharField(source='note.matiere.nom', read_only=True)
    matiere_code = serializers.CharField(source='note.matiere.code', read_only=True)
    note_cc = serializers.DecimalField(source='note.note_cc', max_digits=4, decimal_places=2, read_only=True)
    note_examen = serializers.DecimalField(source='note.note_examen', max_digits=4, decimal_places=2, read_only=True)
    enseignant_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = ReclamationNote
        fields = [
            'id', 'note', 'etudiant', 'etudiant_nom', 'etudiant_matricule',
            'matiere_nom', 'matiere_code', 'note_cc', 'note_examen',
            'type_probleme', 'description', 'note_attendue', 'statut',
            'reponse_enseignant', 'traite_par', 'enseignant_nom',
            'date_creation', 'date_traitement'
        ]
        read_only_fields = ['etudiant', 'date_creation', 'date_traitement']
    
    def get_enseignant_nom(self, obj):
        enseignant = obj.note.matiere.enseignant
        return enseignant.get_full_name() if enseignant else None
    
    def create(self, validated_data):
        # Récupérer l'étudiant depuis l'utilisateur connecté
        user = self.context['request'].user
        if hasattr(user, 'etudiant'):
            validated_data['etudiant'] = user.etudiant
        return super().create(validated_data)


# ===== BUREAU EXÉCUTIF =====
class MembreBureauSerializer(serializers.ModelSerializer):
    utilisateur_nom = serializers.SerializerMethodField()
    utilisateur_email = serializers.CharField(source='utilisateur.email', read_only=True)
    etudiant_matricule = serializers.CharField(source='etudiant.matricule', read_only=True)
    
    class Meta:
        model = MembreBureau
        fields = '__all__'
    
    def get_utilisateur_nom(self, obj):
        return obj.utilisateur.get_full_name()


class PublicationSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = Publication
        fields = '__all__'
        read_only_fields = ['auteur', 'date_creation', 'vues']
    
    def get_auteur_nom(self, obj):
        return obj.auteur.get_full_name()
    
    def create(self, validated_data):
        validated_data['auteur'] = self.context['request'].user
        return super().create(validated_data)


class OptionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionQuestion
        fields = '__all__'


class QuestionSondageSerializer(serializers.ModelSerializer):
    options = OptionQuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuestionSondage
        fields = '__all__'


class SondageSerializer(serializers.ModelSerializer):
    createur_nom = serializers.SerializerMethodField()
    questions = QuestionSondageSerializer(many=True, read_only=True)
    nb_reponses = serializers.SerializerMethodField()
    
    class Meta:
        model = Sondage
        fields = '__all__'
        read_only_fields = ['createur', 'date_creation']
    
    def get_createur_nom(self, obj):
        return obj.createur.get_full_name()
    
    def get_nb_reponses(self, obj):
        return obj.reponses.values('etudiant').distinct().count()
    
    def create(self, validated_data):
        validated_data['createur'] = self.context['request'].user
        return super().create(validated_data)


class ReponseSondageSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    question_texte = serializers.CharField(source='question.texte', read_only=True)
    option_texte = serializers.CharField(source='option.texte', read_only=True)
    
    class Meta:
        model = ReponseSondage
        fields = '__all__'
        read_only_fields = ['etudiant', 'date_reponse']
    
    def get_etudiant_nom(self, obj):
        return obj.etudiant.get_full_name() if obj.etudiant else 'Anonyme'


class InscriptionEvenementSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    etudiant_matricule = serializers.CharField(source='etudiant.matricule', read_only=True)
    evenement_titre = serializers.CharField(source='evenement.titre', read_only=True)
    
    class Meta:
        model = InscriptionEvenement
        fields = '__all__'
        read_only_fields = ['date_inscription']
    
    def get_etudiant_nom(self, obj):
        return obj.etudiant.get_full_name()


class EvenementSerializer(serializers.ModelSerializer):
    organisateur_nom = serializers.SerializerMethodField()
    nb_inscrits = serializers.SerializerMethodField()
    inscriptions = InscriptionEvenementSerializer(many=True, read_only=True)
    
    class Meta:
        model = Evenement
        fields = '__all__'
        read_only_fields = ['organisateur', 'date_creation']
    
    def get_organisateur_nom(self, obj):
        return obj.organisateur.get_full_name()
    
    def get_nb_inscrits(self, obj):
        return obj.inscriptions.filter(statut='confirme').count()
    
    def create(self, validated_data):
        validated_data['organisateur'] = self.context['request'].user
        return super().create(validated_data)


class MessageBureauSerializer(serializers.ModelSerializer):
    expediteur_nom = serializers.SerializerMethodField()
    destinataire_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = MessageBureau
        fields = '__all__'
        read_only_fields = ['expediteur', 'date_envoi']
    
    def get_expediteur_nom(self, obj):
        return obj.expediteur.get_full_name()
    
    def get_destinataire_nom(self, obj):
        return obj.destinataire.get_full_name() if obj.destinataire else 'Groupe'
    
    def create(self, validated_data):
        validated_data['expediteur'] = self.context['request'].user
        return super().create(validated_data)


class DemandeAdministrativeSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    etudiant_matricule = serializers.CharField(source='etudiant.matricule', read_only=True)
    traite_par_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = DemandeAdministrative
        fields = '__all__'
        read_only_fields = ['etudiant', 'date_demande', 'date_traitement', 'traite_par']
    
    def get_etudiant_nom(self, obj):
        return obj.etudiant.get_full_name()
    
    def get_traite_par_nom(self, obj):
        return obj.traite_par.get_full_name() if obj.traite_par else None
    
    def create(self, validated_data):
        user = self.context['request'].user
        if hasattr(user, 'etudiant'):
            validated_data['etudiant'] = user.etudiant
        return super().create(validated_data)


class ObjetPerduSerializer(serializers.ModelSerializer):
    declarant_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = ObjetPerdu
        fields = '__all__'
        read_only_fields = ['declarant', 'date_declaration']
    
    def get_declarant_nom(self, obj):
        return obj.declarant.get_full_name()
    
    def create(self, validated_data):
        validated_data['declarant'] = self.context['request'].user
        return super().create(validated_data)



# ===== GESTION FINANCIÈRE =====
class RappelPaiementSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    etudiant_matricule = serializers.CharField(source='etudiant.matricule', read_only=True)
    type_rappel_display = serializers.CharField(source='get_type_rappel_display', read_only=True)
    
    class Meta:
        model = RappelPaiement
        fields = '__all__'
        read_only_fields = ['date_envoi', 'envoye_par']
    
    def get_etudiant_nom(self, obj):
        return obj.etudiant.get_full_name()


class LettreRappelSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    etudiant_matricule = serializers.CharField(source='etudiant.matricule', read_only=True)
    type_lettre_display = serializers.CharField(source='get_type_lettre_display', read_only=True)
    
    class Meta:
        model = LettreRappel
        fields = '__all__'
        read_only_fields = ['date_generation', 'generee_par']
    
    def get_etudiant_nom(self, obj):
        return obj.etudiant.get_full_name()


class StatistiquesFinancieresSerializer(serializers.Serializer):
    """Serializer pour les statistiques financières globales"""
    total_encaisse = serializers.DecimalField(max_digits=15, decimal_places=0)
    total_impaye = serializers.DecimalField(max_digits=15, decimal_places=0)
    taux_recouvrement = serializers.FloatField()
    nb_etudiants_total = serializers.IntegerField()
    nb_etudiants_a_jour = serializers.IntegerField()
    nb_etudiants_impayes = serializers.IntegerField()
    statistiques_par_filiere = serializers.ListField()


# ===== CLASSE =====
class ClasseSerializer(serializers.ModelSerializer):
    filiere_nom = serializers.CharField(source='filiere.nom', read_only=True)
    filiere_code = serializers.CharField(source='filiere.code', read_only=True)
    effectif_actuel = serializers.ReadOnlyField()
    
    class Meta:
        model = Classe
        fields = '__all__'


# ===== INSCRIPTION =====
class InscriptionSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    etudiant_matricule = serializers.CharField(source='etudiant.matricule', read_only=True)
    classe_nom = serializers.CharField(source='classe.nom', read_only=True)
    classe_code = serializers.CharField(source='classe.code', read_only=True)
    
    class Meta:
        model = Inscription
        fields = '__all__'
    
    def get_etudiant_nom(self, obj):
        return obj.etudiant.get_full_name()


# ===== ENSEIGNEMENT MATIÈRE =====
class EnseignementMatiereSerializer(serializers.ModelSerializer):
    enseignant_nom = serializers.SerializerMethodField()
    enseignant_email = serializers.EmailField(source='enseignant.email', read_only=True)
    matiere_nom = serializers.CharField(source='matiere.nom', read_only=True)
    matiere_code = serializers.CharField(source='matiere.code', read_only=True)
    classe_nom = serializers.CharField(source='classe.nom', read_only=True)
    classe_code = serializers.CharField(source='classe.code', read_only=True)
    filiere_nom = serializers.CharField(source='classe.filiere.nom', read_only=True)
    
    class Meta:
        model = EnseignementMatiere
        fields = '__all__'
    
    def get_enseignant_nom(self, obj):
        return obj.enseignant.get_full_name()


class EnseignementMatiereCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une assignation enseignant-matière-classe"""
    
    class Meta:
        model = EnseignementMatiere
        fields = '__all__'
    
    def validate(self, data):
        # Vérifier que l'enseignant n'est pas déjà assigné à cette matière/classe
        if EnseignementMatiere.objects.filter(
            enseignant=data['enseignant'],
            matiere=data['matiere'],
            classe=data['classe'],
            annee_academique=data['annee_academique'],
            semestre=data['semestre']
        ).exists():
            raise serializers.ValidationError(
                "Cet enseignant est déjà assigné à cette matière pour cette classe."
            )
        return data
