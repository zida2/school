# 🧪 GUIDE DE TEST - COMMUNICATION BIDIRECTIONNELLE
## Test des flux Réclamations et Demandes

Date: 26 février 2026

---

## 🎯 OBJECTIF

Tester la communication bidirectionnelle entre les acteurs du système ERP.

---

## 👥 COMPTES DE DÉMONSTRATION

### 🎓 Étudiant
```
Email: m.diallo@etu.bf
Password: etudiant123
Nom: Moussa Diallo
Niveau: L1 Informatique
```

### 👨‍🏫 Enseignant
```
Email: j.ouedraogo@uan.bf
Password: enseignant123
Nom: Jean Ouedraogo
Matières: Informatique
```

### 👔 Administrateur
```
Email: admin@uan.bf
Password: admin123
Rôle: Admin
```

### 🏛️ Bureau Exécutif
```
Email: bureau@uan.bf
Password: bureau123
Rôle: Bureau Exécutif
```

---

## 🔄 TEST 1: FLUX RÉCLAMATION (Étudiant → Enseignant)

### Étape 1: Créer une réclamation (Étudiant)

1. **Se connecter en tant qu'étudiant**
   - Aller sur: `http://127.0.0.1:8080/index.html`
   - Cliquer sur "Étudiant L1" dans Accès rapide
   - OU entrer: `m.diallo@etu.bf` / `etudiant123`

2. **Créer une réclamation**
   - Aller dans "Notes" (sidebar)
   - Trouver une note dans le tableau
   - Cliquer sur "Réclamer" (bouton à droite)
   - Remplir le formulaire:
     ```
     Motif: Erreur de calcul
     Description: Ma note de CC devrait être 15/20 au lieu de 12/20
     ```
   - Cliquer sur "Envoyer"
   - ✅ Vérifier: Toast "Réclamation créée avec succès"

### Étape 2: Voir et traiter la réclamation (Enseignant)

1. **Se déconnecter et se reconnecter en tant qu'enseignant**
   - Cliquer sur le profil en haut à droite → Déconnexion
   - Cliquer sur "Enseignant" dans Accès rapide
   - OU entrer: `j.ouedraogo@uan.bf` / `enseignant123`

2. **Voir les réclamations**
   - Aller dans "Réclamations" (sidebar)
   - ✅ Vérifier: Badge rouge avec "1" sur le lien
   - ✅ Vérifier: La réclamation apparaît dans le tableau
   - ✅ Vérifier: Statut "en_attente" (badge jaune)

3. **Traiter la réclamation**
   - Cliquer sur "Traiter" (bouton à droite)
   - Le modal s'ouvre avec:
     - Info étudiant et matière
     - Description de la réclamation
     - Formulaire de traitement
   
4. **Accepter et corriger la note**
   - Choisir "Accepter (Résoudre)" dans Décision
   - ✅ Vérifier: Section "Correction de la note" apparaît (fond vert)
   - Entrer dans "Nouvelle note CC": `15`
   - Entrer dans "Nouvelle note Examen": `14` (ou laisser vide)
   - Écrire une réponse:
     ```
     Après vérification, votre note de CC a été corrigée. 
     La moyenne a été recalculée automatiquement.
     ```
   - Cliquer sur "Envoyer"
   - ✅ Vérifier: Toast "Réclamation traitée avec succès"
   - ✅ Vérifier: La réclamation disparaît du tableau (ou statut change)
   - ✅ Vérifier: Badge se met à jour (0)

### Étape 3: Vérifier la correction (Étudiant)

1. **Se reconnecter en tant qu'étudiant**
   - Se déconnecter
   - Cliquer sur "Étudiant L1" dans Accès rapide

2. **Vérifier la note corrigée**
   - Aller dans "Notes"
   - ✅ Vérifier: La note CC est maintenant 15/20
   - ✅ Vérifier: La moyenne est recalculée automatiquement
   - Exemple: Si CC=15 et Examen=14 → Moyenne=(15+14)/2=14.5

3. **Voir la réponse de l'enseignant**
   - Aller dans "Services" → "Réclamations"
   - ✅ Vérifier: Statut "resolue" (badge vert)
   - Cliquer sur "Voir" pour lire la réponse
   - ✅ Vérifier: La réponse de l'enseignant s'affiche

