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
        const response = await fetch(`${CONFIG.API_URL}/filieres/`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        const data = await response.json();
        
        const select = document.getElementById('emploiFilterFiliere');
        if (!select) {
            console.log('⚠️ Element emploiFilterFiliere non trouvé');
            return;
        }
        
        // L'API peut retourner un tableau ou un objet avec results
        const filieres = Array.isArray(data) ? data : (data.results || []);
        
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
    const selectFiliere = document.getElementById('emploiFilterFiliere');
    const selectPromo = document.getElementById('emploiFilterPromotion');
    const selectClasse = document.getElementById('emploiFilterClasse');
    
    if (!selectFiliere || !selectPromo || !selectClasse) return;
    
    const filiereId = selectFiliere.value;
    
    selectPromo.innerHTML = '<option value="">Sélectionner une promotion...</option>';
    selectClasse.innerHTML = '<option value="">Sélectionner une classe...</option>';
    
    if (!filiereId) return;
    
    try {
        const response = await fetch(`${CONFIG.API_URL}/promotions/?filiere=${filiereId}`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        
        if (!response.ok) {
            console.error(`Erreur API: ${response.status}`);
            selectPromo.innerHTML += '<option value="">Erreur de chargement</option>';
            return;
        }
        
        const data = await response.json();
        const promotions = Array.isArray(data) ? data : (data.results || []);
        
        if (promotions.length === 0) {
            selectPromo.innerHTML += '<option value="">Aucune promotion disponible</option>';
            return;
        }
        
        promotions.forEach(p => {
            selectPromo.innerHTML += `<option value="${p.id}">${p.nom}</option>`;
        });
    } catch (error) {
        console.error('Erreur chargement promotions:', error);
        selectPromo.innerHTML += '<option value="">Erreur de chargement</option>';
    }
}

// Charger les classes
async function chargerClassesEmploi() {
    const selectPromo = document.getElementById('emploiFilterPromotion');
    const selectClasse = document.getElementById('emploiFilterClasse');
    
    if (!selectPromo || !selectClasse) return;
    
    const promotionId = selectPromo.value;
    
    selectClasse.innerHTML = '<option value="">Sélectionner une classe...</option>';
    
    if (!promotionId) return;
    
    try {
        const response = await fetch(`${CONFIG.API_URL}/classes/?promotion=${promotionId}`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        
        if (!response.ok) {
            console.error(`Erreur API: ${response.status}`);
            selectClasse.innerHTML += '<option value="">Erreur de chargement</option>';
            return;
        }
        
        const data = await response.json();
        const classes = Array.isArray(data) ? data : (data.results || []);
        
        if (classes.length === 0) {
            selectClasse.innerHTML += '<option value="">Aucune classe disponible</option>';
            return;
        }
        
        classes.forEach(c => {
            selectClasse.innerHTML += `<option value="${c.id}">${c.nom} (${c.code})</option>`;
        });
    } catch (error) {
        console.error('Erreur chargement classes:', error);
        selectClasse.innerHTML += '<option value="">Erreur de chargement</option>';
    }
}

// Charger l'emploi du temps d'une classe
async function chargerEmploiClasse() {
    const selectClasse = document.getElementById('emploiFilterClasse');
    if (!selectClasse) return;
    
    const classeId = selectClasse.value;
    
    if (!classeId) {
        emploisData = [];
        afficherGrille();
        return;
    }
    
    currentClasse = classeId;
    
    try {
        const response = await fetch(`${CONFIG.API_URL}/emplois-du-temps/par-classe/${classeId}/`, {
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
        const response = await fetch(`${CONFIG.API_URL}/matieres/`, {
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
    const conflitsResponse = await fetch(`${CONFIG.API_URL}/emplois-du-temps/verifier-conflits/`, {
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
            ? `${CONFIG.API_URL}/emplois-du-temps/${editingEmploi.id}/`
            : `${CONFIG.API_URL}/emplois-du-temps/`;
        
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
        const response = await fetch(`${CONFIG.API_URL}/emplois-du-temps/${editingEmploi.id}/`, {
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


// Sauvegarder l'emploi du temps
async function sauvegarderEmploiDuTemps() {
    const selectClasse = document.getElementById('emploiFilterClasse');
    
    if (!selectClasse || !selectClasse.value) {
        showToast('Veuillez sélectionner une classe', 'warning');
        return;
    }
    
    const classeId = selectClasse.value;
    
    try {
        // Récupérer tous les emplois de la classe
        const response = await fetch(`${CONFIG.API_URL}/emplois-du-temps/?classe=${classeId}`, {
            headers: { 
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('Erreur lors de la récupération des emplois');
        }
        
        const emplois = await response.json();
        const emploisArray = Array.isArray(emplois) ? emplois : (emplois.results || []);
        
        // Vérifier les conflits
        const conflits = [];
        for (let i = 0; i < emploisArray.length; i++) {
            for (let j = i + 1; j < emploisArray.length; j++) {
                const e1 = emploisArray[i];
                const e2 = emploisArray[j];
                
                // Vérifier si même jour et horaires qui se chevauchent
                if (e1.jour === e2.jour) {
                    const debut1 = e1.heure_debut;
                    const fin1 = e1.heure_fin;
                    const debut2 = e2.heure_debut;
                    const fin2 = e2.heure_fin;
                    
                    if ((debut1 < fin2 && fin1 > debut2)) {
                        conflits.push({
                            jour: e1.jour,
                            cours1: e1.matiere_nom,
                            cours2: e2.matiere_nom,
                            horaire: `${debut1}-${fin1} / ${debut2}-${fin2}`
                        });
                    }
                }
            }
        }
        
        if (conflits.length > 0) {
            const message = `⚠️ ${conflits.length} conflit(s) détecté(s):\n\n` + 
                conflits.map(c => `${c.jour}: ${c.cours1} ⚔️ ${c.cours2} (${c.horaire})`).join('\n');
            
            if (!confirm(message + '\n\nVoulez-vous quand même sauvegarder ?')) {
                return;
            }
        }
        
        // Tout est OK, afficher un message de succès
        showToast(`✅ Emploi du temps sauvegardé avec succès (${emploisArray.length} cours)`, 'success');
        
        // Optionnel: Envoyer une notification aux enseignants
        if (confirm('Voulez-vous envoyer l\'emploi du temps par email aux enseignants ?')) {
            await envoyerEmploiDuTemps();
        }
        
    } catch (error) {
        console.error('Erreur sauvegarde emploi du temps:', error);
        showToast('Erreur lors de la sauvegarde de l\'emploi du temps', 'error');
    }
}

// Fonction showToast si elle n'existe pas déjà
if (typeof showToast === 'undefined') {
    function showToast(message, type = 'info') {
        const icons = { success: '✅', danger: '❌', warning: '⚠️', info: 'ℹ️' };
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:10px;';
            document.body.appendChild(container);
        }
        const toast = document.createElement('div');
        const colors = { success: '#059669', danger: '#dc2626', warning: '#d97706', info: '#2563eb' };
        toast.style.cssText = `background:rgba(10,14,39,0.95);border-radius:12px;padding:14px 18px;box-shadow:0 8px 32px rgba(0,0,0,.3);display:flex;align-items:center;gap:12px;min-width:280px;max-width:400px;border-left:4px solid ${colors[type]};animation:slideIn .3s ease;backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.1)`;
        toast.innerHTML = `<span style="font-size:20px">${icons[type]}</span><span style="color:#fff;font-size:14px;font-weight:500">${message}</span>`;
        container.appendChild(toast);
        setTimeout(() => { toast.style.animation = 'slideOut .3s ease'; setTimeout(() => toast.remove(), 300); }, 4000);
    }
}
