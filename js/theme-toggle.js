/**
 * THEME TOGGLE - Changement de thème Dark/Light avec chargement dynamique des CSS
 */

// Fonction pour charger le CSS du thème
function loadThemeCSS(theme) {
    // Supprimer l'ancien lien CSS du thème s'il existe
    const oldLink = document.getElementById('theme-css');
    if (oldLink) {
        oldLink.remove();
    }
    
    // Créer un nouveau lien CSS
    const link = document.createElement('link');
    link.id = 'theme-css';
    link.rel = 'stylesheet';
    link.href = theme === 'light' ? 'css/dashboard-light.css?v=3.0' : 'css/dashboard-dark-premium.css?v=3.0';
    
    // Ajouter le lien dans le head
    document.head.appendChild(link);
}

// Fonction pour basculer le thème
function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.contains('dark-theme');
    
    if (isDark) {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        localStorage.setItem('erp_theme', 'light');
        loadThemeCSS('light');
    } else {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        localStorage.setItem('erp_theme', 'dark');
        loadThemeCSS('dark');
    }
    
    // Animation de transition
    body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    updateThemeButton();
    
    // Afficher un toast
    showToast(`Thème ${isDark ? 'clair' : 'sombre'} activé`, 'success');
}

// Charger le thème sauvegardé
function loadTheme() {
    const savedTheme = localStorage.getItem('erp_theme') || 'dark';
    if (!document.body.classList.contains('dark-theme') && !document.body.classList.contains('light-theme')) {
        document.body.classList.add(savedTheme + '-theme');
    }
    loadThemeCSS(savedTheme);
}

// Créer le bouton de thème
function createThemeButton() {
    // Vérifier si le bouton existe déjà
    if (document.getElementById('theme-toggle-btn')) {
        return;
    }
    
    const button = document.createElement('button');
    button.id = 'theme-toggle-btn';
    button.innerHTML = '🌙';
    button.title = 'Changer le thème';
    button.onclick = toggleTheme;
    
    // Style du bouton
    button.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 28px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        z-index: 99999;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeInUp 0.5s ease-out;
    `;
    
    // Ajouter l'animation CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        #theme-toggle-btn:active {
            animation: spin 0.5s ease-in-out;
        }
    `;
    document.head.appendChild(style);
    
    // Hover effect
    button.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1) rotate(10deg)';
        this.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
    });
    button.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) rotate(0deg)';
        this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.3)';
    });
    
    document.body.appendChild(button);
    console.log('✅ Bouton de thème créé');
    updateThemeButton();
}

// Mettre à jour l'icône du bouton
function updateThemeButton() {
    const button = document.getElementById('theme-toggle-btn');
    if (button) {
        const isDark = document.body.classList.contains('dark-theme');
        button.innerHTML = isDark ? '🌙' : '☀️';
        
        // Changer le gradient selon le thème
        if (isDark) {
            button.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        } else {
            button.style.background = 'linear-gradient(135deg, #0891B2 0%, #14B8A6 100%)';
        }
    }
}

// Initialiser immédiatement si le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        loadTheme();
        createThemeButton();
    });
} else {
    // DOM déjà chargé
    loadTheme();
    createThemeButton();
}

// Aussi essayer après un court délai pour être sûr
setTimeout(function() {
    if (!document.getElementById('theme-toggle-btn')) {
        createThemeButton();
    }
}, 500);

console.log('✅ Theme toggle chargé');

