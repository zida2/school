# Ajout de la Gestion d'Emploi du Temps dans l'Espace Admin

## Problème
L'administrateur ne peut pas créer/gérer l'emploi du temps. Cette fonctionnalité manque dans `dashboard-admin.html`.

## Solution Rapide (Mode MOCK)

### 1. Ajouter le lien dans le menu (ligne ~50)
Après la ligne avec "Filières", ajouter :
```html
<a class="nav-item-ultra" data-page="emploi" onclick="navToUltra('emploi',this)">
    <span class="nav-icon-ultra">📅</span>
    <span class="nav-text-ultra">Emploi du temps</span>
</a>
```

### 2. Ajouter la page emploi du temps (après la page filieres, ligne ~900)
```html
<!-- PAGE: EMPLOI DU TEMPS -->
<div class="page-ultra" id="page-emploi" style="display:none">
    <div class="page-header-ultra">
        <div>
            <h1 class="page-title-ultra">📅 Emploi du temps</h1>
            <p class="page-subtitle-ultra">Gestion des cours et horaires</p>
        </div>
        <div class="page-actions-ultra">
            <button class="btn-ultra btn-primary-ultra" onclick="openModal('modalEmploi')">+ Ajouter un cours</button>
        </div>
    </div>

    <div class="card-ultra">
        <div class="card-body-ultra" style="padding:0">
            <table class="table-ultra">
                <thead>
                    <tr>
                        <th>Jour</th>
                        <th>Heure</th>
                        <th>Matière</th>
                        <th>Enseignant</th>
                        <th>Filière</th>
                        <th>Salle</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="tbodyEmploi">
                    <tr><td colspan="7" style="text-align:center;padding:40px">Chargement...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
```

### 3. Ajouter le modal d'ajout (avant la fermeture du body, ligne ~1030)
```html
<!-- MODAL: AJOUTER EMPLOI -->
<div class="modal-ultra" id="modalEmploi">
    <div class="modal-content-ultra">
        <div class="modal-header-ultra">
            <h3>Ajouter un cours</h3>
            <button class="modal-close-ultra" onclick="closeModal('modalEmploi')">✕</button>
        </div>
        <form onsubmit="ajouterEmploi(event)">
            <div class="modal-body-ultra">
                <div class="form-group-ultra">
                    <label class="form-label-ultra">Jour *</label>
                    <select name="jour" class="form-input-ultra" required>
                        <option value="">Sélectionner</option>
                        <option value="Lundi">Lundi</option>
                        <option value="Mardi">Mardi</option>
                        <option value="Mercredi">Mercredi</option>
                        <option value="Jeudi">Jeudi</option>
                        <option value="Vendredi">Vendredi</option>
                        <option value="Samedi">Samedi</option>
                    </select>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
                    <div class="form-group-ultra">
                        <label class="form-label-ultra">Heure début *</label>
                        <input type="time" name="heure_debut" class="form-input-ultra" required>
                    </div>
                    <div class="form-group-ultra">
                        <label class="form-label-ultra">Heure fin *</label>
                        <input type="time" name="heure_fin" class="form-input-ultra" required>
                    </div>
                </div>
                <div class="form-group-ultra">
                    <label class="form-label-ultra">Matière *</label>
                    <select name="matiere" id="selectMatiereEmploi" class="form-input-ultra" required>
                        <option value="">Sélectionner</option>
                    </select>
                </div>
                <div class="form-group-ultra">
                    <label class="form-label-ultra">Enseignant *</label>
                    <select name="enseignant" id="selectEnseignantEmploi" class="form-input-ultra" required>
                        <option value="">Sélectionner</option>
                    </select>
                </div>
                <div class="form-group-ultra">
                    <label class="form-label-ultra">Salle *</label>
                    <input type="text" name="salle" class="form-input-ultra" placeholder="Ex: A101" required>
                </div>
            </div>
            <div class="modal-footer-ultra">
                <button type="button" class="btn-ultra btn-secondary-ultra" onclick="closeModal('modalEmploi')">Annuler</button>
                <button type="submit" class="btn-ultra btn-primary-ultra">Enregistrer</button>
            </div>
        </form>
    </div>
</div>
```

### 4. Ajouter les fonctions JavaScript (dans la section script, ligne ~2000)
```javascript
async function chargerEmploi() {
    try {
        const emplois = await API.getEmploisDuTemps();
        const tbody = document.getElementById('tbodyEmploi');
        
        if (emplois && emplois.length > 0) {
            tbody.innerHTML = emplois.map(e => `
                <tr>
                    <td><strong>${e.jour}</strong></td>
                    <td>${e.heure_debut} - ${e.heure_fin}</td>
                    <td>${e.matiere_nom}</td>
                    <td>${e.enseignant_nom}</td>
                    <td>${e.filiere_nom || 'N/A'}</td>
                    <td><span class="badge-ultra primary">${e.salle}</span></td>
                    <td>
                        <button class="btn-ultra btn-ghost-ultra btn-sm-ultra" onclick="supprimerEmploi(${e.id})">🗑️</button>
                    </td>
                </tr>
            `).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:40px;color:rgba(255,255,255,0.5)">Aucun cours programmé</td></tr>';
        }
        
        // Charger les matières et enseignants pour le formulaire
        const matieres = await API.getMatieres();
        const enseignants = await API.getEnseignants();
        
        document.getElementById('selectMatiereEmploi').innerHTML = 
            '<option value="">Sélectionner</option>' +
            matieres.map(m => `<option value="${m.id}">${m.nom} (${m.filiere_nom})</option>`).join('');
        
        document.getElementById('selectEnseignantEmploi').innerHTML = 
            '<option value="">Sélectionner</option>' +
            enseignants.map(e => `<option value="${e.id}">${e.prenom} ${e.nom}</option>`).join('');
            
    } catch (err) {
        console.error('Erreur:', err);
    }
}

async function ajouterEmploi(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    
    try {
        await API.createEmploi(Object.fromEntries(formData));
        showToast('Cours ajouté !', 'success');
        closeModal('modalEmploi');
        form.reset();
        chargerEmploi();
    } catch (err) {
        showToast('Erreur : ' + err.message, 'danger');
    }
}

async function supprimerEmploi(id) {
    if (!confirm('Supprimer ce cours ?')) return;
    try {
        await API.deleteEmploi(id);
        showToast('Cours supprimé', 'success');
        chargerEmploi();
    } catch (err) {
        showToast('Erreur', 'danger');
    }
}
```

### 5. Appeler chargerEmploi() dans navToUltra
Dans la fonction `navToUltra`, ajouter :
```javascript
else if (page === 'emploi') {
    chargerEmploi();
}
```

## Note
En mode MOCK, les ajouts/suppressions ne seront pas persistés (rechargement = données initiales).
Pour une vraie persistance, il faut connecter au backend Django.
