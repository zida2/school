/**
 * THEME TOGGLE - Changement de thème Dark/Light
 */

// Fonction pour basculer le thème
function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.contains('dark-theme');
    
    if (isDark) {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        localStorage.setItem('erp_theme', 'light');
    } else {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        localStorage.setItem('erp_theme', 'dark');
    }
    
    // Animation de transition
    body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
}

// Charger le thème sauvegardé
function loadTheme() {
    const savedTheme = localStorage.getItem('erp_theme') || 'dark';
    document.body.classList.add(savedTheme + '-theme');
}

// Créer le bouton de thème
function createThemeButton() {
    const button = document.createElement('button');
    button.id = 'theme-toggle-btn';
    button.innerHTML = '🌙';
    button.title = 'Changer le thème';
    button.onclick = function() {
        toggleTheme();
        updateThemeButton();
    };
    
    // Style du bouton
    button.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        z-index: 9999;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    // Hover effect
    button.onmouseenter = function() {
        this.style.transform = 'scale(1.1) rotate(10deg)';
        this.style.boxShadow = '0 6px 20px rgba(0,0,0,0.4)';
    };
    button.onmouseleave = function() {
        this.style.transform = 'scale(1) rotate(0deg)';
        this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.3)';
    };
    
    document.body.appendChild(button);
}

// Mettre à jour l'icône du bouton
function updateThemeButton() {
    const button = document.getElementById('theme-toggle-btn');
    if (button) {
        const isDark = document.body.classList.contains('dark-theme');
        button.innerHTML = isDark ? '🌙' : '☀️';
    }
}

// Initialiser au chargement
document.addEventListener('DOMContentLoaded', function() {
    loadTheme();
    createThemeButton();
    updateThemeButton();
});

console.log('✅ Theme toggle chargé');
