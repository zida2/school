# 🔧 Corrections Dashboard Admin - Fonctionnalités Backend

## 📋 Problèmes Identifiés

### 1. Emploi du Temps
- ❌ URL incorrecte: `/emploi-du-temps/` au lieu de `/emplois-du-temps/`
- ❌ Pas de chargement des matières et enseignants pour les filtres
- ❌ Pas de gestion des classes dans l'emploi du temps

### 2. Gestion des Inscriptions Étudiants
- ❌ Pas d'interface pour voir les demandes d'inscription
- ❌ Pas de bouton pour approuver/rejeter les demandes
- ❌ Pas de liste des étudiants par filière et promotion

### 3. Gestion des Classes
- ❌ Pas d'interface pour créer/gérer les classes
- ❌ Pas d'assignation de professeurs aux classes

## ✅ Solutions à Implémenter

### 1. Corriger l'Emploi du Temps

#### A. Corriger les URLs dans dashboard-admin.html
```javascript
// AVANT (ligne ~2955)
let url = '/emploi-du-temps/';

// APRÈS
let url = '/emplois-du-temps/';
```

```javascript
// AVANT (ligne ~3050)
await API.put(`/emploi-du-temps/${id}/`, data);
await API.post('/emploi-du-temps/', data);

// APRÈS
await API.put(`/emplois-du-temps/${id}/`, data);
await API.post('/emplois-du-temps/', data);
```

```javascript
// AVANT (ligne ~3084)
await API.delete(`/emploi-du-temps/${id}/`);

// APRÈS
await API.delete(`/emplois-du-temps/${id}/`, data);
```

#### B. Ajouter le chargement des classes
```javascript
async function chargerMatieresEtEnseignants() {
    try {
        // Charger les matières
        matieresData = await API.get('/matieres/');
        const selectMatiere = document.getElementById('emploiMatiere');
        const filterMatiere = document.getElementById('filterMatiereEmploi');
        
        selectMatiere.innerHTML = '<option value="">Sélectionner une matière</option>' +
            matieresData.map(m => `<option value="${m.id}">${m.nom}</option>`).join('');
        filterMatiere.innerHTML = '<option value="">📚 Toutes les matières</option>' +
            matieresData.map(m => `<option value="${m.id}">${m.nom}</option>`).join('');
        
        // Charger les enseignants
        enseignantsData = await API.get('/enseignants/');
        const filterEnseignant = document.getElementById('filterEnseignantEmploi');
        
        filterEnseignant.innerHTML = '<option value="">👨‍🏫 Tous les enseignants</option>' +
            enseignantsData.map(e => `<option value="${e.id}">${e.prenom} ${e.nom}</option>`).join('');
        
        // Charger les classes
        const classesData = await API.get('/classes/');
        const selectClasse = document.getElementById('emploiClasse');
        
        selectClasse.innerHTML = '<option value="">Sélectionner une classe</option>' +
            classesData.map(c => `<option value="${c.id}">${c.nom} (${c.filiere_nom})</option>`).join('');
            
    } catch (error) {
        console.error('Erreur chargement données:', error);
    }
}
```

#### C. Ajouter le champ classe dans le formulaire
```html
<!-- Ajouter après le champ matière -->
<div class="form-group-ultra">
    <label class="form-label-ultra">Classe</label>
    <select id="emploiClasse" class="form-input-ultra" required>
        <option value="">Sélectionner une classe</option>
    </select>
</div>
```

### 2. Ajouter la Gestion des Inscriptions Étudiants

#### A. Ajouter une nouvelle page dans le dashboard
```html
<!-- PAGE: INSCRIPTIONS ÉTUDIANTS -->
<div class="page-ultra" id="page-inscriptions-etudiants" style="display:none">
    <div class="page-header-ultra">
        <div>
            <h1 class="page-title-ultra">📝 Inscriptions Étudiants</h1>
            <p class="page-subtitle-ultra">Gérer les demandes d'inscription</p>
        </div>
    </div>

    <div class="card-ultra">
        <!-- Filtres -->
        <div class="filters-bar-ultra" style="margin-bottom:24px">
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px">
                <select id="filterStatutInscription" class="form-input-ultra" onchange="chargerInscriptionsEtudiants()">
                    <option value="">📋 Tous les statuts</option>
                    <option value="en_attente">En attente</option>
                    <option value="validee">Validée</option>
                    <option value="rejetee">Rejetée</option>
                </select>
                <select id="filterFiliereInscription" class="form-input-ultra" onchange="chargerInscriptionsEtudiants()">
                    <option value="">🎓 Toutes les filières</option>
                </select>
            </div>
        </div>

        <!-- Tableau -->
        <div class="table-responsive-ultra">
            <table class="table-ultra">
                <thead>
                    <tr>
                        <th>Nom & Prénom</th>
                        <th>Email</th>
                        <th>Téléphone</th>
                        <th>Filière</th>
                        <th>Niveau</th>
                        <th>Date</th>
                        <th>Statut</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="tbodyInscriptionsEtudiants">
                    <tr><td colspan="8" style="text-align:center;padding:40px">Chargement...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
```

