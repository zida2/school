# Fix: Design modals thème light et erreur 500 demandes 🎨🔧

## Problème 1: Design des modals en thème light
Les modals avaient un fond sombre même en thème light, ce qui créait un contraste désagréable.

### Solution
Ajout de styles spécifiques pour le thème light dans `css/dashboard-light.css`:

```css
body.light-theme .modal-ultra {
    background: rgba(0, 0, 0, 0.5) !important;
}

body.light-theme .modal-content-ultra {
    background: #ffffff !important;
    color: #0F172A !important;
    border: 1px solid rgba(8, 145, 178, 0.2) !important;
    box-shadow: 0 20px 60px rgba(8, 145, 178, 0.15) !important;
}

body.light-theme .modal-header-ultra {
    border-bottom: 1px solid rgba(8, 145, 178, 0.1) !important;
}

body.light-theme .modal-header-ultra h3 {
    color: #0F172A !important;
    font-weight: 700 !important;
}

body.light-theme .modal-close-ultra {
    background: rgba(8, 145, 178, 0.1) !important;
    color: #0891B2 !important;
}

body.light-theme .modal-close-ultra:hover {
    background: rgba(8, 145, 178, 0.2) !important;
    color: #0e7490 !important;
}

body.light-theme .modal-body-ultra {
    color: #0F172A !important;
}

body.light-theme .modal-body-ultra label {
    color: #334155 !important;
    font-weight: 600 !important;
}

body.light-theme .modal-footer-ultra {
    border-top: 1px solid rgba(8, 145, 178, 0.1) !important;
}
```

### Résultat
- Fond blanc pour le contenu du modal
- Texte noir profond (#0F172A) pour une bonne lisibilité
- Bordures cyan doux pour rester dans le thème "eau de mer"
- Ombres cyan subtiles
- Bouton de fermeture avec fond cyan clair

## Problème 2: Erreur 500 sur `/api/demandes-administratives/`
```
Failed to load resource: the server responded with a status of 500 (Internal Server Error)
Erreur chargement demandes: SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

### Cause
Dans `backend/api/views.py`, ligne 1503, le `DemandeAdministrativeViewSet` utilisait:
```python
return qs.order_by('-date_creation')
```

Mais le modèle `DemandeAdministrative` n'a pas de champ `date_creation`, il a `date_demande`.

### Solution
Correction dans `backend/api/views.py`:
```python
# AVANT
return qs.order_by('-date_creation')

# APRÈS
return qs.order_by('-date_demande')
```

### Déploiement backend
```bash
# Sur PythonAnywhere
cd ~/school/backend
git pull origin main
# Recharger l'application web depuis le dashboard PythonAnywhere
```

## Fichiers modifiés
- `css/dashboard-light.css`: Styles modals thème light (ligne ~1678)
- `backend/api/views.py`: Correction order_by (ligne 1503)
- `js/theme-toggle.js`: Version CSS 5.0 → 6.0

## Test
1. Se connecter avec le compte bureau: `bureau@uan.bf / bureau123`
2. Aller dans "Objets perdus"
3. Cliquer sur "+ Déclarer un objet"
4. Vérifier que le modal a un fond blanc avec texte noir
5. Aller dans "Demandes administratives"
6. Vérifier qu'il n'y a plus d'erreur 500

## Version CSS
v5.0 → v6.0

## Notes
- Vider le cache navigateur: `Ctrl + Shift + R` (Chrome/Edge) ou `Ctrl + F5` (Firefox)
- Le backend doit être redéployé sur PythonAnywhere pour corriger l'erreur 500
