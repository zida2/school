# Déploiement Backend - Correction erreur 500 demandes

## Commandes à exécuter sur PythonAnywhere

### 1. Se connecter à PythonAnywhere
- Aller sur https://www.pythonanywhere.com
- Se connecter avec le compte `wendlasida`
- Ouvrir un terminal Bash

### 2. Mettre à jour le code
```bash
cd ~/school/backend
git pull origin main
```

### 3. Vérifier les changements
```bash
git log -1 --oneline
# Devrait afficher: Fix: Design modals thème light et erreur 500 demandes
```

### 4. Recharger l'application web
Deux options:

#### Option A: Via le dashboard (recommandé)
1. Aller dans l'onglet "Web"
2. Trouver l'application `wendlasida.pythonanywhere.com`
3. Cliquer sur le bouton vert "Reload"

#### Option B: Via le terminal
```bash
touch /var/www/wendlasida_pythonanywhere_com_wsgi.py
```

### 5. Tester l'API
```bash
# Tester l'endpoint demandes administratives
curl -H "Authorization: Bearer <TOKEN>" https://wendlasida.pythonanywhere.com/api/demandes-administratives/
```

Ou simplement:
1. Aller sur https://school-wheat-six.vercel.app
2. Se connecter avec `bureau@uan.bf / bureau123`
3. Aller dans "Demandes administratives"
4. Vérifier qu'il n'y a plus d'erreur 500

## Changement effectué
Dans `backend/api/views.py`, ligne 1503:
```python
# AVANT (causait l'erreur 500)
return qs.order_by('-date_creation')

# APRÈS (corrigé)
return qs.order_by('-date_demande')
```

Le champ `date_creation` n'existe pas dans le modèle `DemandeAdministrative`, le bon champ est `date_demande`.

## Vérification
Après le déploiement, l'erreur suivante devrait disparaître:
```
Failed to load resource: the server responded with a status of 500 (Internal Server Error)
Erreur chargement demandes: SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

## Frontend
Le frontend est déjà déployé automatiquement sur Vercel.
Vider le cache: `Ctrl + Shift + R` (Chrome/Edge) ou `Ctrl + F5` (Firefox)

## Résumé des corrections
1. ✅ Design modals thème light (fond blanc, texte noir, bordures cyan)
2. ✅ Erreur 500 demandes administratives (date_creation → date_demande)
3. ✅ Version CSS 5.0 → 6.0
