/**
 * DONNÉES MOCK POUR DÉMO SANS BACKEND
 * Simule les réponses de l'API
 */

// Mode MOCK activé
const MOCK_MODE = true;

// Utilisateurs de test
const MOCK_USERS = {
    'admin@uan.bf': {
        email: 'admin@uan.bf',
        password: 'admin123',
        role: 'administrateur',
        id: 1,
        prenom: 'Admin',
        nom: 'Système'
    },
    'j.ouedraogo@uan.bf': {
        email: 'j.ouedraogo@uan.bf',
        password: 'enseignant123',
        role: 'professeur',
        id: 2,
        prenom: 'Jean',
        nom: 'Ouedraogo',
        enseignant: {
            id: 1,
            grade: 'Maître de Conférences',
            specialite: 'Informatique'
        }
    },
    'm.diallo@etu.bf': {
        email: 'm.diallo@etu.bf',
        password: 'etudiant123',
        role: 'etudiant',
        id: 3,
        prenom: 'Moussa',
        nom: 'Diallo',
        etudiant: {
            id: 1,
            matricule: 'ETU2024001',
            niveau: 'L1',
            filiere: 'Informatique'
        }
    }
};

// Données mock
const MOCK_DATA = {
    // Étudiants
    etudiants: [
        { id: 1, matricule: 'ETU2024001', prenom: 'Moussa', nom: 'Diallo', email: 'm.diallo@etu.bf', telephone: '70123456', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-03-15', statut: 'actif' },
        { id: 2, matricule: 'ETU2024002', prenom: 'Fatima', nom: 'Sawadogo', email: 'f.sawadogo@etu.bf', telephone: '70234567', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-07-22', statut: 'actif' },
        { id: 3, matricule: 'ETU2024003', prenom: 'Ibrahim', nom: 'Kaboré', email: 'i.kabore@etu.bf', telephone: '70345678', niveau: 'L2', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2004-11-08', statut: 'actif' },
        { id: 4, matricule: 'ETU2024004', prenom: 'Aminata', nom: 'Traoré', email: 'a.traore@etu.bf', telephone: '70456789', niveau: 'L2', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2004-05-30', statut: 'actif' },
        { id: 5, matricule: 'ETU2024005', prenom: 'Boureima', nom: 'Ouédraogo', email: 'b.ouedraogo@etu.bf', telephone: '70567890', niveau: 'L3', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2003-09-12', statut: 'actif' }
    ],

    // Enseignants
    enseignants: [
        { id: 1, prenom: 'Jean', nom: 'Ouedraogo', email: 'j.ouedraogo@uan.bf', telephone: '70111111', grade: 'Maître de Conférences', specialite: 'Informatique', statut: 'actif' },
        { id: 2, prenom: 'Marie', nom: 'Compaoré', email: 'm.compaore@uan.bf', telephone: '70222222', grade: 'Professeur Titulaire', specialite: 'Mathématiques', statut: 'actif' },
        { id: 3, prenom: 'Paul', nom: 'Zongo', email: 'p.zongo@uan.bf', telephone: '70333333', grade: 'Maître-Assistant', specialite: 'Physique', statut: 'actif' },
        { id: 4, prenom: 'Sophie', nom: 'Sankara', email: 's.sankara@uan.bf', telephone: '70444444', grade: 'Assistant', specialite: 'Chimie', statut: 'actif' }
    ],

    // Filières
    filieres: [
        { id: 1, nom: 'Licence Informatique', code: 'L-INFO', niveau: 'Licence', universite: 1, universite_nom: 'Université Aube Nouvelle' },
        { id: 2, nom: 'Licence Mathématiques', code: 'L-MATH', niveau: 'Licence', universite: 1, universite_nom: 'Université Aube Nouvelle' },
        { id: 3, nom: 'Master Informatique', code: 'M-INFO', niveau: 'Master', universite: 1, universite_nom: 'Université Aube Nouvelle' }
    ],

    // Matières
    matieres: [
        { id: 1, nom: 'Algorithmique', code: 'ALGO101', coefficient: 3, filiere: 1, filiere_nom: 'Licence Informatique', semestre: 1 },
        { id: 2, nom: 'Programmation C', code: 'PROG101', coefficient: 4, filiere: 1, filiere_nom: 'Licence Informatique', semestre: 1 },
        { id: 3, nom: 'Base de Données', code: 'BDD201', coefficient: 3, filiere: 1, filiere_nom: 'Licence Informatique', semestre: 2 },
        { id: 4, nom: 'Réseaux Informatiques', code: 'RES201', coefficient: 3, filiere: 1, filiere_nom: 'Licence Informatique', semestre: 2 }
    ],

    // Notes
    notes: [
        { id: 1, etudiant: 1, matiere: 1, note_cc: 14.5, note_examen: 16.0, moyenne: 15.4, publie: true, statut: 'publie' },
        { id: 2, etudiant: 1, matiere: 2, note_cc: 12.0, note_examen: 13.5, moyenne: 12.9, publie: true, statut: 'publie' },
        { id: 3, etudiant: 2, matiere: 1, note_cc: 15.0, note_examen: 17.0, moyenne: 16.2, publie: true, statut: 'publie' },
        { id: 4, etudiant: 2, matiere: 2, note_cc: 13.5, note_examen: 14.0, moyenne: 13.8, publie: true, statut: 'publie' }
    ],

    // Paiements
    paiements: [
        { id: 1, etudiant: 1, montant: 150000, type_paiement: 'Frais de scolarité', date_paiement: '2024-10-15', mode_paiement: 'Espèces', statut: 'validé' },
        { id: 2, etudiant: 1, montant: 50000, type_paiement: 'Frais de scolarité', date_paiement: '2024-11-20', mode_paiement: 'Mobile Money', statut: 'validé' },
        { id: 3, etudiant: 2, montant: 200000, type_paiement: 'Frais de scolarité', date_paiement: '2024-10-10', mode_paiement: 'Virement', statut: 'validé' }
    ],

    // Dashboard Admin
    dashboardAdmin: {
        total_etudiants: 5,
        total_enseignants: 4,
        total_filieres: 3,
        total_matieres: 4,
        etudiants_actifs: 5,
        etudiants_bloques: 0,
        paiements_mois: 400000,
        taux_paiement: 75
    },

    // Dashboard Prof
    dashboardProf: {
        matieres: [
            { id: 1, nom: 'Algorithmique', code: 'ALGO101', coefficient: 3, filiere: 1, filiere_nom: 'Licence Informatique' },
            { id: 2, nom: 'Programmation C', code: 'PROG101', coefficient: 4, filiere: 1, filiere_nom: 'Licence Informatique' }
        ],
        total_etudiants: 5,
        notes_saisies: 4,
        cours_semaine: 6
    },

    // Dashboard Étudiant
    dashboardEtudiant: {
        moyenne_generale: 14.6,
        credits_valides: 24,
        credits_total: 30,
        notes_publiees: 2,
        paiements_effectues: 200000,
        solde_restant: 100000
    }
};

// Fonction pour simuler un délai réseau
function mockDelay(ms = 300) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// API Mock
const MockAPI = {
    // Auth
    async login(email, password) {
        await mockDelay();
        const user = MOCK_USERS[email];
        if (user && user.password === password) {
            const token = 'mock-token-' + Date.now();
            return {
                access: token,
                refresh: token,
                user: user
            };
        }
        throw new Error('Email ou mot de passe incorrect');
    },

    async getMe() {
        await mockDelay();
        const user = JSON.parse(localStorage.getItem('erp_user'));
        return user;
    },

    // Dashboard
    async getDashboardAdmin() {
        await mockDelay();
        return MOCK_DATA.dashboardAdmin;
    },

    async getDashboardProf() {
        await mockDelay();
        return MOCK_DATA.dashboardProf;
    },

    async getDashboardEtudiant() {
        await mockDelay();
        return MOCK_DATA.dashboardEtudiant;
    },

    // Étudiants
    async getEtudiants(params = {}) {
        await mockDelay();
        return MOCK_DATA.etudiants;
    },

    async getEtudiant(id) {
        await mockDelay();
        return MOCK_DATA.etudiants.find(e => e.id == id);
    },

    // Enseignants
    async getEnseignants() {
        await mockDelay();
        return MOCK_DATA.enseignants;
    },

    async getEnseignant(id) {
        await mockDelay();
        return MOCK_DATA.enseignants.find(e => e.id == id);
    },

    // Filières
    async getFilieres() {
        await mockDelay();
        return MOCK_DATA.filieres;
    },

    // Matières
    async getMatieres() {
        await mockDelay();
        return MOCK_DATA.matieres;
    },

    // Notes
    async getNotes(params = {}) {
        await mockDelay();
        let notes = MOCK_DATA.notes;
        if (params.etudiant) {
            notes = notes.filter(n => n.etudiant == params.etudiant);
        }
        if (params.matiere) {
            notes = notes.filter(n => n.matiere == params.matiere);
        }
        return notes;
    },

    // Paiements
    async getPaiements(params = {}) {
        await mockDelay();
        let paiements = MOCK_DATA.paiements;
        if (params.etudiant) {
            paiements = paiements.filter(p => p.etudiant == params.etudiant);
        }
        return paiements;
    },

    async getPaiementsEtudiant(id) {
        await mockDelay();
        return MOCK_DATA.paiements.filter(p => p.etudiant == id);
    },

    // Années académiques
    async getAnnees() {
        await mockDelay();
        return [
            { id: 1, annee: '2024-2025', active: true }
        ];
    },

    // Évaluations
    async getEvaluations(params = {}) {
        await mockDelay();
        return [];
    },

    // Supports
    async getSupports() {
        await mockDelay();
        return [];
    },

    // Emplois du temps
    async getEmploisDuTemps() {
        await mockDelay();
        return [];
    },

    // Méthodes vides pour les autres appels
    async createEtudiant() { await mockDelay(); return { id: Date.now() }; },
    async updateEtudiant() { await mockDelay(); return {}; },
    async deleteEtudiant() { await mockDelay(); return {}; },
    async createEnseignant() { await mockDelay(); return { id: Date.now() }; },
    async updateEnseignant() { await mockDelay(); return {}; },
    async createFiliere() { await mockDelay(); return { id: Date.now() }; },
    async updateFiliere() { await mockDelay(); return {}; },
    async deleteFiliere() { await mockDelay(); return {}; },
    async createMatiere() { await mockDelay(); return { id: Date.now() }; },
    async updateMatiere() { await mockDelay(); return {}; },
    async deleteMatiere() { await mockDelay(); return {}; },
    async createNote() { await mockDelay(); return { id: Date.now() }; },
    async updateNote() { await mockDelay(); return {}; },
    async deleteNote() { await mockDelay(); return {}; },
    async createPaiement() { await mockDelay(); return { id: Date.now() }; },
    async createEvaluation() { await mockDelay(); return { id: Date.now() }; },
    async updateEvaluation() { await mockDelay(); return {}; },
    async deleteEvaluation() { await mockDelay(); return {}; },
    async getNotesEvaluations() { await mockDelay(); return []; },
    async createNoteEvaluation() { await mockDelay(); return { id: Date.now() }; },
    async updateNoteEvaluation() { await mockDelay(); return {}; },
};

console.log('🎭 MODE MOCK ACTIVÉ - Données de démonstration chargées');
 