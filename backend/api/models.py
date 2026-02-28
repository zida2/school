from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


# ===== MANAGER UTILISATEUR =====
class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault('role', 'superadmin')
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra)


# ===== UTILISATEUR =====
class Utilisateur(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('superadmin', 'Super Administrateur'),
        ('admin', 'Administration'),
        ('professeur', 'Enseignant'),
        ('etudiant', 'Étudiant'),
        ('bureau_executif', 'Bureau Exécutif'),
    ]
    email = models.EmailField(unique=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLES, default='etudiant')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_creation = models.DateTimeField(default=timezone.now)
    derniere_connexion = models.DateTimeField(null=True, blank=True)

    objects = UtilisateurManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['prenom', 'nom']

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role})"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"


# ===== UNIVERSITÉ =====
class Universite(models.Model):
    LICENCES = [('BASIC','Basic'),('STANDARD','Standard'),('PRO','Pro')]
    STATUTS = [('active','Active'),('suspendu','Suspendu'),('expire','Expiré')]
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=200)
    ville = models.CharField(max_length=100)
    adresse = models.TextField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    licence = models.CharField(max_length=20, choices=LICENCES, default='STANDARD')
    statut = models.CharField(max_length=20, choices=STATUTS, default='active')
    date_expiration_licence = models.DateField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Université'
        ordering = ['nom']

    def __str__(self):
        return self.nom


# ===== ANNÉE ACADÉMIQUE =====
class AnneeAcademique(models.Model):
    universite = models.ForeignKey(Universite, on_delete=models.CASCADE, related_name='annees')
    libelle = models.CharField(max_length=20)  # ex: 2024-2025
    debut = models.DateField()
    fin = models.DateField()
    active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('universite', 'libelle')
        ordering = ['-libelle']

    def __str__(self):
        return f"{self.universite.code} – {self.libelle}"


# ===== FILIÈRE =====
class Filiere(models.Model):
    NIVEAUX = [('Licence','Licence'),('Master','Master'),('DUT','DUT'),('Doctorat','Doctorat'),('BTS','BTS')]
    universite = models.ForeignKey(Universite, on_delete=models.CASCADE, related_name='filieres')
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=200)
    niveau = models.CharField(max_length=20, choices=NIVEAUX)
    duree = models.PositiveIntegerField(default=3)
    frais_inscription = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    description = models.TextField(blank=True)
    actif = models.BooleanField(default=True)

    class Meta:
        unique_together = ('universite', 'code')
        ordering = ['niveau', 'nom']

    def __str__(self):
        return f"{self.code} – {self.nom}"


# ===== MATIÈRE =====
class Matiere(models.Model):
    SEMESTRES = [(1,'Semestre 1'),(2,'Semestre 2')]
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='matieres')
    enseignant = models.ForeignKey('Enseignant', on_delete=models.SET_NULL, null=True, blank=True, related_name='matieres')
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=200)
    credits = models.PositiveIntegerField(default=3)
    coefficient = models.PositiveIntegerField(default=1)
    semestre = models.IntegerField(choices=SEMESTRES, default=1)
    niveau = models.CharField(max_length=10, default='L1')
    actif = models.BooleanField(default=True)

    class Meta:
        unique_together = ('filiere', 'code')
        ordering = ['semestre', 'nom']

    def __str__(self):
        return f"{self.code} – {self.nom}"


