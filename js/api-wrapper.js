/**
 * Wrapper API - Utilise MockAPI si USE_MOCK = true
 */

// Intercepter toutes les méthodes API
if (typeof USE_MOCK !== 'undefined' && USE_MOCK && typeof MockAPI !== 'undefined') {
    console.log('🎭 Mode MOCK activé - Utilisation de MockAPI');
    
    // Remplacer l'objet API par MockAPI
    const OriginalAPI = { ...API };
    
    Object.keys(MockAPI).forEach(method => {
        if (typeof MockAPI[method] === 'function') {
            API[method] = MockAPI[method];
        }
    });
    
    // Garder les méthodes qui n'existent pas dans MockAPI
    Object.keys(OriginalAPI).forEach(method => {
        if (!MockAPI[method] && typeof OriginalAPI[method] === 'function') {
            API[method] = OriginalAPI[method];
        }
    });
}
