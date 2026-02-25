from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    Utilisateur, Universite, AnneeAcademique, Filiere, Matiere,
    Enseignant, Etudiant, Note, Paiement, EmploiDuTemps,
    Presence, SupportCours, Notification, ReclamationNote,
    Evaluation, NoteEvaluation
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

    class Meta:
        model = Etudiant
        fields = '__all__'
        extra_fields = ['password']

    def create(self, validated_data):
        password = validated_data.pop('password', 'etudiant123')
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
    mention = serializers.SerializerMethodField()
    valide = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = '__all__'

    def get_etudiant_nom(self, obj):
        return obj.etudiant.get_full_name()

    def get_moyenne(self, obj):
        return obj.moyenne

    def get_mention(self, obj):
        return obj.mention

    def get_valide(self, obj):
        return obj.valide


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
