# 🧪 GUIDE DE TEST COMPLET DU SYSTÈME

**Date**: 6 mars 2026  
**Objectif**: Tester le système après nettoyage de la base de données

---

## 📋 PRÉREQUIS

✅ Base de données nettoyée (script exécuté)  
✅ Application redémarrée sur PythonAnywhere  
✅ Frontend déployé sur Vercel  

---

## 🔐 IDENTIFIANTS ADMIN

- **Email**: admin@unierp.bf
- **Mot de passe**: Admin2026

---

## 🧪 TEST 1: Connexion Admin

### Étapes:
1. Ouvrir: https://school-wheat-six.vercel.app/connexion-admin.html
2. Entrer les identifiants admin
3. Cliquer sur "Se connecter"

### Résultat attendu:
✅ Redirection vers le dashboard admin  
✅ Pas d'erreur de connexion  

---

## 🧪 TEST 2: Page de Gestion des Inscriptions

### Étapes:
1. Ouvrir: https://school-wheat-six.vercel.app/gestion-inscriptions.html
2. Vérifier les statistiques
3. Cliquer sur chaque onglet (Communication, Académique, Comptabilité, Professeurs)

### Résultat attendu:
✅ Statistiques affichent tous 0  
✅ Message "Aucune demande" dans chaque onglet  
✅ Les 4 onglets fonctionnent  
✅ Pas d'erreur de chargement  

---

## 🧪 TEST 3: Inscription Service Communication

### Étapes:
1. Ouvrir: https://school-wheat-six.vercel.app/inscription-communication.html
2. Remplir le formulaire:
   - Nom: Test
   - Prénom: Communication
   - Email: test.comm@example.com
   - Téléphone: 70123456
   - Poste souhaité: Chargé de communication
   - Motivation: Test du système
3. Soumettre le formulaire

### Résultat attendu:
✅ Message de succès  
✅ Formulaire réinitialisé  

---

## 🧪 TEST 4: Validation de la Demande

### Étapes:
1. Retourner sur: https://school-wheat-six.vercel.app/gestion-inscriptions.html
2. Aller dans l'onglet "Communication"
3. Vérifier que la demande apparaît
4. Cliquer sur "Valider"

### Résultat attendu:
✅ Demande visible dans le tableau  
✅ Statut "En attente"  
✅ Popup s'affiche avec:
   - Email: test.comm@example.com
   - Mot de passe généré (ex: comm12ab34cd)  
✅ Statistiques mises à jour (1 validée)  
✅ Demande passe en statut "Validée"  

**IMPORTANT**: Noter le mot de passe affiché!

---

## 🧪 TEST 5: Connexion avec le Nouveau Compte

### Étapes:
1. Se déconnecter du compte admin
2. Ouvrir: https://school-wheat-six.vercel.app/connexion-communication.html
3. Entrer:
   - Email: test.comm@example.com
   - Mot de passe: (celui affiché dans la popup)
4. Se connecter

### Résultat attendu:
✅ Connexion réussie  
✅ Redirection vers le dashboard Communication  
✅ Pas d'erreur  

---

## 🧪 TEST 6: Inscription Service Académique

### Étapes:
1. Ouvrir: https://school-wheat-six.vercel.app/inscription-academique.html
2. Remplir le formulaire:
   - Nom: Test
   - Prénom: Academique
   - Email: test.acad@example.com
   - Téléphone: 70234567
   - Poste souhaité: Responsable académique
   - Motivation: Test du système
3. Soumettre

### Résultat attendu:
✅ Message de succès  

---

## 🧪 TEST 7: Validation Service Académique

### Étapes:
1. Se reconnecter en admin
2. Aller sur: https://school-wheat-six.vercel.app/gestion-inscriptions.html
3. Onglet "Académique"
4. Valider la demande

### Résultat attendu:
✅ Demande validée  
✅ Mot de passe affiché  
✅ Statistiques mises à jour  

---

## 🧪 TEST 8: Inscription Service Comptabilité

### Étapes:
1. Ouvrir: https://school-wheat-six.vercel.app/inscription-comptabilite.html
2. Remplir le formulaire:
   - Nom: Test
   - Prénom: Comptabilite
   - Email: test.compta@example.com
   - Téléphone: 70345678
   - Poste souhaité: Comptable
   - Motivation: Test du système
3. Soumettre

### Résultat attendu:
✅ Message de succès  

---

## 🧪 TEST 9: Validation Service Comptabilité

### Étapes:
1. En tant qu'admin
2. Onglet "Comptabilité"
3. Valider la demande

