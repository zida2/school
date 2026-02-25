/**
 * FIX NAVIGATION - Correction des bugs d'affichage et navigation
 */

// Fonction globale de navigation corrigée
window.navTo = function(page, el) {
    console.log('Navigation vers:', page);
    
    // Cacher toutes les pages
    document.querySelectorAll('.erp-page').forEach(p => {
        p.style.display = 'none';
    });
    
    // Afficher la page demandée
    const targetPage = document.getElementById('page-' + page);
    if (targetPage) {
        targetPage.style.display = 'block';
        targetPage.style.animation = 'fadeIn 0.3s ease';
    } else {
        console.error('Page non trouvée:', 'page-' + page);
    }
    
    // Mettre à jour la navigation active
    document.querySelectorAll('.nav-item').forEach(i => {
        i.classList.remove('active');
    });
    if (el) {
        el.classList.add('active');
    }
    
    // Mettre à jour le titre
    const titles = {
        dashboard: 'Tableau de bord',
        accueil: 'Mon tableau de bord',
        etudiants: 'Gestion des Étudiants',
        enseignants: 'Gestion des Enseignants',
        filieres: 'Filières & Matières',
        emploidutemps: 'Emploi du Temps',
        notes: 'Notes & Examens',
        paiements: 'Gestion des Paiements',
        statistiques: 'Statistiques & Rapports',
        finance: 'Suivi Financier',
        documents: 'Mes Documents',
        notifs: 'Notifications'
    };
    
    const titleEl = document.getElementById('pageTitle');
    if (titleEl) {
        titleEl.textContent = titles[page] || page;
    }
};

// Toggle sidebar mobile
window.toggleSidebar = function() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    }
};

// Fermer sidebar en cliquant à l'extérieur (mobile)
if (window.innerWidth <= 1024) {
    document.addEventListener('click', function(e) {
        const sidebar = document.querySelector('.sidebar');
        const toggleBtn = document.querySelector('.topbar-btn');
        
        if (sidebar && sidebar.classList.contains('open')) {
            if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        }
    }, { passive: true });
}

// Fonction de déconnexion globale
window.logout = function() {
    if (confirm('Voulez-vous vraiment vous déconnecter ?')) {
        if (typeof API !== 'undefined' && API.logout) {
            API.logout();
        } else {
            localStorage.removeItem('erp_access_token');
            localStorage.removeItem('erp_refresh_token');
            localStorage.removeItem('erp_user');
            window.location.href = 'index.html';
        }
    }
};

// Fonctions modales globales
window.openModal = function(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
};

window.closeModal = function(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
};

// Fermer modal en cliquant sur l'overlay
window.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
        document.body.style.overflow = '';
    }
}, { passive: true });

// Fermer avec la touche Échap
window.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (modal.style.display === 'flex') {
                modal.style.display = 'none';
                document.body.style.overflow = '';
            }
        });
    }
}, { passive: true });

// Fonction de filtrage de table
window.filterTable = function(searchValue, tableId) {
    const query = searchValue.toLowerCase();
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
    });
};

// Export CSV
window.exportTableCSV = function(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) {
        showToast('Tableau introuvable', 'danger');
        return;
    }
    
    let csv = [];
    table.querySelectorAll('tr').forEach(row => {
        const cells = [...row.querySelectorAll('th, td')].map(c => 
            `"${c.textContent.trim().replace(/"/g, '""')}"`
        );
        csv.push(cells.join(','));
    });
    
    const blob = new Blob(['\uFEFF' + csv.join('\n')], { 
        type: 'text/csv;charset=utf-8;' 
    });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    showToast(`Export ${filename} réussi !`, 'success');
};

// Formater la date
window.formatDate = function(dateStr) {
    if (!dateStr) return '—';
    const date = new Date(dateStr);
    return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
};

// Formater la monnaie
window.formatCFA = function(montant) {
    if (!montant && montant !== 0) return '—';
    return new Intl.NumberFormat('fr-FR').format(montant) + ' FCFA';
};

// Badge de note
window.noteBadge = function(note) {
    const n = parseFloat(note);
    if (isNaN(n)) return '<span class="badge badge-muted">—</span>';
    if (n >= 16) return `<span class="note-chip excellent">${n.toFixed(2)}</span>`;
    if (n >= 12) return `<span class="note-chip bien">${n.toFixed(2)}</span>`;
    if (n >= 10) return `<span class="note-chip passable">${n.toFixed(2)}</span>`;
    return `<span class="note-chip echec">${n.toFixed(2)}</span>`;
};

// Toast notification
window.showToast = function(msg, type = 'info', duration = 3500) {
    const icons = { 
        success: '✅', 
        danger: '❌', 
        warning: '⚠️', 
        info: 'ℹ️' 
    };
    
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:10px;';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    const colors = {
        success: '#059669',
        danger: '#dc2626',
        warning: '#d97706',
        info: '#2563a8'
    };
    
    toast.style.cssText = `
        background:#fff;
        border-radius:12px;
        padding:14px 18px;
        box-shadow:0 8px 32px rgba(0,0,0,0.15);
        display:flex;
        align-items:center;
        gap:12px;
        min-width:280px;
        max-width:400px;
        border-left:4px solid ${colors[type]};
        animation:slideIn .3s ease;
        font-family:'Inter',sans-serif;
    `;
    
    toast.innerHTML = `
        <span style="font-size:18px">${icons[type]}</span>
        <span style="font-size:14px;font-weight:500;flex:1;color:#0f2338">${msg}</span>
        <span onclick="this.parentElement.remove()" style="cursor:pointer;color:#94a3b8;flex-shrink:0">✕</span>
    `;
    
    container.appendChild(toast);
    setTimeout(() => { 
        if (toast.parentElement) toast.remove(); 
    }, duration);
};

// Vérifier l'authentification
window.requireAuth = function(allowedRoles = []) {
    const token = localStorage.getItem('erp_access_token');
    const userStr = localStorage.getItem('erp_user');
    
    if (!token || !userStr) {
        window.location.href = 'index.html';
        return false;
    }
    
    try {
        const user = JSON.parse(userStr);
        
        if (allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
            showToast('Accès non autorisé', 'danger');
            window.location.href = 'index.html';
            return false;
        }
        
        return user;
    } catch (e) {
        console.error('Erreur parsing user:', e);
        window.location.href = 'index.html';
        return false;
    }
};

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', function() {
    console.log('Fix navigation chargé');
    
    // Ajouter les animations CSS si elles n'existent pas
    if (!document.getElementById('fix-animations')) {
        const style = document.createElement('style');
        style.id = 'fix-animations';
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(20px); }
                to { opacity: 1; transform: translateX(0); }
            }
            .erp-page {
                animation: fadeIn 0.3s ease;
            }
        `;
        document.head.appendChild(style);
    }
}, { once: true, passive: true });

console.log('✅ Fix navigation initialisé');
