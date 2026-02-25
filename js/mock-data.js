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
    // Étudiants (15 étudiants pour un semestre complet)
    etudiants: [
        { id: 1, matricule: 'ETU2024001', prenom: 'Moussa', nom: 'Diallo', email: 'm.diallo@etu.bf', telephone: '70123456', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-03-15', statut: 'actif' },
        { id: 2, matricule: 'ETU2024002', prenom: 'Fatima', nom: 'Sawadogo', email: 'f.sawadogo@etu.bf', telephone: '70234567', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-07-22', statut: 'actif' },
        { id: 3, matricule: 'ETU2024003', prenom: 'Ibrahim', nom: 'Kaboré', email: 'i.kabore@etu.bf', telephone: '70345678', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2004-11-08', statut: 'actif' },
        { id: 4, matricule: 'ETU2024004', prenom: 'Aminata', nom: 'Traoré', email: 'a.traore@etu.bf', telephone: '70456789', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2004-05-30', statut: 'actif' },
        { id: 5, matricule: 'ETU2024005', prenom: 'Boureima', nom: 'Ouédraogo', email: 'b.ouedraogo@etu.bf', telephone: '70567890', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2003-09-12', statut: 'actif' },
        { id: 6, matricule: 'ETU2024006', prenom: 'Aïcha', nom: 'Koné', email: 'a.kone@etu.bf', telephone: '70678901', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-01-20', statut: 'actif' },
        { id: 7, matricule: 'ETU2024007', prenom: 'Seydou', nom: 'Barro', email: 's.barro@etu.bf', telephone: '70789012', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-06-18', statut: 'actif' },
        { id: 8, matricule: 'ETU2024008', prenom: 'Mariam', nom: 'Sana', email: 'm.sana@etu.bf', telephone: '70890123', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-04-25', statut: 'actif' },
        { id: 9, matricule: 'ETU2024009', prenom: 'Abdoul', nom: 'Nikiema', email: 'a.nikiema@etu.bf', telephone: '70901234', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-08-30', statut: 'actif' },
        { id: 10, matricule: 'ETU2024010', prenom: 'Salimata', nom: 'Zoungrana', email: 's.zoungrana@etu.bf', telephone: '70012345', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-02-14', statut: 'actif' },
        { id: 11, matricule: 'ETU2024011', prenom: 'Ousmane', nom: 'Tapsoba', email: 'o.tapsoba@etu.bf', telephone: '70112233', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-09-05', statut: 'actif' },
        { id: 12, matricule: 'ETU2024012', prenom: 'Rasmata', nom: 'Ilboudo', email: 'r.ilboudo@etu.bf', telephone: '70223344', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-11-12', statut: 'actif' },
        { id: 13, matricule: 'ETU2024013', prenom: 'Souleymane', nom: 'Kinda', email: 's.kinda@etu.bf', telephone: '70334455', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-03-28', statut: 'actif' },
        { id: 14, matricule: 'ETU2024014', prenom: 'Hawa', nom: 'Yameogo', email: 'h.yameogo@etu.bf', telephone: '70445566', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-07-16', statut: 'actif' },
        { id: 15, matricule: 'ETU2024015', prenom: 'Issouf', nom: 'Bambara', email: 'i.bambara@etu.bf', telephone: '70556677', niveau: 'L1', filiere: 1, filiere_nom: 'Licence Informatique', date_naissance: '2005-05-22', statut: 'actif' }
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

    // Notes (Toutes les notes pour les 15 étudiants et 4 matières)
    notes: [
        // Algorithmique (Matière 1)
        { id: 1, etudiant: 1, etudiant_nom: 'Moussa Diallo', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 14.5, note_examen: 16.0, moyenne: 15.4, publie: true, statut: 'publie' },
        { id: 2, etudiant: 2, etudiant_nom: 'Fatima Sawadogo', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 15.0, note_examen: 17.0, moyenne: 16.2, publie: true, statut: 'publie' },
        { id: 3, etudiant: 3, etudiant_nom: 'Ibrahim Kaboré', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 13.0, note_examen: 14.5, moyenne: 13.9, publie: true, statut: 'publie' },
        { id: 4, etudiant: 4, etudiant_nom: 'Aminata Traoré', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 16.0, note_examen: 15.5, moyenne: 15.7, publie: true, statut: 'publie' },
        { id: 5, etudiant: 5, etudiant_nom: 'Boureima Ouédraogo', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 12.5, note_examen: 13.0, moyenne: 12.8, publie: true, statut: 'publie' },
        { id: 6, etudiant: 6, etudiant_nom: 'Aïcha Koné', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 14.0, note_examen: 15.0, moyenne: 14.6, publie: true, statut: 'publie' },
        { id: 7, etudiant: 7, etudiant_nom: 'Seydou Barro', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 11.5, note_examen: 12.0, moyenne: 11.8, publie: true, statut: 'publie' },
        { id: 8, etudiant: 8, etudiant_nom: 'Mariam Sana', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 15.5, note_examen: 16.5, moyenne: 16.1, publie: true, statut: 'publie' },
        { id: 9, etudiant: 9, etudiant_nom: 'Abdoul Nikiema', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 13.5, note_examen: 14.0, moyenne: 13.8, publie: true, statut: 'publie' },
        { id: 10, etudiant: 10, etudiant_nom: 'Salimata Zoungrana', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 14.5, note_examen: 15.5, moyenne: 15.1, publie: true, statut: 'publie' },
        { id: 11, etudiant: 11, etudiant_nom: 'Ousmane Tapsoba', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 12.0, note_examen: 13.5, moyenne: 12.9, publie: true, statut: 'publie' },
        { id: 12, etudiant: 12, etudiant_nom: 'Rasmata Ilboudo', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 16.5, note_examen: 17.0, moyenne: 16.8, publie: true, statut: 'publie' },
        { id: 13, etudiant: 13, etudiant_nom: 'Souleymane Kinda', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 11.0, note_examen: 12.5, moyenne: 11.9, publie: true, statut: 'publie' },
        { id: 14, etudiant: 14, etudiant_nom: 'Hawa Yameogo', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 15.0, note_examen: 16.0, moyenne: 15.6, publie: true, statut: 'publie' },
        { id: 15, etudiant: 15, etudiant_nom: 'Issouf Bambara', matiere: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 13.0, note_examen: 14.5, moyenne: 13.9, publie: true, statut: 'publie' },
        
        // Programmation C (Matière 2)
        { id: 16, etudiant: 1, etudiant_nom: 'Moussa Diallo', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 12.0, note_examen: 13.5, moyenne: 12.9, publie: true, statut: 'publie' },
        { id: 17, etudiant: 2, etudiant_nom: 'Fatima Sawadogo', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 13.5, note_examen: 14.0, moyenne: 13.8, publie: true, statut: 'publie' },
        { id: 18, etudiant: 3, etudiant_nom: 'Ibrahim Kaboré', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 14.0, note_examen: 15.0, moyenne: 14.6, publie: true, statut: 'publie' },
        { id: 19, etudiant: 4, etudiant_nom: 'Aminata Traoré', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 15.5, note_examen: 16.0, moyenne: 15.8, publie: true, statut: 'publie' },
        { id: 20, etudiant: 5, etudiant_nom: 'Boureima Ouédraogo', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 11.0, note_examen: 12.0, moyenne: 11.6, publie: true, statut: 'publie' },
        { id: 21, etudiant: 6, etudiant_nom: 'Aïcha Koné', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 13.0, note_examen: 14.5, moyenne: 13.9, publie: true, statut: 'publie' },
        { id: 22, etudiant: 7, etudiant_nom: 'Seydou Barro', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 10.5, note_examen: 11.5, moyenne: 11.1, publie: true, statut: 'publie' },
        { id: 23, etudiant: 8, etudiant_nom: 'Mariam Sana', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 16.0, note_examen: 17.0, moyenne: 16.6, publie: true, statut: 'publie' },
        { id: 24, etudiant: 9, etudiant_nom: 'Abdoul Nikiema', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 12.5, note_examen: 13.0, moyenne: 12.8, publie: true, statut: 'publie' },
        { id: 25, etudiant: 10, etudiant_nom: 'Salimata Zoungrana', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 14.0, note_examen: 15.0, moyenne: 14.6, publie: true, statut: 'publie' },
        { id: 26, etudiant: 11, etudiant_nom: 'Ousmane Tapsoba', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 11.5, note_examen: 12.5, moyenne: 12.1, publie: true, statut: 'publie' },
        { id: 27, etudiant: 12, etudiant_nom: 'Rasmata Ilboudo', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 17.0, note_examen: 18.0, moyenne: 17.6, publie: true, statut: 'publie' },
        { id: 28, etudiant: 13, etudiant_nom: 'Souleymane Kinda', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 10.0, note_examen: 11.0, moyenne: 10.6, publie: true, statut: 'publie' },
        { id: 29, etudiant: 14, etudiant_nom: 'Hawa Yameogo', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 14.5, note_examen: 15.5, moyenne: 15.1, publie: true, statut: 'publie' },
        { id: 30, etudiant: 15, etudiant_nom: 'Issouf Bambara', matiere: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 12.5, note_examen: 13.5, moyenne: 13.1, publie: true, statut: 'publie' }
    ],

    // Paiements
    paiements: [
        { id: 1, etudiant: 1, numero_recu: 'REC2024001', montant: 150000, type_paiement: 'inscription', date_paiement: '2024-10-15', mode: 'especes', statut: 'valide' },
        { id: 2, etudiant: 1, numero_recu: 'REC2024002', montant: 50000, type_paiement: 'acompte', date_paiement: '2024-11-20', mode: 'orange_money', statut: 'valide' },
        { id: 3, etudiant: 2, numero_recu: 'REC2024003', montant: 200000, type_paiement: 'inscription', date_paiement: '2024-10-10', mode: 'virement', statut: 'valide' }
    ],

    // Emploi du temps
    emploisDuTemps: [
        { id: 1, jour: 'Lundi', heure_debut: '08:00', heure_fin: '10:00', matiere: 1, matiere_nom: 'Algorithmique', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', salle: 'A101', filiere: 1, semaine: 'toutes' },
        { id: 2, jour: 'Lundi', heure_debut: '10:15', heure_fin: '12:15', matiere: 2, matiere_nom: 'Programmation C', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', salle: 'B205', filiere: 1, semaine: 'toutes' },
        { id: 3, jour: 'Mardi', heure_debut: '08:00', heure_fin: '10:00', matiere: 3, matiere_nom: 'Base de Données', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', salle: 'A102', filiere: 1, semaine: 'toutes' },
        { id: 4, jour: 'Mercredi', heure_debut: '14:00', heure_fin: '16:00', matiere: 1, matiere_nom: 'Algorithmique', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', salle: 'A101', filiere: 1, semaine: 'toutes' },
        { id: 5, jour: 'Jeudi', heure_debut: '08:00', heure_fin: '10:00', matiere: 2, matiere_nom: 'Programmation C', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', salle: 'B205', filiere: 1, semaine: 'toutes' },
        { id: 6, jour: 'Vendredi', heure_debut: '10:15', heure_fin: '12:15', matiere: 4, matiere_nom: 'Réseaux Informatiques', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', salle: 'C301', filiere: 1, semaine: 'toutes' }
    ],

    // Supports de cours
    supports: [
        { id: 1, titre: 'Introduction à l\'Algorithmique', matiere: 1, matiere_nom: 'Algorithmique', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', type_support: 'cours', date_depot: '2024-10-01', fichier: 'algo_intro.pdf' },
        { id: 2, titre: 'TD Algorithmique - Structures de contrôle', matiere: 1, matiere_nom: 'Algorithmique', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', type_support: 'td', date_depot: '2024-10-08', fichier: 'algo_td1.pdf' },
        { id: 3, titre: 'Cours Programmation C - Les bases', matiere: 2, matiere_nom: 'Programmation C', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', type_support: 'cours', date_depot: '2024-10-05', fichier: 'c_bases.pdf' },
        { id: 4, titre: 'TP Programmation C - Premiers programmes', matiere: 2, matiere_nom: 'Programmation C', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', type_support: 'tp', date_depot: '2024-10-12', fichier: 'c_tp1.pdf' },
        { id: 5, titre: 'Examen Algorithmique 2023 Corrigé', matiere: 1, matiere_nom: 'Algorithmique', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', type_support: 'examen_corrige', date_depot: '2024-11-01', fichier: 'algo_exam2023.pdf' },
        { id: 6, titre: 'Ressources complémentaires - Pointeurs en C', matiere: 2, matiere_nom: 'Programmation C', enseignant: 1, enseignant_nom: 'Jean Ouedraogo', type_support: 'ressource', date_depot: '2024-11-15', fichier: 'c_pointeurs.pdf' }
    ],

    // Dashboard Admin
    dashboardAdmin: {
        total_etudiants: 15,
        total_enseignants: 4,
        total_filieres: 3,
        total_matieres: 4,
        etudiants_actifs: 15,
        etudiants_bloques: 0,
        paiements_mois: 600000,
        taux_paiement: 85
    },

    // Dashboard Prof
    dashboardProf: {
        matieres: [
            { id: 1, nom: 'Algorithmique', code: 'ALGO101', coefficient: 3, filiere: 1, filiere_nom: 'Licence Informatique', enseignant: 1 },
            { id: 2, nom: 'Programmation C', code: 'PROG101', coefficient: 4, filiere: 1, filiere_nom: 'Licence Informatique', enseignant: 1 }
        ],
        total_etudiants: 15,
        notes_saisies: 30,
        cours_semaine: 6,
        notes: []
    },

    // Dashboard Étudiant
    dashboardEtudiant: {
        moyenne_generale: 14.6,
        credits_valides: 24,
        credits_total: 30,
        notes_publiees: 2,
        paiements_effectues: 200000,
        solde_restant: 100000,
        total_matieres: 4,
        taux_presence: 92,
        solde_du: 100000,
        notes: [
            { id: 1, matiere_nom: 'Algorithmique', coefficient: 3, note_cc: 14.5, note_examen: 16.0, moyenne: 15.4, publie: true },
            { id: 2, matiere_nom: 'Programmation C', coefficient: 4, note_cc: 12.0, note_examen: 13.5, moyenne: 12.9, publie: true }
        ]
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
            const result = {
                access: token,
                refresh: token,
                user: user
            };
            // Sauvegarder dans localStorage comme le vrai API
            localStorage.setItem('erp_access_token', token);
            localStorage.setItem('erp_refresh_token', token);
            localStorage.setItem('erp_user', JSON.stringify(user));
            return result;
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
        return {
            ...MOCK_DATA.dashboardAdmin,
            etudiants: MOCK_DATA.etudiants.slice(0, 5), // 5 derniers étudiants
            enseignants: MOCK_DATA.enseignants,
            paiements_recents: MOCK_DATA.paiements
        };
    },

    async getDashboardProf() {
        await mockDelay();
        const user = JSON.parse(localStorage.getItem('erp_user'));
        return {
            ...MOCK_DATA.dashboardProf,
            matieres: MOCK_DATA.matieres.filter(m => m.id <= 2), // Matières de l'enseignant
            etudiants: MOCK_DATA.etudiants, // Tous les étudiants
            notes: MOCK_DATA.notes.filter(n => n.matiere <= 2), // Notes des matières de l'enseignant
            emplois: MOCK_DATA.emploisDuTemps,
            supports: MOCK_DATA.supports
        };
    },

    async getDashboardEtudiant() {
        await mockDelay();
        const user = JSON.parse(localStorage.getItem('erp_user'));
        const etudiantId = user?.etudiant?.id || 1;
        
        return {
            ...MOCK_DATA.dashboardEtudiant,
            notes: MOCK_DATA.notes.filter(n => n.etudiant === etudiantId),
            paiements: MOCK_DATA.paiements.filter(p => p.etudiant === etudiantId),
            emplois: MOCK_DATA.emploisDuTemps,
            supports: MOCK_DATA.supports
        };
    },

    // Étudiants
    async getEtudiants(params = {}) {
        await mockDelay();
        let etudiants = MOCK_DATA.etudiants;
        if (params.filiere) {
            etudiants = etudiants.filter(e => e.filiere == params.filiere);
        }
        return etudiants;
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
        // Ajouter les noms des étudiants et matières
        return notes.map(n => ({
            ...n,
            etudiant_nom: MOCK_DATA.etudiants.find(e => e.id === n.etudiant)?.prenom + ' ' + MOCK_DATA.etudiants.find(e => e.id === n.etudiant)?.nom,
            matiere_nom: MOCK_DATA.matieres.find(m => m.id === n.matiere)?.nom
        }));
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

    // Emploi du temps
    async getEmploisDuTemps(params = {}) {
        await mockDelay();
        let emplois = MOCK_DATA.emploisDuTemps;
        if (params.filiere) {
            emplois = emplois.filter(e => e.filiere == params.filiere);
        }
        return emplois;
    },

    // Supports de cours
    async getSupports(params = {}) {
        await mockDelay();
        return MOCK_DATA.supports;
    },

    // Années académiques
    async getAnnees() {
        await mockDelay();
        return [
            { id: 1, nom: '2024-2025', date_debut: '2024-10-01', date_fin: '2025-06-30', active: true }
        ];
    },

    async getPaiementsEtudiant(id) {
        await mockDelay();
        return MOCK_DATA.paiements.filter(p => p.etudiant == id);
    },

    // Années académiques
    async getAnnees() {
        await mockDelay();
        return [
            { id: 1, nom: '2024-2025', date_debut: '2024-10-01', date_fin: '2025-06-30', active: true }
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
 