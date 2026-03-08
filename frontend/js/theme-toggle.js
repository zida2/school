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
    
    // Créer un nouveau lien CSS - THÈME CLASSIQUE (dark ou light)
    const link = document.createElement('link');
    link.id = 'theme-css';
    link.rel = 'stylesheet';
    link.href = `css/dashboard.css?v=13.0`;
    
    // Ajouter le lien dans le head
    document.head.appendChild(link);
    
    console.log('✅ Thème classique chargé:', theme);
}

// Fonction pour basculer le thème
function toggleTheme() {
    const currentTheme = localStorage.getItem('theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    localStorage.setItem('theme', newTheme);
    document.body.classList.remove('dark-theme', 'light-theme');
    document.body.classList.add(newTheme + '-theme');
    
    loadThemeCSS(newTheme);
    
    if (typeof showToast === 'function') {
        showToast('Thème ' + (newTheme === 'dark' ? 'sombre' : 'clair') + ' activé', 'success');
    }
}

// Charger le thème sauvegardé
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.classList.add(savedTheme + '-theme');
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
    button.innerHTML = '☀️';
    button.title = 'Changer de thème';
    button.onclick = function() {
        toggleTheme();
        updateThemeButton();
    };
    
    // Style du bouton simple
    button.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 2px solid rgba(255, 255, 255, 0.2);
        background: rgba(0, 0, 0, 0.5);
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        z-index: 99999;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    // Hover effect simple
    button.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1)';
        this.style.boxShadow = '0 6px 16px rgba(0, 0, 0, 0.4)';
    });
    button.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
        this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.3)';
    });
    
    document.body.appendChild(button);
    console.log('✅ Bouton thème créé');
}

// Mettre à jour l'icône du bouton selon le thème
function updateThemeButton() {
    const button = document.getElementById('theme-toggle-btn');
    if (button) {
        const currentTheme = localStorage.getItem('theme') || 'dark';
        button.innerHTML = currentTheme === 'dark' ? '☀️' : '🌙';
    }
}

// Initialiser immédiatement si le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        loadTheme();
        createThemeButton();
        updateThemeButton();
    });
} else {
    // DOM déjà chargé
    loadTheme();
    createThemeButton();
    updateThemeButton();
}

// Aussi essayer après un court délai pour être sûr
setTimeout(function() {
    if (!document.getElementById('theme-toggle-btn')) {
        createThemeButton();
        updateThemeButton();
    }
}, 500);

console.log('✅ Theme classique chargé');