#### B. Ajouter les fonctions JavaScript
```javascript
let inscriptionsEtudiantsData = [];

async function chargerInscriptionsEtudiants() {
    try {
        const statut = document.getElementById('filterStatutInscription').value;
        const filiere = document.getElementById('filterFiliereInscription').value;
        
        let url = '/demandes-inscription/';
        const params = [];
        if (statut) params.push(`statut=${statut}`);
        if (filiere) params.push(`filiere=${filiere}`);
        if (params.length) url += '?' + params.join('&');
        
        inscriptionsEtudiantsData = await API.get(url);
        afficherInscriptionsEtudiants();
    } catch (error) {
        console.error('Erreur chargement inscriptions:', error);
        document.getElementById('tbodyInscriptionsEtudiants').innerHTML = 
            '<tr><td colspan="8" style="text-align:center;padding:40px;color:#ef4444">Erreur de chargement</td></tr>';
    }
}

function afficherInscriptionsEtudiants() {
    const tbody = document.getElementById('tbodyInscriptionsEtudiants');
    
    if (!inscriptionsEtudiantsData || inscriptionsEtudiantsData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:40px">Aucune demande d\'inscription</td></tr>';
        return;
    }
    
    tbody.innerHTML = inscriptionsEtudiantsData.map(demande => {
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
        
        return `
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
        `;
    }).join('');
}

async function approuverInscriptionEtudiant(id) {
    if (!confirm('Approuver cette demande d\'inscription ?')) return;
    
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
```

### 3. Ajouter la Liste des Étudiants par Filière/Promotion

#### A. Modifier la page étudiants existante
```javascript
async function chargerEtudiants() {
    try {
        const filiere = document.getElementById('filterFiliereEtudiant').value;
        const promotion = document.getElementById('filterPromotionEtudiant').value;
        
        let url = '/etudiants/';
        const params = [];
        if (filiere) params.push(`filiere=${filiere}`);
        if (promotion) params.push(`promotion=${promotion}`);
        if (params.length) url += '?' + params.join('&');
        
        etudiantsData = await API.get(url);
        afficherEtudiants();
    } catch (error) {
        console.error('Erreur chargement étudiants:', error);
    }
}
```

### 4. Ajouter la Gestion des Classes

#### A. Ajouter une nouvelle page
```html
<!-- PAGE: CLASSES -->
<div class="page-ultra" id="page-classes" style="display:none">
    <div class="page-header-ultra">
        <div>
            <h1 class="page-title-ultra">🏫 Gestion des Classes</h1>
            <p class="page-subtitle-ultra">Créer et gérer les classes</p>
        </div>
        <button class="btn-ultra btn-primary-ultra" onclick="openModalClasse()">+ Créer une classe</button>
    </div>

    <div class="card-ultra">
        <div class="table-responsive-ultra">
            <table class="table-ultra">
                <thead>
                    <tr>
                        <th>Code</th>
                        <th>Nom</th>
                        <th>Filière</th>
                        <th>Niveau</th>
                        <th>Effectif</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="tbodyClasses">
                    <tr><td colspan="6" style="text-align:center;padding:40px">Chargement...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
```

## 📝 Fichiers à Modifier

1. **frontend/dashboard-admin.html**
   - Corriger les URLs `/emploi-du-temps/` → `/emplois-du-temps/`
   - Ajouter la page inscriptions étudiants
   - Ajouter la page classes
   - Ajouter les fonctions JavaScript

2. **backend/api/serializers.py**
   - Vérifier que les serializers incluent tous les champs nécessaires

3. **backend/api/views.py**
   - Vérifier que les filtres fonctionnent correctement

## 🚀 Ordre d'Implémentation

1. ✅ Corriger les URLs de l'emploi du temps
2. ✅ Ajouter le chargement des classes dans l'emploi du temps
3. ✅ Créer la page de gestion des inscriptions étudiants
4. ✅ Créer la page de gestion des classes
5. ✅ Tester toutes les fonctionnalités

---

**Date**: 7 mars 2026
**Priorité**: HAUTE
