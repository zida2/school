# 🎯 PROCHAINES ÉTAPES - INTÉGRATION FRONTEND
## Suite de l'intégration complète du système ERP

Date: 26 février 2026

---

## ✅ CE QUI EST FAIT

### Backend (100%)
- ✅ ReclamationNoteViewSet intégré et fonctionnel
- ✅ DemandeAdministrativeViewSet amélioré avec action repondre()
- ✅ SondageViewSet amélioré avec action repondre()
- ✅ EvaluationViewSet amélioré avec actions repondre() et resultats()
- ✅ ObjetPerduViewSet amélioré avec action changer_statut()
- ✅ Routes mises à jour dans urls.py
- ✅ Serveur Django démarre sans erreur
- ✅ Tous les endpoints sont accessibles

### Frontend Étudiant (80%)
- ✅ Dashboard avec statistiques
- ✅ Affichage des notes
- ✅ Emploi du temps
- ✅ Paiements
- ✅ Supports de cours
- ✅ Création de demandes
- ✅ Création de réclamations
- ✅ Affichage publications
- ✅ Affichage sondages
- ✅ Affichage objets perdus
- ❌ Bouton "Participer" sondages (à ajouter)
- ❌ Bouton "Remplir" questionnaires (à ajouter)
- ❌ Affichage réponses demandes (à ajouter)
- ❌ Affichage réponses réclamations (à ajouter)

---

## 🎯 PRIORITÉ 1 - FLUX RÉCLAMATIONS (4h)

### 1. Admin - Page Réclamations (1h)

**Fichier**: `dashboard-admin.html`

**À ajouter**:
```html
<!-- Dans la sidebar -->
<a href="#" onclick="showSection('reclamations-section')">
    <i class="fas fa-exclamation-triangle"></i>
    <span>Réclamations</span>
</a>

<!-- Section réclamations -->
<div id="reclamations-section" class="content-section" style="display:none;">
    <div class="section-header">
        <h2>Réclamations sur les notes</h2>
        <div class="filters">
            <select id="filtreStatutReclamation">
                <option value="">Tous les statuts</option>
                <option value="en_attente">En attente</option>
                <option value="resolue">Résolue</option>
                <option value="rejetee">Rejetée</option>
            </select>
        </div>
    </div>
    
    <div class="table-container">
        <table id="tableReclamations">
            <thead>
                <tr>
                    <th>Étudiant</th>
                    <th>Matière</th>
                    <th>Motif</th>
                    <th>Date</th>
                    <th>Statut</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody id="listeReclamations">
                <!-- Rempli dynamiquement -->
            </tbody>
        </table>
    </div>
</div>

<!-- Modal détails réclamation -->
<div id="modalReclamation" class="modal">
    <div class="modal-content">
        <span class="close">&times;</span>
        <h3>Détails de la réclamation</h3>
        <div id="detailsReclamation"></div>
    </div>
</div>
```

**JavaScript à ajouter**:
```javascript
async function chargerReclamations() {
    try {
        const reclamations = await API.get('/reclamations/');
        const tbody = document.getElementById('listeReclamations');
        tbody.innerHTML = '';
        
        reclamations.forEach(reclamation => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${reclamation.note.etudiant.nom} ${reclamation.note.etudiant.prenom}</td>
                <td>${reclamation.note.matiere.nom}</td>
                <td>${reclamation.description.substring(0, 50)}...</td>
                <td>${new Date(reclamation.date_creation).toLocaleDateString()}</td>
                <td><span class="badge badge-${reclamation.statut}">${reclamation.statut}</span></td>
                <td>
                    <button onclick="voirReclamation(${reclamation.id})" class="btn-icon">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error('Erreur:', err);
        showToast('Erreur lors du chargement des réclamations', 'danger');
    }
}

function voirReclamation(id) {
    // Afficher modal avec détails
    const modal = document.getElementById('modalReclamation');
    modal.style.display = 'block';
    // Charger les détails...
}
```

---

### 2. Enseignant - Page Réclamations (1h)

**Fichier**: `dashboard-prof.html`