---

## 🔄 TEST 2: FLUX DEMANDE (Étudiant → Admin)

### Étape 1: Créer une demande (Étudiant)

1. **Se connecter en tant qu'étudiant**
   - Cliquer sur "Étudiant L1" dans Accès rapide

2. **Créer une demande**
   - Aller dans "Services" (sidebar)
   - Cliquer sur "Demandes administratives"
   - Cliquer sur "+ Nouvelle demande"
   - Remplir le formulaire:
     ```
     Destinataire: Administration
     Type: Certificat de scolarité
     Objet: Demande de certificat pour stage
     Description: Je souhaite obtenir un certificat de scolarité 
                  pour postuler à un stage en entreprise.
     ```
   - Cliquer sur "Envoyer"
   - ✅ Vérifier: Toast "Demande créée avec succès"

### Étape 2: Voir et répondre à la demande (Admin)

1. **Se reconnecter en tant qu'admin**
   - Se déconnecter
   - Cliquer sur "Administrateur" dans Accès rapide
   - OU entrer: `admin@uan.bf` / `admin123`

2. **Voir les demandes**
   - Aller dans "Demandes" (sidebar, section SERVICES)
   - ✅ Vérifier: Badge avec "1" sur le lien
   - ✅ Vérifier: La demande apparaît dans le tableau
   - ✅ Vérifier: Statut "en_attente" (badge jaune)

3. **Voir les détails**
   - Cliquer sur l'icône 👁️ (Voir)
   - ✅ Vérifier: Modal s'ouvre avec tous les détails
   - ✅ Vérifier: Nom étudiant, type, objet, description
   - Fermer le modal

4. **Répondre à la demande**
   - Cliquer sur l'icône 💬 (Répondre)
   - Le modal s'ouvre avec:
     - Info de la demande
     - Formulaire de réponse
   
5. **Envoyer la réponse**
   - Choisir statut: "Traitée"
   - Écrire la réponse:
     ```
     Votre certificat de scolarité est prêt.
     Vous pouvez le retirer au secrétariat du lundi au vendredi 
     de 8h à 16h. Munissez-vous de votre carte d'étudiant.
     ```
   - Cliquer sur "Envoyer"
   - ✅ Vérifier: Toast "Réponse envoyée"
   - ✅ Vérifier: La demande change de statut
   - ✅ Vérifier: Badge se met à jour

### Étape 3: Voir la réponse (Étudiant)

1. **Se reconnecter en tant qu'étudiant**
   - Se déconnecter
   - Cliquer sur "Étudiant L1"

2. **Voir la réponse**
   - Aller dans "Services" → "Demandes administratives"
   - ✅ Vérifier: Statut "traitee" (badge vert)
   - Cliquer sur "Voir" pour lire la réponse
   - ✅ Vérifier: La réponse de l'admin s'affiche

---

## 🔄 TEST 3: FLUX DEMANDE À ENSEIGNANT

### Étape 1: Créer une demande pour un enseignant (Étudiant)

1. **Se connecter en tant qu'étudiant**

2. **Créer une demande**
   - Aller dans "Services" → "Demandes administratives"
   - Cliquer sur "+ Nouvelle demande"
   - Remplir:
     ```
     Destinataire: Professeur
     Professeur concerné: [Sélectionner J. Ouedraogo]
     Type: Autre
     Objet: Demande de rendez-vous
     Description: Je souhaite vous rencontrer pour discuter 
                  de mon projet de fin d'année.
     ```
   - Envoyer

### Étape 2: Répondre (Enseignant)

1. **Se connecter en tant qu'enseignant**
   - `j.ouedraogo@uan.bf` / `enseignant123`

2. **Voir et répondre**
   - Aller dans "Demandes" (si disponible)
   - OU l'enseignant voit ses demandes dans son espace
   - Répondre à la demande

---

## ✅ CHECKLIST DE TEST

### Flux Réclamation
- [ ] Étudiant peut créer une réclamation
- [ ] Enseignant voit la réclamation dans sa liste
- [ ] Badge de notification s'affiche (nombre)
- [ ] Enseignant peut ouvrir le modal de traitement
- [ ] Section correction apparaît si "Accepter"
- [ ] Enseignant peut corriger les notes
- [ ] Réclamation est traitée avec succès
- [ ] Note est mise à jour dans la base
- [ ] Moyenne est recalculée automatiquement
- [ ] Badge se met à jour après traitement
- [ ] Étudiant voit la note corrigée
- [ ] Étudiant voit la réponse de l'enseignant

