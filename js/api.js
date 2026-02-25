/**
 * ERP Universitaire BF – Client API
 * Connexion au backend Django REST Framework
 */

const API_BASE = 'http://localhost:8000/api';

// ===== GESTION DES TOKENS =====
const Auth = {
    getAccessToken: () => localStorage.getItem('erp_access_token'),
    getRefreshToken: () => localStorage.getItem('erp_refresh_token'),
    getUser: () => JSON.parse(localStorage.getItem('erp_user') || 'null'),

    setTokens(access, refresh, user) {
        localStorage.setItem('erp_access_token', access);
        localStorage.setItem('erp_refresh_token', refresh);
        localStorage.setItem('erp_user', JSON.stringify(user));
    },

    clear() {
        localStorage.removeItem('erp_access_token');
        localStorage.removeItem('erp_refresh_token');
        localStorage.removeItem('erp_user');
    },

    isLoggedIn() {
        return !!this.getAccessToken();
    },

    async refreshAccessToken() {
        const refresh = this.getRefreshToken();
        if (!refresh) return false;
        try {
            const res = await fetch(`${API_BASE}/auth/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh })
            });
            if (res.ok) {
                const data = await res.json();
                localStorage.setItem('erp_access_token', data.access);
                return true;
            }
            return false;
        } catch {
            return false;
        }
    }
};

// ===== REQUÊTE API CENTRALE =====
async function apiRequest(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    // Ajouter le token Bearer
    const token = Auth.getAccessToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    // Ne pas envoyer Content-Type pour FormData (upload)
    if (options.body instanceof FormData) {
        delete headers['Content-Type'];
    }

    let res = await fetch(url, { ...options, headers });

    // Token expiré → rafraîchir et réessayer
    if (res.status === 401 && Auth.getRefreshToken()) {
        const refreshed = await Auth.refreshAccessToken();
        if (refreshed) {
            headers['Authorization'] = `Bearer ${Auth.getAccessToken()}`;
            res = await fetch(url, { ...options, headers });
        } else {
            Auth.clear();
            window.location.href = 'index.html';
            return null;
        }
    }

    // Retourner null si pas de contenu
    if (res.status === 204) return null;

    const data = await res.json();
    if (!res.ok) {
        const errMsg = extractError(data);
        throw new Error(errMsg);
    }
    // Si c'est une réponse paginée de DRF, on retourne directement le tableau de résultats
    if (data && typeof data === 'object' && 'results' in data && Array.isArray(data.results)) {
        return data.results;
    }
    return data;
}

function extractError(data) {
    if (typeof data === 'string') return data;
    if (data.detail) return data.detail;
    if (data.non_field_errors) return data.non_field_errors.join(', ');
    const firstKey = Object.keys(data)[0];
    if (firstKey) {
        const val = data[firstKey];
        return `${firstKey}: ${Array.isArray(val) ? val.join(', ') : val}`;
    }
    return 'Erreur inconnue';
}

// ===== API CALLS =====
const API = {
    // Auth
    async login(email, password) {
        const data = await apiRequest('/auth/login/', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        if (data) {
            Auth.setTokens(data.access, data.refresh, data.user);
        }
        return data;
    },

    async logout() {
        const refresh = Auth.getRefreshToken();
        try {
            await apiRequest('/auth/logout/', {
                method: 'POST',
                body: JSON.stringify({ refresh })
            });
        } catch (e) { }
        Auth.clear();
        window.location.href = 'index.html';
    },

    async getMe() {
        return apiRequest('/auth/me/');
    },

    async changePassword(old_password, new_password) {
        return apiRequest('/auth/change-password/', {
            method: 'POST',
            body: JSON.stringify({ old_password, new_password })
        });
    },

    // Dashboard
    async getDashboardAdmin() { return apiRequest('/dashboard/admin/'); },
    async getDashboardProf() { return apiRequest('/dashboard/prof/'); },
    async getDashboardEtudiant() { return apiRequest('/dashboard/etudiant/'); },

    // Universités
    async getUniversites() { return apiRequest('/universites/'); },
    async createUniversite(data) { return apiRequest('/universites/', { method: 'POST', body: JSON.stringify(data) }); },
    async updateUniversite(id, data) { return apiRequest(`/universites/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }); },
    async deleteUniversite(id) { return apiRequest(`/universites/${id}/`, { method: 'DELETE' }); },

    // Filières
    async getFilieres(params = {}) {
        const q = new URLSearchParams(params).toString();
        return apiRequest(`/filieres/${q ? '?' + q : ''}`);
    },
    async createFiliere(data) { return apiRequest('/filieres/', { method: 'POST', body: JSON.stringify(data) }); },
    async updateFiliere(id, data) { return apiRequest(`/filieres/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }); },
    async deleteFiliere(id) { return apiRequest(`/filieres/${id}/`, { method: 'DELETE' }); },

    // Matières
    async getMatieres(params = {}) {
        const q = new URLSearchParams(params).toString();
        return apiRequest(`/matieres/${q ? '?' + q : ''}`);
    },
    async createMatiere(data) { return apiRequest('/matieres/', { method: 'POST', body: JSON.stringify(data) }); },
    async updateMatiere(id, data) { return apiRequest(`/matieres/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }); },
    async deleteMatiere(id) { return apiRequest(`/matieres/${id}/`, { method: 'DELETE' }); },

    // Enseignants
    async getEnseignants(search = '') {
        return apiRequest(`/enseignants/${search ? '?search=' + search : ''}`);
    },
    async getEnseignant(id) { return apiRequest(`/enseignants/${id}/`); },
    async createEnseignant(data) { return apiRequest('/enseignants/', { method: 'POST', body: JSON.stringify(data) }); },
    async updateEnseignant(id, data) { return apiRequest(`/enseignants/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }); },
    async resetPasswordEnseignant(id) { return apiRequest(`/enseignants/${id}/reset_password/`, { method: 'POST' }); },

    // Étudiants
    async getEtudiants(params = {}) {
        const q = new URLSearchParams(params).toString();
        return apiRequest(`/etudiants/${q ? '?' + q : ''}`);
    },
    async getEtudiant(id) { return apiRequest(`/etudiants/${id}/`); },
    async createEtudiant(data) { return apiRequest('/etudiants/', { method: 'POST', body: JSON.stringify(data) }); },
    async updateEtudiant(id, data) { return apiRequest(`/etudiants/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }); },
    async deleteEtudiant(id) { return apiRequest(`/etudiants/${id}/`, { method: 'DELETE' }); },
    async bloquerEtudiant(id) { return apiRequest(`/etudiants/${id}/bloquer/`, { method: 'POST' }); },
    async debloquerEtudiant(id) { return apiRequest(`/etudiants/${id}/debloquer/`, { method: 'POST' }); },
    async getBulletinEtudiant(id) { return apiRequest(`/etudiants/${id}/bulletin/`); },
    async getPaiementsEtudiant(id) { return apiRequest(`/etudiants/${id}/paiements/`); },

    // Notes
    async getNotes(params = {}) {
        const q = new URLSearchParams(params).toString();
        return apiRequest(`/notes/${q ? '?' + q : ''}`);
    },
    async createNote(data) { return apiRequest('/notes/', { method: 'POST', body: JSON.stringify(data) }); },
    async updateNote(id, data) { return apiRequest(`/notes/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }); },
    async deleteNote(id) { return apiRequest(`/notes/${id}/`, { method: 'DELETE' }); },
    async publierNotes(matiere_id, annee_academique_id) {
        return apiRequest('/notes/publier/', { method: 'POST', body: JSON.stringify({ matiere_id, annee_academique_id }) });
    },
    async confirmerNote(id) { return apiRequest(`/notes/${id}/confirmer/`, { method: 'POST' }); },
    async reclamerNote(id, motif) { return apiRequest(`/notes/${id}/reclamer/`, { method: 'POST', body: JSON.stringify({ motif }) }); },

    // Paiements
    async getPaiements(params = {}) {
        const q = new URLSearchParams(params).toString();
        return apiRequest(`/paiements/${q ? '?' + q : ''}`);
    },
    async createPaiement(data) { return apiRequest('/paiements/', { method: 'POST', body: JSON.stringify(data) }); },

    // Emploi du temps
    async getEmploisDuTemps(params = {}) {
        const q = new URLSearchParams(params).toString();
        return apiRequest(`/emplois-du-temps/${q ? '?' + q : ''}`);
    },
    async createEmploi(data) { return apiRequest('/emplois-du-temps/', { method: 'POST', body: JSON.stringify(data) }); },
    async updateEmploi(id, data) { return apiRequest(`/emplois-du-temps/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }); },
    async deleteEmploi(id) { return apiRequest(`/emplois-du-temps/${id}/`, { method: 'DELETE' }); },

    // Présences
    async getPresences(params = {}) {
        const q = new URLSearchParams(params).toString();
        return apiRequest(`/presences/${q ? '?' + q : ''}`);
    },
    async enregistrerSession(emploi_id, date_cours, presences) {
        return apiRequest('/presences/enregistrer_session/', {
            method: 'POST',
            body: JSON.stringify({ emploi_id, date_cours, presences })
        });
    },

    // Supports de cours
    async getSupports(params = {}) {
        const q = new URLSearchParams(params).toString();
        return apiRequest(`/supports/${q ? '?' + q : ''}`);
    },
    async createSupport(formData) {
        return apiRequest('/supports/', { method: 'POST', body: formData });
    },
    async deleteSupport(id) { return apiRequest(`/supports/${id}/`, { method: 'DELETE' }); },

    // Notifications
    async getNotifications() { return apiRequest('/notifications/'); },
    async lireNotification(id) { return apiRequest(`/notifications/${id}/lire/`, { method: 'POST' }); },
    async toutLireNotifications() { return apiRequest('/notifications/tout_lire/', { method: 'POST' }); },

    // Années académiques
    async getAnnees(params = {}) {
        const q = new URLSearchParams(params).toString();
        return apiRequest(`/annees/${q ? '?' + q : ''}`);
    },
    async createAnnee(data) { return apiRequest('/annees/', { method: 'POST', body: JSON.stringify(data) }); },
    async activerAnnee(id) { return apiRequest(`/annees/${id}/activer/`, { method: 'POST' }); },

    // Évaluations
    async getEvaluations(params = {}) {
        const q = new URLSearchParams(params).toString();
        return apiRequest(`/evaluations/${q ? '?' + q : ''}`);
    },
    async getEvaluation(id) { return apiRequest(`/evaluations/${id}/`); },
    async createEvaluation(data) { return apiRequest('/evaluations/', { method: 'POST', body: JSON.stringify(data) }); },
    async updateEvaluation(id, data) { return apiRequest(`/evaluations/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }); },
    async deleteEvaluation(id) { return apiRequest(`/evaluations/${id}/`, { method: 'DELETE' }); },
    async genererNotesEvaluation(id) { return apiRequest(`/evaluations/${id}/generer_notes/`, { method: 'POST' }); },

    // Notes d'évaluations
    async getNotesEvaluations(params = {}) {
        const q = new URLSearchParams(params).toString();
        return apiRequest(`/notes-evaluations/${q ? '?' + q : ''}`);
    },
    async getNoteEvaluation(id) { return apiRequest(`/notes-evaluations/${id}/`); },
    async createNoteEvaluation(data) { return apiRequest('/notes-evaluations/', { method: 'POST', body: JSON.stringify(data) }); },
    async updateNoteEvaluation(id, data) { return apiRequest(`/notes-evaluations/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }); },
    async deleteNoteEvaluation(id) { return apiRequest(`/notes-evaluations/${id}/`, { method: 'DELETE' }); },
};