# ===== ENSEIGNANT =====
class Enseignant(models.Model):
    GRADES = [
        ('assistant','Assistant'),
        ('maitre_assistant','Maître-Assistant'),
        ('maitre_conferences','Maître de Conférences'),
        ('professeur_titulaire','Professeur Titulaire'),
    ]
    STATUTS = [('actif','Actif'),('conge','Congé'),('inactif','Inactif')]
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='enseignant', null=True, blank=True)
    universite = models.ForeignKey(Universite, on_delete=models.CASCADE, related_name='enseignants')
    matricule = models.CharField(max_length=20, unique=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    specialite = models.CharField(max_length=200)
    grade = models.CharField(max_length=30, choices=GRADES, default='maitre_assistant')
    statut = models.CharField(max_length=20, choices=STATUTS, default='actif')
    photo = models.ImageField(upload_to='enseignants/', null=True, blank=True)
    date_recrutement = models.DateField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"


# ===== ÉTUDIANT =====
class Etudiant(models.Model):
    GENRES = [('M','Masculin'),('F','Féminin')]
    STATUTS = [('inscrit','Inscrit'),('reinscrit','Réinscrit'),('bloque','Bloqué'),('diplome','Diplômé'),('abandon','Abandon')]
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='etudiant', null=True, blank=True)
    universite = models.ForeignKey(Universite, on_delete=models.CASCADE, related_name='etudiants')
    filiere = models.ForeignKey(Filiere, on_delete=models.PROTECT, related_name='etudiants')
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.PROTECT, related_name='etudiants')
    matricule = models.CharField(max_length=30, unique=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=1, choices=GENRES, default='M')
    niveau = models.CharField(max_length=10, default='L1')
    statut = models.CharField(max_length=20, choices=STATUTS, default='inscrit')
    solde_du = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    photo = models.ImageField(upload_to='etudiants/', null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.matricule} – {self.prenom} {self.nom}"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"


# ===== NOTE =====
class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='notes')
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE, related_name='notes')
    note_cc = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    note_examen = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    note_rattrapage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    saisie_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)
    date_saisie = models.DateTimeField(auto_now=True)
    publie = models.BooleanField(default=False)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('brouillon', 'Brouillon'),
            ('publie', 'Publié'),
            ('confirme', 'Confirmé par étudiant'),
            ('reclame', 'Réclamé par étudiant')
        ],
        default='brouillon'
    )

    class Meta:
        unique_together = ('etudiant', 'matiere', 'annee_academique')
        ordering = ['matiere__semestre', 'matiere__nom']

    def __str__(self):
        return f"{self.etudiant.matricule} – {self.matiere.code}"

    @property
    def moyenne(self):
        if self.note_cc is not None and self.note_examen is not None:
            return round(float(self.note_cc) * 0.4 + float(self.note_examen) * 0.6, 2)
        return None

    @property
    def mention(self):
        m = self.moyenne
        if m is None:
            return '—'
        if m >= 16:
            return 'Très Bien'
        if m >= 14:
            return 'Bien'
        if m >= 12:
            return 'Assez Bien'
        if m >= 10:
            return 'Passable'
        return 'Ajourné'


# ===== ÉVALUATION (DEVOIR) =====
class Evaluation(models.Model):
    TYPES = [
        ('devoir', 'Devoir'),
        ('interrogation', 'Interrogation'),
        ('tp', 'Travaux Pratiques'),
        ('projet', 'Projet'),
        ('examen', 'Examen'),
        ('oral', 'Oral'),
    ]
    CATEGORIES = [
        ('cc', 'Contrôle Continu'),
        ('examen', 'Examen'),
    ]
    
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='evaluations')
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE, related_name='evaluations')
    titre = models.CharField(max_length=200)
    type_evaluation = models.CharField(max_length=20, choices=TYPES, default='devoir')
    categorie = models.CharField(max_length=10, choices=CATEGORIES, default='cc')
    coefficient = models.IntegerField(default=1)
    note_sur = models.DecimalField(max_digits=4, decimal_places=2, default=20.00)
    date_evaluation = models.DateField()
    description = models.TextField(blank=True)
    cree_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date_evaluation', 'titre']
    
    def __str__(self):
        return f"{self.matiere.code} - {self.titre}"


# ===== NOTE D'ÉVALUATION =====
class NoteEvaluation(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='notes')
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes_evaluations')
    note = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    absent = models.BooleanField(default=False)
    commentaire = models.TextField(blank=True)
    saisie_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)
    date_saisie = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('evaluation', 'etudiant')
        ordering = ['etudiant__nom', 'etudiant__prenom']
    
    def __str__(self):
        return f"{self.etudiant.matricule} - {self.evaluation.titre}: {self.note}"
    
    @property
    def note_sur_20(self):
        """Convertir la note sur 20"""
        if self.note is not None and self.evaluation.note_sur > 0:
            return round(float(self.note) * 20 / float(self.evaluation.note_sur), 2)
        return None

    @property
    def valide(self):
        m = self.moyenne
        return m is not None and m >= 10


