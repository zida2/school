/**
 * Gestion Admin - Emploi du Temps, Inscriptions, Classes
 * Fonctionnalités backend complètes pour le dashboard admin
 */

// ===== EMPLOI DU TEMPS =====
let emploiDuTempsData = [];
let matieresData = [];
let enseignantsData = [];
let classesData = [];

async function chargerMatieresEtEnseignants() {
    try {
        // Charger les matières
        matieresData = await API.get('/matieres/');
        const selectMatiere = document.getElementById('emploiMatiere');
        const filterMatiere = document.getElementById('filterMatiereEmploi');
        
        if (selectMatiere) {
            selectMatiere.innerHTML = '<option value="">Sélectionner une matière</option>' +
                matieresData.map(m => `<option value="${m.id}">${m.nom}</option>`).join('');
        }
        if (filterMatiere) {
            filterMatiere.innerHTML = '<option value="">📚 Toutes les matières</option>' +
                matieresData.map(m => `<option value="${m.id}">${m.nom}</option>`).join('');
        }
        
        // Charger les enseignants
        enseignantsData = await API.get('/enseignants/');
        const filterEnseignant = document.getElementById('filterEnseignantEmploi');
        
        if (filterEnseignant) {
            filterEnseignant.innerHTML = '<option value="">👨‍🏫 Tous les enseignants</option>' +
                enseignantsData.map(e => `<option value="${e.id}">${e.prenom} ${e.nom}</option>`).join('');
        }
        
        // Charger les classes
        classesData = await API.get('/classes/');
        const selectClasse = document.getElementById('emploiClasse');
        
        if (selectClasse) {
            selectClasse.innerHTML = '<option value="">Sélectionner une classe (optionnel)</option>' +
                classesData.map(c => `<option value="${c.id}">${c.nom} (${c.filiere_nom || 'N/A'})</option>`).join('');
        }
            
    } catch (error) {
        console.error('Erreur chargement données:', error);
    }
}

async function chargerEmploiDuTemps() {
    try {
        const jour = document.getElementById('filterJourEmploi')?.value || '';
        const matiere = document.getElementById('filterMatiereEmploi')?.value || '';
        const enseignant = document.getElementById('filterEnseignantEmploi')?.value || '';

        let url = '/emplois-du-temps/'; // CORRECTION: emplois-du-temps au lieu de emploi-du-temps
        const params = [];
        if (jour) params.push(`jour=${jour}`);
        if (matiere) params.push(`matiere=${matiere}`);
        if (enseignant) params.push(`enseignant=${enseignant}`);
        if (params.length) url += '?' + params.join('&');

        emploiDuTempsData = await API.get(url);
        afficherEmploiDuTemps();
    } catch (error) {
        console.error('Erreur chargement emploi du temps:', error);
        const tbody = document.getElementById('tbodyEmploiAdmin');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:#ef4444">Erreur de chargement</td></tr>';
        }
    }
}

function afficherEmploiDuTemps() {
    const tbody = document.getElementById('tbodyEmploiAdmin');
    if (!tbody) return;
    
    if (!emploiDuTempsData || emploiDuTempsData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px">Aucun cours programmé</td></tr>';
        return;
    }

    tbody.innerHTML = emploiDuTempsData.map(emploi => `
        <tr>
            <td>${emploi.jour}</td>
            <td>${emploi.heure_debut} - ${emploi.heure_fin}</td>
            <td><strong>${emploi.matiere_nom || 'N/A'}</strong></td>
            <td>${emploi.enseignant_nom || 'N/A'}</td>
            <td>${emploi.salle || 'N/A'}</td>
            <td>${emploi.classe_nom || 'Toutes'}</td>
            <td>
                <button class="btn-icon-ultra" onclick="modifierEmploi(${emploi.id})" title="Modifier">
                    <span>✏️</span>
                </button>
                <button class="btn-icon-ultra" onclick="supprimerEmploi(${emploi.id})" title="Supprimer">
                    <span style="color:#ef4444">🗑️</span>
                </button>
            </td>
        </tr>
    `).join('');
}

function openModalEmploiDuTemps() {
    const modal = document.getElementById('modalEmploiDuTemps');
    const title = document.getElementById('modalEmploiDuTempsTitle');
    const form = document.getElementById('formEmploiDuTemps');
    const idField = document.getElementById('emploiId');
    
    if (title) title.textContent = '📅 Créer un cours';
    if (form) form.reset();
    if (idField) idField.value = '';
    if (modal) modal.style.display = 'flex';
}

