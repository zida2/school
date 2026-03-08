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
    
    // Créer un nouveau lien CSS - THÈME FUTURISTE
    const link = document.createElement('link');
    link.id = 'theme-css';
    link.rel = 'stylesheet';
    link.href = 'css/futuristic-theme.css?v=8.0';
    
    // Ajouter le lien dans le head
    document.head.appendChild(link);
    
    console.log('🚀 Thème futuriste chargé');
}

// Fonction pour basculer le thème (désactivée - thème futuriste permanent)
function toggleTheme() {
    // Thème futuriste permanent - pas de toggle
    showToast('Thème futuriste activé 🚀', 'success');
}

// Charger le thème sauvegardé (toujours futuriste)
function loadTheme() {
    document.body.classList.add('dark-theme');
    loadThemeCSS('futuristic');
}

// Créer le bouton de thème futuriste
function createThemeButton() {
    // Vérifier si le bouton existe déjà
    if (document.getElementById('theme-toggle-btn')) {
        return;
    }
    
    const button = document.createElement('button');
    button.id = 'theme-toggle-btn';
    button.innerHTML = '🚀';
    button.title = 'Thème Futuriste';
    button.onclick = toggleTheme;
    
    // Style du bouton futuriste
    button.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        border: 2px solid #00f0ff;
        background: linear-gradient(135deg, #00f0ff 0%, #8b5cf6 100%);
        color: white;
        font-size: 28px;
        cursor: pointer;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.5);
        z-index: 99999;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulse-glow 2s ease-in-out infinite;
    `;
    
    // Ajouter l'animation CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse-glow {
            0%, 100% { 
                box-shadow: 0 0 30px rgba(0, 240, 255, 0.5);
                transform: scale(1);
            }
            50% { 
                box-shadow: 0 0 50px rgba(0, 240, 255, 0.8);
                transform: scale(1.05);
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
        this.style.transform = 'scale(1.15) rotate(10deg)';
        this.style.boxShadow = '0 0 60px rgba(0, 240, 255, 0.8)';
    });
    button.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) rotate(0deg)';
        this.style.boxShadow = '0 0 30px rgba(0, 240, 255, 0.5)';
    });
    
    document.body.appendChild(button);
    console.log('✅ Bouton thème futuriste créé');
}

// Mettre à jour l'icône du bouton (toujours fusée pour le thème futuriste)
function updateThemeButton() {
    const button = document.getElementById('theme-toggle-btn');
    if (button) {
        button.innerHTML = '🚀';
        button.style.background = 'linear-gradient(135deg, #00f0ff 0%, #8b5cf6 100%)';
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

console.log('🚀 Theme futuriste chargé');