# ===== RÉCLAMATION NOTE =====
class ReclamationNote(models.Model):
    TYPES_PROBLEME = [
        ('note_incorrecte', 'Note incorrecte / erreur de saisie'),
        ('note_manquante', 'Note manquante'),
        ('mauvaise_matiere', 'Note attribuée à la mauvaise matière'),
        ('calcul_errone', 'Erreur de calcul de moyenne'),
        ('autre', 'Autre problème'),
    ]
    STATUTS = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de traitement'),
        ('resolu', 'Résolu'),
        ('rejete', 'Rejeté'),
    ]
    
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='reclamations')
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='reclamations')
    type_probleme = models.CharField(max_length=30, choices=TYPES_PROBLEME)
    description = models.TextField()
    note_attendue = models.CharField(max_length=100, blank=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    reponse_enseignant = models.TextField(blank=True)
    traite_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='reclamations_traitees')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Réclamation de note'
        verbose_name_plural = 'Réclamations de notes'

    def __str__(self):
        return f"Réclamation #{self.id} - {self.etudiant.matricule} - {self.note.matiere.nom}"


# ===== PAIEMENT =====
class Paiement(models.Model):
    MODES = [
        ('especes','Espèces'),
        ('orange_money','Mobile Money (Orange)'),
        ('moov_money','Mobile Money (Moov)'),
        ('virement','Virement Bancaire'),
        ('cheque','Chèque'),
    ]
    TYPES = [
        ('inscription','Inscription'),
        ('reinscription','Réinscription'),
        ('acompte','Acompte'),
        ('solde','Solde'),
        ('autre','Autre'),
    ]
    STATUTS = [('valide','Validé'),('en_attente','En attente'),('rejete','Rejeté')]

    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='paiements')
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE, related_name='paiements')
    numero_recu = models.CharField(max_length=30, unique=True)
    montant = models.DecimalField(max_digits=12, decimal_places=0)
    mode = models.CharField(max_length=30, choices=MODES)
    type_paiement = models.CharField(max_length=20, choices=TYPES, default='inscription')
    statut = models.CharField(max_length=20, choices=STATUTS, default='valide')
    reference_mobile = models.CharField(max_length=50, blank=True)
    date_paiement = models.DateField()
    enregistre_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)
    observations = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.numero_recu} – {self.etudiant.matricule} – {self.montant} FCFA"


# ===== EMPLOI DU TEMPS =====
class EmploiDuTemps(models.Model):
    JOURS = [
        ('Lundi','Lundi'),('Mardi','Mardi'),('Mercredi','Mercredi'),
        ('Jeudi','Jeudi'),('Vendredi','Vendredi'),('Samedi','Samedi'),
    ]
    SEMAINES = [('toutes','Toutes'),('paire','Paire'),('impaire','Impaire')]
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='emplois')
    salle = models.CharField(max_length=50)
    jour = models.CharField(max_length=10, choices=JOURS)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    semaine = models.CharField(max_length=10, choices=SEMAINES, default='toutes')
    annee_academique = models.ForeignKey(AnneeAcademique, on_delete=models.CASCADE, related_name='emplois')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['jour', 'heure_debut']

    def __str__(self):
        return f"{self.matiere.code} – {self.jour} {self.heure_debut}"


# ===== PRÉSENCE =====
class Presence(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='presences')
    emploi = models.ForeignKey(EmploiDuTemps, on_delete=models.CASCADE, related_name='presences')
    date_cours = models.DateField()
    present = models.BooleanField(default=False)
    justifie = models.BooleanField(default=False)
    observation = models.CharField(max_length=200, blank=True)
    enregistre_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('etudiant', 'emploi', 'date_cours')
        ordering = ['-date_cours']

    def __str__(self):
        return f"{self.etudiant.matricule} – {self.date_cours} – {'Présent' if self.present else 'Absent'}"


# ===== SUPPORT DE COURS =====
class SupportCours(models.Model):
    TYPES = [
        ('cours','Cours magistral'),('td','TD'),('tp','TP'),
        ('examen_corrige','Examen corrigé'),('ressource','Ressource complémentaire'),
    ]
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='supports')
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='supports')
    titre = models.CharField(max_length=200)
    type_support = models.CharField(max_length=30, choices=TYPES, default='cours')
    fichier = models.FileField(upload_to='supports/', null=True, blank=True)
    description = models.TextField(blank=True)
    date_depot = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_depot']

    def __str__(self):
        return f"{self.titre} – {self.matiere.code}"


