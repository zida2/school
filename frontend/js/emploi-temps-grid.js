// Gestion de l'emploi du temps visuel

let currentClasse = null;
let emploisData = [];
let editingEmploi = null;

const JOURS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'];
const HEURES = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'];

// Initialisation
async function initEmploiDuTemps() {
    await chargerFilieres();
    creerGrille();
}

// Charger les filières
async function chargerFilieres() {
    try {
        const response = await fetch(`${API_URL}/filieres/`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        const filieres = await response.json();
        
        const select = document.getElementById('selectFiliereEmploi');
        select.innerHTML = '<option value="">Sélectionner une filière...</option>';
        filieres.forEach(f => {
            select.innerHTML += `<option value="${f.id}">${f.nom}</option>`;
        });
    } catch (error) {
        console.error('Erreur chargement filières:', error);
    }
}

// Charger les promotions
async function chargerPromotionsEmploi() {
    const filiereId = document.getElementById('selectFiliereEmploi').value;
    const selectPromo = document.getElementById('selectPromotionEmploi');
    const selectClasse = document.getElementById('selectClasseEmploi');
    
    selectPromo.innerHTML = '<option value="">Sélectionner une promotion...</option>';
    selectClasse.innerHTML = '<option value="">Sélectionner une classe...</option>';
    
    if (!filiereId) return;
    
    try {
        const response = await fetch(`${API_URL}/promotions/?filiere=${filiereId}`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        const promotions = await response.json();
        
        promotions.forEach(p => {
            selectPromo.innerHTML += `<option value="${p.id}">${p.nom}</option>`;
        });
    } catch (error) {
        console.error('Erreur chargement promotions:', error);
    }
}

// Charger les classes
async function chargerClassesEmploi() {
    const promotionId = document.getElementById('selectPromotionEmploi').value;
    const selectClasse = document.getElementById('selectClasseEmploi');
    
    selectClasse.innerHTML = '<option value="">Sélectionner une classe...</option>';
    
    if (!promotionId) return;
    
    try {
        const response = await fetch(`${API_URL}/classes/?promotion=${promotionId}`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        const classes = await response.json();
        
        classes.forEach(c => {
            selectClasse.innerHTML += `<option value="${c.id}">${c.nom} (${c.code})</option>`;
        });
    } catch (error) {
        console.error('Erreur chargement classes:', error);
    }
}

// Charger l'emploi du temps d'une classe
async function chargerEmploiClasse() {
    const classeId = document.getElementById('selectClasseEmploi').value;
    
    if (!classeId) {
        emploisData = [];
        afficherGrille();
        return;
    }
    
    currentClasse = classeId;
    
    try {
        const response = await fetch(`${API_URL}/emplois-du-temps/par-classe/${classeId}/`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        const data = await response.json();
        emploisData = data.emplois || [];
        afficherGrille();
    } catch (error) {
        console.error('Erreur chargement emploi du temps:', error);
        emploisData = [];
        afficherGrille();
    }
}

// Créer la grille
function creerGrille() {
    const container = document.getElementById('emploiGridContainer');
    if (!container) return;
    
    let html = '<div class="emploi-grid">';
    
    // En-tête vide pour la colonne des heures
    html += '<div class="emploi-grid-header"></div>';
    
    // En-têtes des jours
    JOURS.forEach(jour => {
        html += `<div class="emploi-grid-header">${jour}</div>`;
    });
    
    // Lignes pour chaque heure
    HEURES.forEach((heure, heureIndex) => {
        // Colonne de l'heure
        html += `<div class="emploi-grid-time">${heure}</div>`;
        
        // Cellules pour chaque jour
        JOURS.forEach((jour, jourIndex) => {
            html += `<div class="emploi-grid-cell" data-jour="${jour}" data-heure="${heure}" onclick="ouvrirModalCours('${jour}', '${heure}')"></div>`;
        });
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// Afficher les cours dans la grille
function afficherGrille() {
    // Réinitialiser toutes les cellules
    document.querySelectorAll('.emploi-grid-cell').forEach(cell => {
        cell.innerHTML = '';
        cell.classList.remove('has-cours');
    });
    
    // Placer chaque cours
    emploisData.forEach(emploi => {
        const cell = document.querySelector(`.emploi-grid-cell[data-jour="${emploi.jour}"][data-heure="${emploi.heure_debut.substring(0, 5)}"]`);
        if (cell) {
            const typeClass = emploi.type_cours ? `type-${emploi.type_cours.toLowerCase()}` : 'type-cm';
            cell.innerHTML = `
                <div class="cours-card ${typeClass}" onclick="event.stopPropagation(); ouvrirModalModifier(${emploi.id})">
                    <div class="cours-card-matiere">${emploi.matiere_nom}</div>
                    <div class="cours-card-prof">👨‍🏫 ${emploi.enseignant_nom || 'Non assigné'}</div>
                    <div class="cours-card-salle">📍 ${emploi.salle}</div>
                    <div class="cours-card-horaire">${emploi.heure_debut.substring(0, 5)} - ${emploi.heure_fin.substring(0, 5)}</div>
                </div>
            `;
            cell.classList.add('has-cours');
        }
    });
}

// Ouvrir modal pour créer un cours
async function ouvrirModalCours(jour, heure) {
    if (!currentClasse) {
        alert('Veuillez d\'abord sélectionner une classe');
        return;
    }
    
    editingEmploi = null;
    document.getElementById('modalEmploiTitle').textContent = 'Créer un cours';
    document.getElementById('btnDeleteEmploi').style.display = 'none';
    document.getElementById('btnSaveEmploi').textContent = 'Créer';
    
    // Pré-remplir jour et heure
    document.getElementById('inputJourEmploi').value = jour;
    document.getElementById('inputHeureDebutEmploi').value = heure;
    
    // Calculer heure de fin (1h après)
    const [h, m] = heure.split(':');
    const heureFin = `${String(parseInt(h) + 1).padStart(2, '0')}:${m}`;
    document.getElementById('inputHeureFinEmploi').value = heureFin;
    
    // Charger les matières
    await chargerMatieresEmploi();
    
    document.getElementById('modalEmploi').classList.add('active');
}

// Ouvrir modal pour modifier un cours
async function ouvrirModalModifier(emploiId) {
    const emploi = emploisData.find(e => e.id === emploiId);
    if (!emploi) return;
    
    editingEmploi = emploi;
    document.getElementById('modalEmploiTitle').textContent = 'Modifier le cours';
    document.getElementById('btnDeleteEmploi').style.display = 'block';
    document.getElementById('btnSaveEmploi').textContent = 'Modifier';
    
    // Charger les matières d'abord
    await chargerMatieresEmploi();
    
    // Pré-remplir le formulaire
    document.getElementById('inputJourEmploi').value = emploi.jour;
    document.getElementById('selectMatiereEmploi').value = emploi.matiere;
    document.getElementById('inputSalleEmploi').value = emploi.salle;
    document.getElementById('selectTypeCoursEmploi').value = emploi.type_cours || 'CM';
    document.getElementById('inputHeureDebutEmploi').value = emploi.heure_debut.substring(0, 5);
    document.getElementById('inputHeureFinEmploi').value = emploi.heure_fin.substring(0, 5);
    
    document.getElementById('modalEmploi').classList.add('active');
}

// Charger les matières
async function chargerMatieresEmploi() {
    try {
        const response = await fetch(`${API_URL}/matieres/`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        const matieres = await response.json();
        
        const select = document.getElementById('selectMatiereEmploi');
        select.innerHTML = '<option value="">Sélectionner une matière...</option>';
        matieres.forEach(m => {
            const profNom = m.enseignant_nom || 'Pas de prof';
            select.innerHTML += `<option value="${m.id}">${m.nom} - ${profNom}</option>`;
        });
    } catch (error) {
        console.error('Erreur chargement matières:', error);
    }
}

// Fermer modal
function fermerModalEmploi() {
    document.getElementById('modalEmploi').classList.remove('active');
    document.getElementById('formEmploi').reset();
    editingEmploi = null;
}

// Sauvegarder cours
async function sauvegarderCours() {
    const jour = document.getElementById('inputJourEmploi').value;
    const matiere = document.getElementById('selectMatiereEmploi').value;
    const salle = document.getElementById('inputSalleEmploi').value;
    const typeCours = document.getElementById('selectTypeCoursEmploi').value;
    const heureDebut = document.getElementById('inputHeureDebutEmploi').value;
    const heureFin = document.getElementById('inputHeureFinEmploi').value;
    
    if (!jour || !matiere || !salle || !heureDebut || !heureFin) {
        alert('Veuillez remplir tous les champs obligatoires');
        return;
    }
    
    const data = {
        jour,
        matiere,
        classe: currentClasse,
        salle,
        type_cours: typeCours,
        heure_debut: heureDebut,
        heure_fin: heureFin
    };
    
    // Vérifier les conflits
    const conflitsResponse = await fetch(`${API_URL}/emplois-du-temps/verifier-conflits/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            ...data,
            emploi_id: editingEmploi ? editingEmploi.id : null
        })
    });
    
    const conflitsData = await conflitsResponse.json();
    
    if (conflitsData.has_conflicts) {
        let message = 'Conflits détectés:\n\n';
        conflitsData.conflicts.forEach(c => {
            message += `${c.message}\n`;
        });
        alert(message);
        return;
    }
    
    try {
        const url = editingEmploi 
            ? `${API_URL}/emplois-du-temps/${editingEmploi.id}/`
            : `${API_URL}/emplois-du-temps/`;
        
        const method = editingEmploi ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            fermerModalEmploi();
            await chargerEmploiClasse();
            alert(editingEmploi ? 'Cours modifié avec succès' : 'Cours créé avec succès');
        } else {
            const error = await response.json();
            alert('Erreur: ' + JSON.stringify(error));
        }
    } catch (error) {
        console.error('Erreur sauvegarde cours:', error);
        alert('Erreur lors de la sauvegarde');
    }
}

// Supprimer cours
async function supprimerCours() {
    if (!editingEmploi) return;
    
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce cours ?')) return;
    
    try {
        const response = await fetch(`${API_URL}/emplois-du-temps/${editingEmploi.id}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        
        if (response.ok) {
            fermerModalEmploi();
            await chargerEmploiClasse();
            alert('Cours supprimé avec succès');
        } else {
            alert('Erreur lors de la suppression');
        }
    } catch (error) {
        console.error('Erreur suppression cours:', error);
        alert('Erreur lors de la suppression');
    }
}
