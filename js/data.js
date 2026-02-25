// =====================================================
//  ERP UNIVERSITAIRE - DONNÉES DE DÉMONSTRATION
// =====================================================

const ERPData = {

    // === UNIVERSITÉS ===
    universites: [
        { id: 1, nom: "Université Aube Nouvelle (UAN)", ville: "Ouagadougou", code: "UAN", statut: "active", etudiants: 3420, licence: "PRO", expiration: "2025-12-31" },
        { id: 2, nom: "Institut Supérieur de Technologie (IST)", ville: "Bobo-Dioulasso", code: "IST", statut: "active", etudiants: 1850, licence: "STANDARD", expiration: "2025-06-30" },
        { id: 3, nom: "Université Polytechnique de Bobo (UPB)", ville: "Bobo-Dioulasso", code: "UPB", statut: "active", etudiants: 2100, licence: "PRO", expiration: "2026-01-15" },
        { id: 4, nom: "ISTIC Koudougou", ville: "Koudougou", code: "ISTIC", statut: "suspendu", etudiants: 890, licence: "BASIC", expiration: "2024-08-31" },
    ],

    // === FILIÈRES ===
    filieres: [
        { id: 1, code: "INFO", nom: "Licence Informatique", niveau: "Licence", duree: 3, frais: 350000 },
        { id: 2, code: "GESTION", nom: "Licence Sciences de Gestion", niveau: "Licence", duree: 3, frais: 300000 },
        { id: 3, code: "DROIT", nom: "Licence Droit Privé", niveau: "Licence", duree: 3, frais: 280000 },
        { id: 4, code: "MATH", nom: "Licence Mathématiques", niveau: "Licence", duree: 3, frais: 280000 },
        { id: 5, code: "MINFO", nom: "Master Informatique", niveau: "Master", duree: 2, frais: 500000 },
        { id: 6, code: "MBA", nom: "Master Business Administration", niveau: "Master", duree: 2, frais: 650000 },
        { id: 7, code: "DUTS", nom: "DUT Systèmes Réseaux", niveau: "DUT", duree: 2, frais: 400000 },
    ],

    // === MATIÈRES ===
    matieres: [
        { id: 1, code: "ALGO101", nom: "Algorithmique et Structures de Données", filiere_id: 1, credits: 4, coeff: 3, semestre: 1, enseignant_id: 1 },
        { id: 2, code: "POO101", nom: "Programmation Orientée Objet (Java)", filiere_id: 1, credits: 3, coeff: 2, semestre: 1, enseignant_id: 1 },
        { id: 3, code: "BD101", nom: "Bases de Données", filiere_id: 1, credits: 3, coeff: 2, semestre: 2, enseignant_id: 2 },
        { id: 4, code: "MATH101", nom: "Mathématiques Discrètes", filiere_id: 1, credits: 3, coeff: 2, semestre: 1, enseignant_id: 4 },
        { id: 5, code: "COMPTA101", nom: "Comptabilité Générale", filiere_id: 2, credits: 4, coeff: 3, semestre: 1, enseignant_id: 3 },
        { id: 6, code: "MKTG101", nom: "Marketing Fondamental", filiere_id: 2, credits: 3, coeff: 2, semestre: 2, enseignant_id: 3 },
        { id: 7, code: "RESEAU101", nom: "Réseaux Informatiques", filiere_id: 7, credits: 4, coeff: 3, semestre: 1, enseignant_id: 2 },
        { id: 8, code: "SYS101", nom: "Systèmes d'Exploitation", filiere_id: 7, credits: 3, coeff: 2, semestre: 1, enseignant_id: 2 },
    ],

    // === ÉTUDIANTS ===
    etudiants: [
        { id: 1, matricule: "UAN2024001", prenom: "Aminata", nom: "Ouedraogo", email: "aminata.o@uan.bf", tel: "+226 70 11 22 33", filiere_id: 1, niveau: "L1", annee: "2024-2025", statut: "inscrit", solde_du: 0, date_naissance: "2003-05-12", lieu_naissance: "Ouagadougou", genre: "F" },
        { id: 2, matricule: "UAN2024002", prenom: "Ibrahim", nom: "Sawadogo", email: "ibrahim.s@uan.bf", tel: "+226 76 44 55 66", filiere_id: 1, niveau: "L1", annee: "2024-2025", statut: "inscrit", solde_du: 175000, date_naissance: "2002-11-30", lieu_naissance: "Bobo-Dioulasso", genre: "M" },
        { id: 3, matricule: "UAN2023015", prenom: "Fatoumata", nom: "Traoré", email: "fatoumata.t@uan.bf", tel: "+226 65 77 88 99", filiere_id: 2, niveau: "L2", annee: "2024-2025", statut: "inscrit", solde_du: 0, date_naissance: "2002-03-18", lieu_naissance: "Koudougou", genre: "F" },
        { id: 4, matricule: "UAN2022010", prenom: "Moussa", nom: "Compaoré", email: "moussa.c@uan.bf", tel: "+226 71 22 33 44", filiere_id: 1, niveau: "L3", annee: "2024-2025", statut: "inscrit", solde_du: 0, date_naissance: "2001-07-25", lieu_naissance: "Ouagadougou", genre: "M" },
        { id: 5, matricule: "UAN2024003", prenom: "Salimata", nom: "Zongo", email: "salimata.z@uan.bf", tel: "+226 60 55 66 77", filiere_id: 3, niveau: "L1", annee: "2024-2025", statut: "bloque", solde_du: 280000, date_naissance: "2003-09-01", lieu_naissance: "Tenkodogo", genre: "F" },
        { id: 6, matricule: "UAN2023022", prenom: "Adama", nom: "Diallo", email: "adama.d@uan.bf", tel: "+226 77 33 44 55", filiere_id: 2, niveau: "L2", annee: "2024-2025", statut: "inscrit", solde_du: 50000, date_naissance: "2002-01-14", lieu_naissance: "Ouahigouya", genre: "M" },
        { id: 7, matricule: "UAN2022005", prenom: "Mariam", nom: "Kaboré", email: "mariam.k@uan.bf", tel: "+226 79 66 77 88", filiere_id: 5, niveau: "M1", annee: "2024-2025", statut: "inscrit", solde_du: 0, date_naissance: "2000-12-22", lieu_naissance: "Ouagadougou", genre: "F" },
        { id: 8, matricule: "UAN2024008", prenom: "Boukari", nom: "Ouattara", email: "boukari.o@uan.bf", tel: "+226 70 88 99 00", filiere_id: 7, niveau: "D1", annee: "2024-2025", statut: "inscrit", solde_du: 0, date_naissance: "2003-06-05", lieu_naissance: "Fada N'Gourma", genre: "M" },
    ],

    // === ENSEIGNANTS ===
    enseignants: [
        { id: 1, matricule: "ENS001", prenom: "Dr. Serge", nom: "Kouanda", email: "s.kouanda@uan.bf", tel: "+226 70 12 34 56", specialite: "Informatique", grade: "Maître de Conférences", statut: "actif", nb_cours: 3 },
        { id: 2, matricule: "ENS002", prenom: "Prof. Alice", nom: "Nikiéma", email: "a.nikema@uan.bf", tel: "+226 76 23 45 67", specialite: "Réseaux & Sécurité", grade: "Professeur Titulaire", statut: "actif", nb_cours: 4 },
        { id: 3, matricule: "ENS003", prenom: "Dr. Paul", nom: "Bélem", email: "p.belem@uan.bf", tel: "+226 65 34 56 78", specialite: "Gestion & Finance", grade: "Maître-Assistant", statut: "actif", nb_cours: 2 },
        { id: 4, matricule: "ENS004", prenom: "Dr. Cécile", nom: "Yameogo", email: "c.yameogo@uan.bf", tel: "+226 71 45 67 89", specialite: "Mathématiques", grade: "Maître de Conférences", statut: "conge", nb_cours: 1 },
        { id: 5, matricule: "ENS005", prenom: "Dr. Omar", nom: "Sidibé", email: "o.sidibe@uan.bf", tel: "+226 60 56 78 90", specialite: "Droit", grade: "Maître-Assistant", statut: "actif", nb_cours: 2 },
    ],

    // === NOTES ===
    notes: [
        { id: 1, etudiant_id: 1, matiere_id: 1, note_cc: 14, note_exam: 16, semestre: 1, annee: "2024-2025" },
        { id: 2, etudiant_id: 1, matiere_id: 2, note_cc: 12, note_exam: 14, semestre: 1, annee: "2024-2025" },
        { id: 3, etudiant_id: 1, matiere_id: 4, note_cc: 10, note_exam: 11, semestre: 1, annee: "2024-2025" },
        { id: 4, etudiant_id: 2, matiere_id: 1, note_cc: 8, note_exam: 9, semestre: 1, annee: "2024-2025" },
        { id: 5, etudiant_id: 2, matiere_id: 2, note_cc: 11, note_exam: 13, semestre: 1, annee: "2024-2025" },
        { id: 6, etudiant_id: 4, matiere_id: 1, note_cc: 17, note_exam: 18, semestre: 1, annee: "2024-2025" },
        { id: 7, etudiant_id: 4, matiere_id: 2, note_cc: 15, note_exam: 17, semestre: 1, annee: "2024-2025" },
        { id: 8, etudiant_id: 4, matiere_id: 4, note_cc: 16, note_exam: 15, semestre: 1, annee: "2024-2025" },
    ],

    // === PAIEMENTS ===
    paiements: [
        { id: 1, etudiant_id: 1, montant: 350000, date: "2024-09-05", mode: "Mobile Money (Orange)", recu: "REC-2024-001", type: "inscription", statut: "valide" },
        { id: 2, etudiant_id: 3, montant: 300000, date: "2024-09-08", mode: "Espèces", recu: "REC-2024-002", type: "inscription", statut: "valide" },
        { id: 3, etudiant_id: 4, montant: 350000, date: "2024-09-10", mode: "Mobile Money (Moov)", recu: "REC-2024-003", type: "inscription", statut: "valide" },
        { id: 4, etudiant_id: 2, montant: 175000, date: "2024-09-12", mode: "Espèces", recu: "REC-2024-004", type: "acompte", statut: "valide" },
        { id: 5, etudiant_id: 6, montant: 250000, date: "2024-09-15", mode: "Virement", recu: "REC-2024-005", type: "inscription", statut: "valide" },
        { id: 6, etudiant_id: 7, montant: 500000, date: "2024-09-03", mode: "Mobile Money (Orange)", recu: "REC-2024-006", type: "inscription", statut: "valide" },
        { id: 7, etudiant_id: 8, montant: 400000, date: "2024-09-20", mode: "Virement", recu: "REC-2024-007", type: "inscription", statut: "valide" },
    ],

    // === EMPLOI DU TEMPS ===
    emploiDuTemps: [
        { id: 1, matiere_id: 1, salle: "A101", jour: "Lundi", heure_debut: "08:00", heure_fin: "10:00", filiere_id: 1, niveau: "L1", semaine: "impaire" },
        { id: 2, matiere_id: 2, salle: "A102", jour: "Mardi", heure_debut: "10:00", heure_fin: "12:00", filiere_id: 1, niveau: "L1", semaine: "toutes" },
        { id: 3, matiere_id: 4, salle: "B201", jour: "Mercredi", heure_debut: "14:00", heure_fin: "16:00", filiere_id: 1, niveau: "L1", semaine: "toutes" },
        { id: 4, matiere_id: 5, salle: "C301", jour: "Jeudi", heure_debut: "08:00", heure_fin: "10:00", filiere_id: 2, niveau: "L1", semaine: "toutes" },
        { id: 5, matiere_id: 3, salle: "A103", jour: "Vendredi", heure_debut: "08:00", heure_fin: "10:00", filiere_id: 1, niveau: "L2", semaine: "paire" },
        { id: 6, matiere_id: 7, salle: "INFO-LAB1", jour: "Lundi", heure_debut: "14:00", heure_fin: "17:00", filiere_id: 7, niveau: "D1", semaine: "toutes" },
    ],

    // === NOTIFICATIONS ===
    notifications: [
        { id: 1, titre: "Inscription réussie", message: "Votre inscription pour 2024-2025 a été validée.", date: "2024-09-05", lue: true, type: "success" },
        { id: 2, titre: "Résultats disponibles", message: "Les notes du semestre 1 sont publiées.", date: "2025-01-20", lue: false, type: "info" },
        { id: 3, titre: "Rappel de paiement", message: "Il vous reste 175 000 FCFA à régler avant le 28/02.", date: "2025-02-10", lue: false, type: "warning" },
    ],

    // === HELPER FUNCTIONS ===
    getEtudiant(id) { return this.etudiants.find(e => e.id === id); },
    getEnseignant(id) { return this.enseignants.find(e => e.id === id); },
    getMatiere(id) { return this.matieres.find(m => m.id === id); },
    getFiliere(id) { return this.filieres.find(f => f.id === id); },
    getNotesEtudiant(etudiantId) { return this.notes.filter(n => n.etudiant_id === etudiantId); },
    getPaiementsEtudiant(etudiantId) { return this.paiements.filter(p => p.etudiant_id === etudiantId); },

    calculMoyenne(etudiantId, semestre) {
        const notes = this.notes.filter(n => n.etudiant_id === etudiantId && n.semestre === semestre);
        if (!notes.length) return null;
        let totalPts = 0, totalCoeff = 0;
        notes.forEach(n => {
            const mat = this.getMatiere(n.matiere_id);
            if (!mat) return;
            const moy = (n.note_cc * 0.4) + (n.note_exam * 0.6);
            totalPts += moy * mat.coeff;
            totalCoeff += mat.coeff;
        });
        return totalCoeff > 0 ? (totalPts / totalCoeff) : null;
    },

    getMention(moy) {
        if (moy === null) return '—';
        if (moy >= 16) return 'Très Bien';
        if (moy >= 14) return 'Bien';
        if (moy >= 12) return 'Assez Bien';
        if (moy >= 10) return 'Passable';
        return 'Ajourné';
    },

    totalEncaisse() {
        return this.paiements.reduce((s, p) => s + p.montant, 0);
    },

    totalDu() {
        return this.etudiants.reduce((s, e) => s + (e.solde_du || 0), 0);
    }
};