**À ajouter**:
```html
<!-- Section réclamations -->
<div id="reclamations-section" class="content-section" style="display:none;">
    <div class="section-header">
        <h2>Réclamations sur mes matières</h2>
    </div>
    
    <div class="table-container">
        <table id="tableReclamations">
            <thead>
                <tr>
                    <th>Étudiant</th>
                    <th>Matière</th>
                    <th>Note actuelle</th>
                    <th>Motif</th>
                    <th>Date</th>
                    <th>Statut</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody id="listeReclamations">
                <!-- Rempli dynamiquement -->
            </tbody>
        </table>
    </div>
</div>

<!-- Modal traiter réclamation -->
<div id="modalTraiterReclamation" class="modal">
    <div class="modal-content">
        <span class="close">&times;</span>
        <h3>Traiter la réclamation</h3>
        <form id="formTraiterReclamation">
            <div class="form-group">
                <label>Décision</label>
                <select id="decisionReclamation" required>
                    <option value="">Choisir...</option>
                    <option value="resolue">Accepter</option>
                    <option value="rejetee">Rejeter</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Réponse</label>
                <textarea id="reponseReclamation" rows="4" required></textarea>
            </div>
            
            <div id="correctionNote" style="display:none;">
                <h4>Correction de la note</h4>
                <div class="form-row">
                    <div class="form-group">
                        <label>Nouvelle note CC</label>
                        <input type="number" id="nouvelleNoteCC" min="0" max="20" step="0.5">
                    </div>
                    <div class="form-group">
                        <label>Nouvelle note Examen</label>
                        <input type="number" id="nouvelleNoteExamen" min="0" max="20" step="0.5">
                    </div>
                </div>
            </div>
            
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Envoyer</button>
                <button type="button" class="btn btn-secondary" onclick="fermerModal('modalTraiterReclamation')">Annuler</button>
            </div>
        </form>
    </div>
</div>
```

**JavaScript à ajouter**:
```javascript
async function traiterReclamation(id) {
    const decision = document.getElementById('decisionReclamation').value;
    const reponse = document.getElementById('reponseReclamation').value;
    const corriger = decision === 'resolue';
    
    const data = {
        statut: decision,
        reponse_enseignant: reponse,
        corriger_note: corriger
    };
    
    if (corriger) {
        const noteCC = document.getElementById('nouvelleNoteCC').value;
        const noteExamen = document.getElementById('nouvelleNoteExamen').value;
        
        if (noteCC) data.nouvelle_note_cc = parseFloat(noteCC);
        if (noteExamen) data.nouvelle_note_examen = parseFloat(noteExamen);
    }
    
    try {
        await API.post(`/reclamations/${id}/traiter/`, data);
        showToast('Réclamation traitée avec succès', 'success');
        fermerModal('modalTraiterReclamation');
        chargerReclamations();
    } catch (err) {
        console.error('Erreur:', err);
        showToast('Erreur lors du traitement', 'danger');
    }
}

// Afficher/masquer la section correction
document.getElementById('decisionReclamation').addEventListener('change', (e) => {
    const correctionDiv = document.getElementById('correctionNote');
    correctionDiv.style.display = e.target.value === 'resolue' ? 'block' : 'none';
});
```

---

### 3. Étudiant - Afficher réponses réclamations (30min)

**Fichier**: `dashboard-etudiant.html`

**Modifier la section réclamations**:
```javascript
async function chargerReclamations() {
    try {
        const reclamations = await API.get('/reclamations/');
        const tbody = document.getElementById('listeReclamations');
        tbody.innerHTML = '';
        
        reclamations.forEach(reclamation => {
            const tr = document.createElement('tr');
            
            // Badge "Nouveau" si réponse non lue
            const badgeNouveau = reclamation.statut !== 'en_attente' && !reclamation.lu 
                ? '<span class="badge badge-new">Nouveau</span>' 
                : '';
            
            tr.innerHTML = `
                <td>${reclamation.note.matiere.nom}</td>
                <td>${reclamation.description.substring(0, 50)}...</td>
                <td>${new Date(reclamation.date_creation).toLocaleDateString()}</td>
                <td>
                    <span class="badge badge-${reclamation.statut}">${reclamation.statut}</span>
                    ${badgeNouveau}
                </td>
                <td>
                    ${reclamation.reponse_enseignant 
                        ? `<button onclick="voirReponseReclamation(${reclamation.id})" class="btn-sm btn-primary">
                            <i class="fas fa-eye"></i> Voir réponse
                           </button>`
                        : '<span class="text-muted">En attente</span>'
                    }
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error('Erreur:', err);
    }
}

