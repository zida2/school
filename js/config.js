/**
 * Configuration de l'application
 * Permet de basculer entre développement et production
 */

const CONFIG = {
    // URL de l'API
    // En développement: http://localhost:8000/api
    // En production: https://votre-username.pythonanywhere.com/api
    API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000/api'
        : 'https://Wendlasida.pythonanywhere.com/api',
    
    // Mode de l'application
    IS_PRODUCTION: window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1',
    
    // Version de l'application
    VERSION: '1.0.1',
    
    // Nom de l'application
    APP_NAME: 'UniERP BF'
};

// Exposer la configuration globalement
window.CONFIG = CONFIG;

// Log de la configuration (uniquement en développement)
if (!CONFIG.IS_PRODUCTION) {
    console.log('📋 Configuration:', CONFIG);
    console.log('🌐 API URL:', CONFIG.API_URL);
    console.log('🔧 Mode:', CONFIG.IS_PRODUCTION ? 'Production' : 'Développement');
}