### Résultat attendu:
✅ Demande validée  
✅ Mot de passe affiché  

---

## 🧪 TEST 10: Inscription Professeur

### Étapes:
1. Ouvrir: https://school-wheat-six.vercel.app/inscription-professeur.html
2. Remplir le formulaire:
   - Nom: Test
   - Prénom: Professeur
   - Email: test.prof@example.com
   - Téléphone: 70456789
   - Filière: (sélectionner une filière)
   - Diplôme: Master
   - Expérience: 5 ans
   - Motivation: Test du système
3. Soumettre

### Résultat attendu:
✅ Message de succès  

---

## 🧪 TEST 11: Validation Professeur

### Étapes:
1. En tant qu'admin
2. Onglet "Professeurs"
3. Valider la demande

### Résultat attendu:
✅ Demande validée  
✅ Mot de passe affiché  

---

## 🧪 TEST 12: Rejet d'une Demande

### Étapes:
1. Créer une nouvelle demande (n'importe quel service)
2. En tant qu'admin, cliquer sur "Rejeter"
3. Entrer un commentaire: "Test de rejet"
4. Confirmer

### Résultat attendu:
✅ Demande rejetée  
✅ Statut "Rejetée"  
✅ Statistiques mises à jour  
✅ Boutons Valider/Rejeter disparaissent  

---

## 🧪 TEST 13: Actualisation des Données

### Étapes:
1. Sur la page de gestion
2. Cliquer sur "Actualiser"

### Résultat attendu:
✅ Données rechargées  
✅ Statistiques à jour  
✅ Pas d'erreur  

---

## 🧪 TEST 14: Changement de Mot de Passe

### Étapes:
1. Se connecter avec un compte créé
2. Ouvrir: https://school-wheat-six.vercel.app/changer-mot-de-passe.html
3. Entrer:
   - Ancien mot de passe
   - Nouveau mot de passe (min 8 caractères)
   - Confirmer le nouveau
4. Soumettre

### Résultat attendu:
✅ Message de succès  
✅ Déconnexion automatique  
✅ Reconnexion avec nouveau mot de passe fonctionne  

---

## 🧪 TEST 15: Application Mobile PWA

### Étapes:
1. Ouvrir: https://school-wheat-six.vercel.app/mobile/
2. Vérifier l'affichage
3. Tester l'inscription étudiant
4. Vérifier le Service Worker (console)

### Résultat attendu:
✅ Page s'affiche correctement  
✅ Pas d'erreur dans la console  
✅ Service Worker enregistré  
✅ Icône SVG chargée  

---

## 📊 RÉSUMÉ DES TESTS

| Test | Description | Statut |
|------|-------------|--------|
| 1 | Connexion admin | ⬜ |
| 2 | Page gestion inscriptions | ⬜ |
| 3 | Inscription Communication | ⬜ |
| 4 | Validation Communication | ⬜ |
| 5 | Connexion nouveau compte | ⬜ |
| 6 | Inscription Académique | ⬜ |
| 7 | Validation Académique | ⬜ |
| 8 | Inscription Comptabilité | ⬜ |
| 9 | Validation Comptabilité | ⬜ |
| 10 | Inscription Professeur | ⬜ |
| 11 | Validation Professeur | ⬜ |
| 12 | Rejet demande | ⬜ |
| 13 | Actualisation | ⬜ |
| 14 | Changement mot de passe | ⬜ |
| 15 | PWA Mobile | ⬜ |

---

## 🐛 EN CAS DE PROBLÈME

### Erreur de connexion
- Vérifier que le backend est actif: https://wendlasida.pythonanywhere.com/api/
- Vérifier les identifiants
- Vider le cache du navigateur

### Demandes ne s'affichent pas
- Vérifier le token dans localStorage
- Actualiser la page
- Vérifier la console pour les erreurs

### Validation ne fonctionne pas
- Vérifier que le statut est "en_attente"
- Vérifier les permissions admin
- Consulter les logs backend

### Mot de passe ne s'affiche pas
- Vérifier la réponse de l'API dans la console
- Vérifier que la modal Bootstrap est chargée

---

## ✅ CRITÈRES DE SUCCÈS

Le système est considéré comme fonctionnel si:
- ✅ Tous les tests passent
- ✅ Aucune erreur dans la console
- ✅ Les statistiques sont correctes
- ✅ Les mots de passe sont générés et affichés
- ✅ Les connexions fonctionnent
- ✅ Les statuts changent correctement

---

**BON TEST!** 🚀
