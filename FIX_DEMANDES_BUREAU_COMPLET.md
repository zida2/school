# Fix: Demandes administratives pour le bureau exécutif 📨✅

## Problème
Le bureau exécutif ne pouvait ni voir ni traiter les demandes administratives:
- Bouton "Nouvelle demande" inapproprié (le bureau ne crée pas de demandes)
- Pas de fonctionnalité pour voir les détails
- Pas de fonctionnalité pour traiter les demandes

## Contexte
Les demandes administratives sont créées par les étudiants et traitées par:
- Le bureau exécutif (toutes les demandes)
- Les admins (demandes administratives)
- Les enseignants (demandes qui leur sont adressées)

Le bureau ne peut PAS créer de demandes car le modèle `DemandeAdministrative` requiert un champ `etudiant` (ForeignKey vers Etudiant).

## Solution implémentée

### 1. Modification de la page demandes
**Changements:**
- Titre: "Mes demandes" → "Demandes administratives"
- Sous-titre: "Soumettre et suivre vos demandes" → "Consulter et traiter les demandes des étudiants"
- Suppression du bouton "Nouvelle demande"
- Ajout d'une colonne "Étudiant" dans le tableau
- Ajout de boutons d'action: 👁️ Voir et ✅ Traiter

### 2. Ajout de 2 modals

#### Modal "Voir demande"
Affiche les détails complets d'une demande:
- Étudiant
- Type de demande
- Objet
- Description
- Date de demande
- Statut
- Commentaire admin (si présent)
- Date de traitement (si présent)
- Traité par (si présent)

#### Modal "Traiter demande"
Permet de traiter une demande:
- Affichage des infos de la demande
- Sélection du statut: En traitement, Approuvé, Rejeté, Terminé
- Champ commentaire pour l'étudiant
- Boutons Annuler/Enregistrer

### 3. Fonctions JavaScript ajoutées

#### `chargerDemandes()` (mise à jour)
```javascript
- Affiche 6 colonnes: Date, Étudiant, Type, Objet, Statut, Actions
- Bouton 👁️ pour voir les détails (toujours visible)
- Bouton ✅ pour traiter (visible uniquement si statut = 'en_attente')
- Badges colorés selon le statut:
  * success: approuvé
  * danger: rejeté
  * info: terminé
  * warning: en_attente, en_traitement
```

#### `voirDemande(id)`
```javascript
- Récupère les détails via GET /api/demandes-administratives/{id}/
- Affiche dans le modal modalVoirDemande
- Formatage avec badges et sections colorées
```

#### `ouvrirModalTraiter(id)`
```javascript
- Récupère la demande via GET /api/demandes-administratives/{id}/
- Pré-remplit les infos dans le modal modalTraiterDemande
- Stocke l'ID dans un champ caché
```

#### `traiterDemande(event)`
```javascript
- Récupère les données du formulaire
- Envoie via POST /api/demandes-administratives/{id}/traiter/
- Affiche un toast de succès/erreur
- Ferme le modal et recharge la liste
```

## API Backend
L'endpoint existe déjà et est fonctionnel:
- `GET /api/demandes-administratives/`: Liste des demandes (filtrée par rôle)
- `GET /api/demandes-administratives/{id}/`: Détails d'une demande
- `POST /api/demandes-administratives/{id}/traiter/`: Traiter une demande

Permissions:
- Bureau: Voir toutes les demandes et les traiter
- Admin: Voir les demandes administratives et les traiter
- Enseignant: Voir les demandes qui lui sont adressées
- Étudiant: Voir uniquement ses propres demandes

## Structure HTML

### Tableau des demandes
```html
<table class="table-ultra">
    <thead>
        <tr>
            <th>Date</th>
            <th>Étudiant</th>
            <th>Type</th>
            <th>Objet</th>
            <th>Statut</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody id="tbodyDemandes">
        <!-- Rempli dynamiquement -->
    </tbody>
</table>
```

### Modal Voir
```html
<div class="modal-ultra" id="modalVoirDemande">
    <div class="modal-content-ultra">
        <div class="modal-header-ultra">
            <h3>📝 Détails de la demande</h3>
            <span class="modal-close-ultra" onclick="closeModal('modalVoirDemande')">&times;</span>
        </div>
        <div class="modal-body-ultra">
            <div id="detailsDemande">
                <!-- Rempli dynamiquement -->
            </div>
        </div>
        <div class="modal-footer-ultra">
            <button type="button" class="btn-ultra btn-ghost-ultra" onclick="closeModal('modalVoirDemande')">Fermer</button>
        </div>
    </div>
</div>
```

### Modal Traiter
```html
<div class="modal-ultra" id="modalTraiterDemande">
    <div class="modal-content-ultra">
        <div class="modal-header-ultra">
            <h3>✅ Traiter la demande</h3>
            <span class="modal-close-ultra" onclick="closeModal('modalTraiterDemande')">&times;</span>
        </div>
        <div class="modal-body-ultra">
            <form id="formTraiterDemande" onsubmit="traiterDemande(event)">
                <input type="hidden" id="demandeIdTraiter">
                <div id="demandeInfoTraiter">
                    <!-- Info demande -->
                </div>
                <div class="form-group-ultra">
                    <label>Statut *</label>
                    <select name="statut" required class="form-input-ultra">
                        <option value="">Sélectionner...</option>
                        <option value="en_traitement">En traitement</option>
                        <option value="approuve">Approuvé</option>
                        <option value="rejete">Rejeté</option>
                        <option value="termine">Terminé</option>
                    </select>
                </div>
                <div class="form-group-ultra">
                    <label>Commentaire</label>
                    <textarea name="commentaire_admin" rows="4" class="form-input-ultra"></textarea>
                </div>
                <div class="modal-footer-ultra">
                    <button type="button" class="btn-ultra btn-ghost-ultra" onclick="closeModal('modalTraiterDemande')">Annuler</button>
                    <button type="submit" class="btn-ultra btn-primary-ultra">Enregistrer</button>
                </div>
            </form>
        </div>
    </div>
</div>
```

## Test
1. Se connecter avec le compte bureau: `bureau@uan.bf / bureau123`
2. Aller dans "Demandes administratives"
3. Vérifier que la liste des demandes s'affiche (avec les étudiants)
4. Cliquer sur 👁️ pour voir les détails d'une demande
5. Cliquer sur ✅ pour traiter une demande en attente
6. Sélectionner un statut et ajouter un commentaire
7. Enregistrer et vérifier le toast de succès
8. Vérifier que le statut est mis à jour dans la liste

## Fichiers modifiés
- `dashboard-bureau.html`: Page demandes complète avec modals et fonctions JS

## Déploiement
```bash
git add dashboard-bureau.html FIX_DEMANDES_BUREAU_COMPLET.md
git commit -m "Fix: Demandes administratives complètes pour bureau 📨✅"
git push origin main
```

Le déploiement sur Vercel est automatique.
Vider le cache: `Ctrl + Shift + R`

## Notes
- Le bureau ne peut pas créer de demandes (réservé aux étudiants)
- Le bureau peut voir et traiter toutes les demandes
- Les modals utilisent le design unifié avec le thème light/dark
- Les fonctions utilisent l'API existante (pas de changement backend nécessaire)