# ===== NOTIFICATION =====
class Notification(models.Model):
    TYPES = [('info','Info'),('success','Succès'),('warning','Avertissement'),('danger','Danger')]
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_notif = models.CharField(max_length=20, choices=TYPES, default='info')
    lue = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} → {self.destinataire.email}"


# ===== MEMBRE BUREAU EXÉCUTIF =====
class MembreBureau(models.Model):
    POSTES = [
        ('president', 'Président(e)'),
        ('vice_president', 'Vice-Président(e)'),
        ('secretaire', 'Secrétaire Général(e)'),
        ('tresorier', 'Trésorier(ère)'),
        ('charge_communication', 'Chargé(e) de Communication'),
        ('charge_evenements', 'Chargé(e) des Événements'),
        ('charge_academique', 'Chargé(e) des Affaires Académiques'),
        ('membre', 'Membre'),
    ]
    
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='membre_bureau')
    etudiant = models.OneToOneField(Etudiant, on_delete=models.CASCADE, related_name='membre_bureau', null=True, blank=True)
    poste = models.CharField(max_length=50, choices=POSTES)
    date_debut_mandat = models.DateField()
    date_fin_mandat = models.DateField(null=True, blank=True)
    actif = models.BooleanField(default=True)
    biographie = models.TextField(blank=True)
    photo = models.ImageField(upload_to='bureau/', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Membre du Bureau'
        verbose_name_plural = 'Membres du Bureau'
        ordering = ['poste', 'utilisateur__nom']
    
    def __str__(self):
        return f"{self.utilisateur.prenom} {self.utilisateur.nom} - {self.get_poste_display()}"


# ===== PUBLICATION =====
class Publication(models.Model):
    CATEGORIES = [
        ('actualite', 'Actualité'),
        ('evenement', 'Événement'),
        ('annonce', 'Annonce'),
        ('info', 'Information'),
        ('urgent', 'Urgent'),
    ]
    
    STATUTS = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('archive', 'Archivé'),
    ]
    
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    statut = models.CharField(max_length=20, choices=STATUTS, default='brouillon')
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='publications')
    image = models.ImageField(upload_to='publications/', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_publication = models.DateTimeField(null=True, blank=True)
    vues = models.IntegerField(default=0)
    epingle = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        ordering = ['-date_creation']
    
    def __str__(self):
        return self.titre


# ===== SONDAGE =====
class Sondage(models.Model):
    STATUTS = [
        ('brouillon', 'Brouillon'),
        ('actif', 'Actif'),
        ('termine', 'Terminé'),
        ('archive', 'Archivé'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    createur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='sondages')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUTS, default='brouillon')
    anonyme = models.BooleanField(default=True)
    multiple_reponses = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Sondage'
        verbose_name_plural = 'Sondages'
        ordering = ['-date_creation']
    
    def __str__(self):
        return self.titre


# ===== QUESTION SONDAGE =====
class QuestionSondage(models.Model):
    TYPES = [
        ('choix_unique', 'Choix unique'),
        ('choix_multiple', 'Choix multiple'),
        ('texte', 'Texte libre'),
        ('note', 'Note (1-5)'),
    ]
    
    sondage = models.ForeignKey(Sondage, on_delete=models.CASCADE, related_name='questions')
    texte = models.TextField()
    type_question = models.CharField(max_length=20, choices=TYPES)
    ordre = models.IntegerField(default=0)
    obligatoire = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Question de Sondage'
        verbose_name_plural = 'Questions de Sondage'
        ordering = ['sondage', 'ordre']
    
    def __str__(self):
        return f"{self.sondage.titre} - Q{self.ordre}"


# ===== OPTION QUESTION =====
class OptionQuestion(models.Model):
    question = models.ForeignKey(QuestionSondage, on_delete=models.CASCADE, related_name='options')
    texte = models.CharField(max_length=200)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Option de Question'
        verbose_name_plural = 'Options de Question'
        ordering = ['question', 'ordre']
    
    def __str__(self):
        return self.texte


# ===== RÉPONSE SONDAGE =====
class ReponseSondage(models.Model):
    sondage = models.ForeignKey(Sondage, on_delete=models.CASCADE, related_name='reponses')
    question = models.ForeignKey(QuestionSondage, on_delete=models.CASCADE, related_name='reponses')
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='reponses_sondages', null=True, blank=True)
    option = models.ForeignKey(OptionQuestion, on_delete=models.CASCADE, null=True, blank=True, related_name='reponses')
    texte_reponse = models.TextField(blank=True)
    note = models.IntegerField(null=True, blank=True)
    date_reponse = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Réponse de Sondage'
        verbose_name_plural = 'Réponses de Sondage'
        ordering = ['-date_reponse']
    
    def __str__(self):
        return f"Réponse - {self.sondage.titre}"