async function saveEmploiDuTemps(event) {
    event.preventDefault();

    const id = document.getElementById('emploiId')?.value;
    const data = {
        matiere: parseInt(document.getElementById('emploiMatiere').value),
        jour: document.getElementById('emploiJour').value,
        heure_debut: document.getElementById('emploiHeureDebut').value,
        heure_fin: document.getElementById('emploiHeureFin').value,
        salle: document.getElementById('emploiSalle').value,
        semaine: document.getElementById('emploiSemaine')?.value || 'toutes'
    };
    
    // Ajouter la classe si sélectionnée
    const classeId = document.getElementById('emploiClasse')?.value;
    if (classeId) {
        data.classe = parseInt(classeId);
    }

    try {
        if (id) {
            await API.put(`/emplois-du-temps/${id}/`, data);
            showNotification('Cours modifié avec succès', 'success');
        } else {
            await API.post('/emplois-du-temps/', data);
            showNotification('Cours créé avec succès', 'success');
        }

        closeModal('modalEmploiDuTemps');
        await chargerEmploiDuTemps();
    } catch (error) {
        showNotification('Erreur: ' + (error.message || 'Erreur inconnue'), 'error');
    }
}

async function modifierEmploi(id) {
    const emploi = emploiDuTempsData.find(e => e.id === id);
    if (!emploi) return;

    document.getElementById('modalEmploiDuTempsTitle').textContent = '✏️ Modifier le cours';
    document.getElementById('emploiId').value = emploi.id;
    document.getElementById('emploiMatiere').value = emploi.matiere;
    document.getElementById('emploiJour').value = emploi.jour;
    document.getElementById('emploiHeureDebut').value = emploi.heure_debut;
    document.getElementById('emploiHeureFin').value = emploi.heure_fin;
    document.getElementById('emploiSalle').value = emploi.salle;
    if (document.getElementById('emploiSemaine')) {
        document.getElementById('emploiSemaine').value = emploi.semaine || 'toutes';
    }
    if (document.getElementById('emploiClasse') && emploi.classe) {
        document.getElementById('emploiClasse').value = emploi.classe;
    }

    document.getElementById('modalEmploiDuTemps').style.display = 'flex';
}

async function supprimerEmploi(id) {
    if (!confirm('Supprimer ce cours ?')) return;

    try {
        await API.delete(`/emplois-du-temps/${id}/`);
        showNotification('Cours supprimé avec succès', 'success');
        await chargerEmploiDuTemps();
    } catch (error) {
        showNotification('Erreur lors de la suppression', 'error');
    }
}

// ===== INSCRIPTIONS ÉTUDIANTS =====
let inscriptionsEtudiantsData = [];

async function chargerInscriptionsEtudiants() {
    try {
        const statut = document.getElementById('filterStatutInscription')?.value || '';
        const filiere = document.getElementById('filterFiliereInscription')?.value || '';
        
        let url = '/demandes-inscription/';
        const params = [];
        if (statut) params.push(`statut=${statut}`);
        if (filiere) params.push(`filiere=${filiere}`);
        if (params.length) url += '?' + params.join('&');
        
        inscriptionsEtudiantsData = await API.get(url);
        afficherInscriptionsEtudiants();
    } catch (error) {
        console.error('Erreur chargement inscriptions:', error);
        const tbody = document.getElementById('tbodyInscriptionsEtudiants');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:40px;color:#ef4444">Erreur de chargement</td></tr>';
        }
    }
}