### Flux Demande
- [ ] Étudiant peut créer une demande
- [ ] Admin voit la demande dans sa liste
- [ ] Badge de notification s'affiche
- [ ] Admin peut voir les détails
- [ ] Admin peut ouvrir le modal de réponse
- [ ] Admin peut envoyer une réponse
- [ ] Demande change de statut
- [ ] Badge se met à jour
- [ ] Étudiant voit la réponse

---

## 🐛 PROBLÈMES POSSIBLES

### Erreur 401 (Non autorisé)
**Cause**: Token JWT expiré
**Solution**: Se reconnecter

### Erreur 403 (Interdit)
**Cause**: Permissions insuffisantes
**Solution**: Vérifier le rôle de l'utilisateur

### Erreur 500 (Serveur)
**Cause**: Erreur backend
**Solution**: 
1. Vérifier que le serveur Django tourne
2. Vérifier les logs dans le terminal
3. Vérifier les migrations: `python manage.py migrate`

### Badge ne se met pas à jour
**Cause**: Cache du navigateur
**Solution**: 
1. Rafraîchir la page (F5)
2. Vider le cache (Ctrl+Shift+R)
3. Recharger les données

### Note non mise à jour
**Cause**: Erreur dans l'API
**Solution**:
1. Vérifier les logs Django
2. Vérifier que l'endpoint `/api/reclamations/{id}/traiter/` fonctionne
3. Tester avec curl ou Postman

---

## 📊 RÉSULTATS ATTENDUS

### Après Test Réclamation
- ✅ Note CC corrigée: 15/20
- ✅ Moyenne recalculée: (15+14)/2 = 14.5/20
- ✅ Statut réclamation: "resolue"
- ✅ Réponse visible par l'étudiant

### Après Test Demande
- ✅ Statut demande: "traitee"
- ✅ Réponse visible par l'étudiant
- ✅ Badge admin: 0 (si toutes traitées)

---

## 🎯 SCÉNARIOS AVANCÉS

### Test 1: Rejeter une réclamation
1. Créer une réclamation (étudiant)
2. Traiter et choisir "Rejeter" (enseignant)
3. Écrire une justification
4. Vérifier que la note n'est PAS modifiée
5. Vérifier que le statut est "rejetee"

### Test 2: Demande en cours
1. Créer une demande (étudiant)
2. Répondre avec statut "En cours de traitement" (admin)
3. Vérifier que le statut est "en_cours" (badge bleu)
4. Plus tard, répondre avec "Traitée"

### Test 3: Plusieurs réclamations
1. Créer 3 réclamations (étudiant)
2. Vérifier que le badge affiche "3"
3. Traiter 1 réclamation
4. Vérifier que le badge affiche "2"
5. Traiter toutes les réclamations
6. Vérifier que le badge affiche "0"

---

## 📞 AIDE

### Commandes utiles

```bash
# Voir les logs Django
cd backend
python manage.py runserver
# Les logs s'affichent dans le terminal

# Tester un endpoint
curl -X GET http://127.0.0.1:8000/api/reclamations/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Vérifier la base de données
python manage.py shell
>>> from api.models import ReclamationNote, Note
>>> ReclamationNote.objects.all()
>>> Note.objects.filter(etudiant__utilisateur__email='m.diallo@etu.bf')
```

### Console du navigateur (F12)

```javascript
// Voir les données chargées
console.log(toutesReclamations);
console.log(toutesDemandes);

// Tester l'API
API.get('/reclamations/').then(console.log);
API.get('/demandes-administratives/').then(console.log);

// Voir le token
console.log(localStorage.getItem('token'));
```

---

## 🎊 CONCLUSION

Si tous les tests passent, vous avez:
- ✅ Communication bidirectionnelle fonctionnelle
- ✅ Correction automatique des notes
- ✅ Notifications en temps réel
- ✅ Système opérationnel

**Le système ERP est prêt!** 🚀

---

Date: 26 février 2026
Version: 1.0
