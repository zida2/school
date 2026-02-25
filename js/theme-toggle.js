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
    updateThemeButton();
}

// Charger le thème sauvegardé
function loadTheme() {
    const savedTheme = localStorage.getItem('erp_theme') || 'dark';
    if (!document.body.classList.contains('dark-theme') && !document.body.classList.contains('light-theme')) {
        document.body.classList.add(savedTheme + '-theme');
    }
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
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
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