# ===== ÉVÉNEMENT =====
class Evenement(models.Model):
    TYPES = [
        ('conference', 'Conférence'),
        ('atelier', 'Atelier'),
        ('competition', 'Compétition'),
        ('culturel', 'Événement Culturel'),
        ('sportif', 'Événement Sportif'),
        ('social', 'Événement Social'),
        ('autre', 'Autre'),
    ]
    
    STATUTS = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    type_evenement = models.CharField(max_length=20, choices=TYPES)
    organisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='evenements')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=200)
    capacite_max = models.IntegerField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='planifie')
    image = models.ImageField(upload_to='evenements/', null=True, blank=True)
    inscription_requise = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Événement'
        verbose_name_plural = 'Événements'
        ordering = ['-date_debut']
    
    def __str__(self):
        return self.titre


# ===== INSCRIPTION ÉVÉNEMENT =====
class InscriptionEvenement(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
    ]
    
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='inscriptions')
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='inscriptions_evenements')
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    date_inscription = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Inscription Événement'
        verbose_name_plural = 'Inscriptions Événements'
        unique_together = ['evenement', 'etudiant']
        ordering = ['-date_inscription']
    
    def __str__(self):
        return f"{self.etudiant} - {self.evenement.titre}"


# ===== MESSAGE BUREAU =====
class MessageBureau(models.Model):
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_recus', null=True, blank=True)
    groupe = models.BooleanField(default=False)  # True si message à tout le bureau
    sujet = models.CharField(max_length=200, blank=True)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Message Bureau'
        verbose_name_plural = 'Messages Bureau'
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"{self.expediteur} -> {self.destinataire or 'Groupe'}"


# ===== DEMANDE ADMINISTRATIVE =====
class DemandeAdministrative(models.Model):
    TYPES = [
        ('attestation', 'Attestation d\'inscription'),
        ('releve', 'Relevé de notes'),
        ('certificat', 'Certificat de scolarité'),
        ('carte', 'Carte d\'étudiant'),
        ('stage', 'Convention de stage'),
        ('autre', 'Autre'),
    ]
    
    STATUTS = [
        ('en_attente', 'En attente'),
        ('en_traitement', 'En traitement'),
        ('approuve', 'Approuvé'),
        ('rejete', 'Rejeté'),
        ('termine', 'Terminé'),
    ]
    
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='demandes')
    type_demande = models.CharField(max_length=20, choices=TYPES)
    objet = models.CharField(max_length=200)
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    date_demande = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)
    traite_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='demandes_traitees')
    commentaire_admin = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Demande Administrative'
        verbose_name_plural = 'Demandes Administratives'
        ordering = ['-date_demande']
    
    def __str__(self):
        return f"{self.etudiant} - {self.get_type_demande_display()}"


# ===== OBJET PERDU =====
class ObjetPerdu(models.Model):
    TYPES = [
        ('perdu', 'Objet perdu'),
        ('trouve', 'Objet trouvé'),
    ]
    
    STATUTS = [
        ('actif', 'Actif'),
        ('recupere', 'Récupéré'),
        ('archive', 'Archivé'),
    ]
    
    declarant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='objets_declares')
    type_declaration = models.CharField(max_length=10, choices=TYPES)
    nom_objet = models.CharField(max_length=200)
    description = models.TextField()
    lieu = models.CharField(max_length=200)
    date_declaration = models.DateTimeField(auto_now_add=True)
    date_perte = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUTS, default='actif')
    image = models.ImageField(upload_to='objets_perdus/', null=True, blank=True)
    contact = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Objet Perdu'
        verbose_name_plural = 'Objets Perdus'
        ordering = ['-date_declaration']
    
    def __str__(self):
        return f"{self.nom_objet} - {self.get_type_declaration_display()}"