function voirReponseReclamation(id) {
    // Afficher modal avec la réponse
    const modal = document.getElementById('modalReponseReclamation');
    modal.style.display = 'block';
    // Charger et afficher la réponse...
}
```

---

## 🎯 PRIORITÉ 2 - FLUX DEMANDES (3h)

### 1. Admin - Page Demandes (1h)

**Fichier**: `dashboard-admin.html`

**À ajouter**:
```html
<!-- Section demandes -->
<div id="demandes-section" class="content-section" style="display:none;">
    <div class="section-header">
        <h2>Demandes administratives</h2>
        <div class="filters">
            <select id="filtreStatutDemande">
                <option value="">Tous les statuts</option>
                <option value="en_attente">En attente</option>
                <option value="en_cours">En cours</option>
                <option value="traitee">Traitée</option>
                <option value="rejetee">Rejetée</option>
            </select>
        </div>
    </div>
    
    <div class="table-container">
        <table id="tableDemandes">
            <thead>
                <tr>
                    <th>Étudiant</th>
                    <th>Type</th>
                    <th>Objet</th>
                    <th>Date</th>
                    <th>Statut</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody id="listeDemandes">
                <!-- Rempli dynamiquement -->
            </tbody>
        </table>
    </div>
</div>

<!-- Modal répondre demande -->
<div id="modalRepondreDemande" class="modal">
    <div class="modal-content">
        <span class="close">&times;</span>
        <h3>Répondre à la demande</h3>
        <form id="formRepondreDemande">
            <div class="form-group">
                <label>Statut</label>
                <select id="statutDemande" required>
                    <option value="">Choisir...</option>
                    <option value="en_cours">En cours de traitement</option>
                    <option value="traitee">Traitée</option>
                    <option value="rejetee">Rejetée</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Réponse</label>
                <textarea id="reponseDemande" rows="5" required></textarea>
            </div>
            
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Envoyer</button>
                <button type="button" class="btn btn-secondary" onclick="fermerModal('modalRepondreDemande')">Annuler</button>
            </div>
        </form>
    </div>
</div>
```

**JavaScript**:
```javascript
async function chargerDemandes() {
    try {
        const demandes = await API.get('/demandes-administratives/');
        const tbody = document.getElementById('listeDemandes');
        tbody.innerHTML = '';
        
        demandes.forEach(demande => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${demande.etudiant.nom} ${demande.etudiant.prenom}</td>
                <td>${demande.type_demande}</td>
                <td>${demande.objet}</td>
                <td>${new Date(demande.date_creation).toLocaleDateString()}</td>
                <td><span class="badge badge-${demande.statut}">${demande.statut}</span></td>
                <td>
                    <button onclick="repondreDemande(${demande.id})" class="btn-icon">
                        <i class="fas fa-reply"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error('Erreur:', err);
    }
}

async function repondreDemande(id) {
    const statut = document.getElementById('statutDemande').value;
    const reponse = document.getElementById('reponseDemande').value;
    
    try {
        await API.post(`/demandes-administratives/${id}/repondre/`, {
            statut,
            reponse
        });
        showToast('Réponse envoyée', 'success');
        fermerModal('modalRepondreDemande');
        chargerDemandes();
    } catch (err) {
        console.error('Erreur:', err);
        showToast('Erreur lors de l\'envoi', 'danger');
    }
}
```

---

## 🎯 PRIORITÉ 3 - SONDAGES (3h)

### 1. Bureau - Page Sondages (2h)
- Créer des sondages
- Ajouter des questions dynamiquement
- Voir les résultats avec graphiques

### 2. Étudiant - Participer sondages (1h)
- Bouton "Participer"
- Modal avec questions
- Soumission des réponses

---

## 📊 ESTIMATION TEMPS TOTAL

- Priorité 1 (Réclamations): 4h
- Priorité 2 (Demandes): 3h
- Priorité 3 (Sondages): 3h
- Priorité 4 (Questionnaires): 3h
- Priorité 5 (Notifications): 2h

**TOTAL: ~15 heures**

---

## ✅ CHECKLIST

### Backend
- [x] ReclamationNoteViewSet
- [x] DemandeAdministrativeViewSet
- [x] SondageViewSet
- [x] EvaluationViewSet
- [x] ObjetPerduViewSet
- [x] Routes mises à jour
- [x] Serveur fonctionnel

### Frontend - Priorité 1
- [ ] Admin - Page réclamations
- [ ] Enseignant - Page réclamations
- [ ] Étudiant - Afficher réponses réclamations

### Frontend - Priorité 2
- [ ] Admin - Page demandes
- [ ] Enseignant - Page demandes
- [ ] Étudiant - Afficher réponses demandes

### Frontend - Priorité 3
- [ ] Bureau - Page sondages
- [ ] Étudiant - Participer sondages

---

Date: 26 février 2026
Statut: Backend ✅ | Frontend en cours 🔄