function afficherInscriptionsEtudiants() {
    const tbody = document.getElementById('tbodyInscriptionsEtudiants');
    if (!tbody) return;
    
    if (!inscriptionsEtudiantsData || inscriptionsEtudiantsData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:40px">Aucune demande d\'inscription</td></tr>';
        return;
    }
    
    const statutColors = {
        'en_attente': '#f59e0b',
        'validee': '#10b981',
        'rejetee': '#ef4444'
    };
    const statutLabels = {
        'en_attente': 'En attente',
        'validee': 'Validée',
        'rejetee': 'Rejetée'
    };
    
    tbody.innerHTML = inscriptionsEtudiantsData.map(demande => `
        <tr>
            <td><strong>${demande.prenom} ${demande.nom}</strong></td>
            <td>${demande.email}</td>
            <td>${demande.telephone || 'N/A'}</td>
            <td>${demande.filiere_demandee_nom || 'N/A'}</td>
            <td>${demande.niveau_demande || 'N/A'}</td>
            <td>${new Date(demande.date_demande).toLocaleDateString('fr-FR')}</td>
            <td>
                <span style="padding:6px 12px;border-radius:6px;font-size:12px;font-weight:600;background:${statutColors[demande.statut]}22;color:${statutColors[demande.statut]}">
                    ${statutLabels[demande.statut]}
                </span>
            </td>
            <td>
                ${demande.statut === 'en_attente' ? `
                    <button class="btn-icon-ultra" onclick="approuverInscriptionEtudiant(${demande.id})" title="Approuver">
                        <span style="color:#10b981">✓</span>
                    </button>
                    <button class="btn-icon-ultra" onclick="rejeterInscriptionEtudiant(${demande.id})" title="Rejeter">
                        <span style="color:#ef4444">✕</span>
                    </button>
                ` : `
                    <button class="btn-icon-ultra" onclick="voirDetailsInscription(${demande.id})" title="Détails">
                        <span>👁️</span>
                    </button>
                `}
            </td>
        </tr>
    `).join('');
}

async function approuverInscriptionEtudiant(id) {
    if (!confirm('Approuver cette demande d\'inscription ?\n\nUn email sera envoyé automatiquement avec les identifiants.')) return;
    
    try {
        const result = await API.post(`/demandes-inscription/${id}/approuver/`);
        showNotification(`Inscription approuvée ! Matricule: ${result.matricule}`, 'success');
        await chargerInscriptionsEtudiants();
    } catch (error) {
        showNotification('Erreur lors de l\'approbation: ' + (error.message || 'Erreur inconnue'), 'error');
    }
}

async function rejeterInscriptionEtudiant(id) {
    const motif = prompt('Motif du rejet (optionnel):');
    if (motif === null) return; // Annulé
    
    try {
        await API.post(`/demandes-inscription/${id}/rejeter/`, { motif });
        showNotification('Demande rejetée', 'success');
        await chargerInscriptionsEtudiants();
    } catch (error) {
        showNotification('Erreur lors du rejet', 'error');
    }
}

function voirDetailsInscription(id) {
    const demande = inscriptionsEtudiantsData.find(d => d.id === id);
    if (!demande) return;
    
    alert(`Détails de l'inscription:\n\nNom: ${demande.prenom} ${demande.nom}\nEmail: ${demande.email}\nTéléphone: ${demande.telephone || 'N/A'}\nFilière: ${demande.filiere_demandee_nom}\nNiveau: ${demande.niveau_demande}\nStatut: ${demande.statut}\nDate: ${new Date(demande.date_demande).toLocaleDateString('fr-FR')}`);
}

// ===== CLASSES =====
let classesGestionData = [];

async function chargerClassesGestion() {
    try {
        classesGestionData = await API.get('/classes/');
        afficherClassesGestion();
    } catch (error) {
        console.error('Erreur chargement classes:', error);
        const tbody = document.getElementById('tbodyClasses');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:40px;color:#ef4444">Erreur de chargement</td></tr>';
        }
    }
}

function afficherClassesGestion() {
    const tbody = document.getElementById('tbodyClasses');
    if (!tbody) return;
    
    if (!classesGestionData || classesGestionData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:40px">Aucune classe créée</td></tr>';
        return;
    }
    
    tbody.innerHTML = classesGestionData.map(classe => `
        <tr>
            <td><strong>${classe.code}</strong></td>
            <td>${classe.nom}</td>
            <td>${classe.filiere_nom || 'N/A'}</td>
            <td>${classe.niveau || 'N/A'}</td>
            <td>${classe.effectif || 0}</td>
            <td>
                <button class="btn-icon-ultra" onclick="modifierClasse(${classe.id})" title="Modifier">
                    <span>✏️</span>
                </button>
                <button class="btn-icon-ultra" onclick="supprimerClasse(${classe.id})" title="Supprimer">
                    <span style="color:#ef4444">🗑️</span>
                </button>
            </td>
        </tr>
    `).join('');
}

// Fonction utilitaire pour afficher les notifications
function showNotification(message, type = 'info') {
    // Utiliser showToast si disponible, sinon alert
    if (typeof showToast === 'function') {
        showToast(message, type);
    } else {
        alert(message);
    }
}

// Fonction utilitaire pour fermer les modals
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

console.log('✅ admin-gestion.js chargé');