# ===== MODÈLES POUR LA GESTION DES CLASSES ET INSCRIPTIONS =====

class Classe(models.Model):
    """Modèle pour les classes/groupes d'étudiants"""
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=200)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='classes')
    niveau = models.CharField(max_length=10)  # L1, L2, L3, M1, M2
    annee_academique = models.CharField(max_length=20)
    effectif_max = models.IntegerField(default=50)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Classe'
        verbose_name_plural = 'Classes'
        ordering = ['niveau', 'code']
        unique_together = ['code', 'annee_academique']
    
    def __str__(self):
        return f"{self.code} - {self.nom}"
    
    @property
    def effectif_actuel(self):
        return self.inscriptions.filter(statut='actif').count()


class Inscription(models.Model):
    """Modèle pour l'inscription des étudiants dans les classes"""
    STATUTS = [
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
        ('abandonne', 'Abandonné'),
        ('diplome', 'Diplômé'),
    ]
    
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='inscriptions')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='inscriptions')
    annee_academique = models.CharField(max_length=20)
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='actif')
    
    class Meta:
        verbose_name = 'Inscription'
        verbose_name_plural = 'Inscriptions'
        ordering = ['-date_inscription']
        unique_together = ['etudiant', 'classe', 'annee_academique']
    
    def __str__(self):
        return f"{self.etudiant.get_full_name()} - {self.classe.code}"


class EnseignementMatiere(models.Model):
    """Modèle pour l'assignation des enseignants aux matières et classes"""
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='enseignements')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='enseignements')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='enseignements')
    annee_academique = models.CharField(max_length=20)
    semestre = models.IntegerField(choices=[(1, 'Semestre 1'), (2, 'Semestre 2')])
    date_assignation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Enseignement de Matière'
        verbose_name_plural = 'Enseignements de Matières'
        ordering = ['classe', 'matiere']
        unique_together = ['enseignant', 'matiere', 'classe', 'annee_academique', 'semestre']
    
    def __str__(self):
        return f"{self.enseignant.get_full_name()} - {self.matiere.nom} ({self.classe.code})"


# ===== HISTORIQUE DES NOTES =====
class HistoriqueNote(models.Model):
    """Modèle pour tracer toutes les modifications apportées aux notes"""
    ACTIONS = [
        ('creation', 'Création'),
        ('modification', 'Modification'),
        ('publication', 'Publication'),
        ('confirmation', 'Confirmation étudiant'),
        ('reclamation', 'Réclamation'),
        ('correction', 'Correction après réclamation'),
    ]
    
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='historique')
    action = models.CharField(max_length=20, choices=ACTIONS)
    
    # Valeurs avant modification
    note_cc_avant = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    note_examen_avant = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    statut_avant = models.CharField(max_length=20, blank=True)
    publie_avant = models.BooleanField(default=False)
    
    # Valeurs après modification
    note_cc_apres = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    note_examen_apres = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    statut_apres = models.CharField(max_length=20, blank=True)
    publie_apres = models.BooleanField(default=False)
    
    # Métadonnées
    modifie_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True)
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Historique de Note'
        verbose_name_plural = 'Historiques de Notes'
        ordering = ['-date_modification']
        indexes = [
            models.Index(fields=['note', '-date_modification']),
            models.Index(fields=['modifie_par', '-date_modification']),
        ]
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.note.etudiant.matricule} - {self.date_modification.strftime('%d/%m/%Y %H:%M')}"
    
    @property
    def moyenne_avant(self):
        """Calculer la moyenne avant modification"""
        if self.note_cc_avant is not None and self.note_examen_avant is not None:
            return round(float(self.note_cc_avant) * 0.4 + float(self.note_examen_avant) * 0.6, 2)
        return None
    
    @property
    def moyenne_apres(self):
        """Calculer la moyenne après modification"""
        if self.note_cc_apres is not None and self.note_examen_apres is not None:
            return round(float(self.note_cc_apres) * 0.4 + float(self.note_examen_apres) * 0.6, 2)
        return None
