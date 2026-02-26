# 🧪 TEST - AFFICHAGE DES RÉPONSES ÉTUDIANT
## Guide de test rapide

Date: 26 février 2026

---

## 🎯 OBJECTIF

Tester l'affichage des réponses aux demandes et réclamations côté étudiant.

---

## ✅ TEST 1: RÉPONSE À UNE DEMANDE ADMINISTRATIVE

### Étape 1: Créer une demande (Étudiant)

1. **Se connecter**
   ```
   URL: http://127.0.0.1:8080/index.html
   Email: m.diallo@etu.bf
   Password: etudiant123
   ```

2. **Créer une demande**
   - Cliquer sur "Demandes" dans la sidebar (section Services)
   - Cliquer sur "+ Nouvelle demande"
   - Remplir:
     ```
     Destinataire: Administration
     Type: Certificat de scolarité
     Objet: Demande de certificat pour stage
     Description: Je souhaite obtenir un certificat de scolarité 
                  pour postuler à un stage en entreprise.
     ```
   - Cliquer sur "📤 Envoyer"
   - ✅ Vérifier: Toast "Demande envoyée avec succès!"

### Étape 2: Répondre à la demande (Admin)

1. **Se déconnecter et se reconnecter en tant qu'admin**
   - Cliquer sur le profil → Déconnexion
   - Cliquer sur "Administrateur" dans Accès rapide
   - OU entrer: `admin@uan.bf` / `admin123`

2. **Répondre à la demande**
   - Aller dans "Demandes" (sidebar, section SERVICES)
   - Trouver la demande de Moussa Diallo
   - Cliquer sur l'icône 💬 (Répondre)
   - Remplir:
     ```
     Statut: Traitée
     Réponse: Votre certificat de scolarité est prêt.
              Vous pouvez le retirer au secrétariat du lundi au vendredi 
              de 8h à 16h. Munissez-vous de votre carte d'étudiant.
     ```
   - Cliquer sur "Envoyer"
   - ✅ Vérifier: Toast "Réponse envoyée"

### Étape 3: Voir la réponse (Étudiant) ⭐ NOUVEAU

1. **Se reconnecter en tant qu'étudiant**
   - Se déconnecter
   - Cliquer sur "Étudiant L1" dans Accès rapide

2. **Consulter la réponse**
   - Aller dans "Services" → "Demandes"
   - ✅ Vérifier: La demande a le statut "traitee" (badge vert)
   - Cliquer sur "👁️ Voir" sur la demande
   - ✅ Vérifier que le modal s'ouvre avec:
     * Destinataire: Administration
     * Type: Certificat de scolarité
     * Objet: Demande de certificat pour stage
     * Description complète
     * **Section "RÉPONSE DE L'ADMINISTRATION" avec fond vert** ⭐
     * Texte de la réponse de l'admin
     * Date de réponse
   - Cliquer sur "Fermer"
   - ✅ Vérifier: Le modal se ferme correctement

---

## ✅ TEST 2: RÉPONSE À UNE RÉCLAMATION

### Étape 1: Créer une réclamation (Étudiant)

1. **Se connecter en tant qu'étudiant**
   ```
   Email: m.diallo@etu.bf
   Password: etudiant123
   ```

2. **Créer une réclamation**
   - Aller dans "Mes notes"
   - Trouver une note dans le tableau
   - Cliquer sur "⚠️ Signaler"
   - Remplir:
     ```
     Type de problème: Note incorrecte / erreur de saisie
     Description: Ma note de CC devrait être 15/20 au lieu de 12/20.
                  J'ai vérifié avec ma copie corrigée.
     Note correcte attendue: CC: 15/20
     ```
   - Cliquer sur "📤 Envoyer la réclamation"
   - ✅ Vérifier: Toast "Réclamation envoyée avec succès!"

### Étape 2: Traiter la réclamation (Enseignant)

1. **Se reconnecter en tant qu'enseignant**
   - Se déconnecter
   - Cliquer sur "Enseignant" dans Accès rapide
   - OU entrer: `j.ouedraogo@uan.bf` / `enseignant123`

2. **Traiter la réclamation**
   - Aller dans "Réclamations" (sidebar)
   - ✅ Vérifier: Badge rouge avec "1"
   - Trouver la réclamation de Moussa Diallo
   - Cliquer sur "Traiter"
   - Dans le modal:
     * Choisir "Accepter (Résoudre)" dans Décision
     * ✅ Vérifier: Section "Correction de la note" apparaît (fond vert)
     * Entrer "15" dans "Nouvelle note CC"
     * Écrire une réponse:
       ```
       Après vérification de votre copie, vous avez raison.
       Votre note de CC a été corrigée de 12/20 à 15/20.
       La moyenne a été recalculée automatiquement.
       ```
   - Cliquer sur "Envoyer"
   - ✅ Vérifier: Toast "Réclamation traitée avec succès"

### Étape 3: Voir la réponse (Étudiant) ⭐ NOUVEAU

1. **Se reconnecter en tant qu'étudiant**
   - Se déconnecter
   - Cliquer sur "Étudiant L1"

2. **Vérifier la note corrigée**
   - Aller dans "Mes notes"
   - ✅ Vérifier: La note CC est maintenant 15/20
   - ✅ Vérifier: La moyenne est recalculée

3. **Consulter la réponse** ⭐ NOUVEAU
   - Aller dans "Services" → "Réclamations"
   - ✅ Vérifier: La réclamation a le statut "resolue" (badge vert)
   - ✅ Vérifier: Colonne "Actions" affiche "👁️ Voir réponse"
   - Cliquer sur "👁️ Voir réponse"
   - ✅ Vérifier que le modal s'ouvre avec:
     * **Informations générales**:
       - Matière
       - Enseignant
       - Date de création
       - Statut: Résolue (badge vert)
     * **Notes concernées** (fond bleu):
       - Note CC: 12/20 (ancienne)
       - Note Examen
       - Moyenne (ancienne)
     * **Type de problème**: Note incorrecte (badge)
     * **Votre description**: Texte complet
     * **Note attendue**: CC: 15/20
     * **RÉPONSE DE L'ENSEIGNANT** (fond vert) ⭐:
       - Icône ✅
       - Titre: "RÉPONSE DE L'ENSEIGNANT - Acceptée"
       - Texte de la réponse
       - **NOTES CORRIGÉES** ⭐:
         * Nouvelle note CC: 15/20 (en vert)
         * Nouvelle moyenne: [calculée] (en vert)
       - Date de traitement
   - Cliquer sur "Fermer"
   - ✅ Vérifier: Le modal se ferme correctement

---

## ✅ TEST 3: DEMANDE EN ATTENTE

### Étape 1: Créer une demande sans réponse

1. **Se connecter en tant qu'étudiant**
2. **Créer une nouvelle demande**
   - Aller dans "Services" → "Demandes"
   - Cliquer sur "+ Nouvelle demande"
   - Remplir rapidement
   - Envoyer

### Étape 2: Consulter immédiatement

1. **Cliquer sur "👁️ Voir" sur la nouvelle demande**
2. ✅ Vérifier que le modal affiche:
   - Toutes les informations de la demande
   - Statut: "En attente" (badge jaune)
   - **Message d'information** (fond jaune):
     * Icône ⏳
     * Texte: "Votre demande est en attente de traitement"
   - PAS de section "Réponse"

---

## ✅ TEST 4: RÉCLAMATION EN ATTENTE

### Étape 1: Créer une réclamation sans réponse

1. **Se connecter en tant qu'étudiant**
2. **Créer une nouvelle réclamation**
   - Aller dans "Mes notes"
   - Cliquer sur "⚠️ Signaler" sur une note
   - Remplir et envoyer

### Étape 2: Consulter dans la liste

1. **Aller dans "Services" → "Réclamations"**
2. ✅ Vérifier que la nouvelle réclamation affiche:
   - Statut: "en_attente" (badge jaune)
   - Colonne "Actions": Texte "En attente" (pas de bouton)

---

## ✅ TEST 5: RÉCLAMATION REJETÉE

### Étape 1: Créer et rejeter une réclamation

1. **Créer une réclamation** (étudiant)
2. **Traiter et rejeter** (enseignant):
   - Choisir "Rejeter" dans Décision
   - Écrire une justification:
     ```
     Après vérification, la note saisie est correcte.
     Elle correspond bien à votre copie corrigée.
     ```
   - Envoyer

### Étape 2: Voir la réponse (Étudiant)

1. **Se reconnecter en tant qu'étudiant**
2. **Aller dans "Services" → "Réclamations"**
3. ✅ Vérifier: Statut "rejetee" (badge rouge)
4. **Cliquer sur "👁️ Voir réponse"**
5. ✅ Vérifier que le modal affiche:
   - **RÉPONSE DE L'ENSEIGNANT** (fond rouge) ⭐:
     * Icône ❌
     * Titre: "RÉPONSE DE L'ENSEIGNANT - Rejetée"
     * Texte de la justification
     * PAS de section "Notes corrigées"
     * Date de traitement

---

## 📊 CHECKLIST COMPLÈTE

### Demandes
- [ ] Création de demande fonctionne
- [ ] Bouton "👁️ Voir" visible dans le tableau
- [ ] Modal s'ouvre au clic
- [ ] Toutes les informations s'affichent
- [ ] Réponse s'affiche avec fond vert (si disponible)
- [ ] Message "En attente" s'affiche (si pas de réponse)
- [ ] Date de réponse s'affiche
- [ ] Modal se ferme correctement

### Réclamations
- [ ] Création de réclamation fonctionne
- [ ] Colonne "Actions" affiche correctement:
  - [ ] "👁️ Voir réponse" si réponse disponible
  - [ ] "En attente" si pas de réponse
- [ ] Modal s'ouvre au clic
- [ ] Informations générales s'affichent
- [ ] Notes concernées s'affichent (fond bleu)
- [ ] Type de problème s'affiche
- [ ] Description s'affiche
- [ ] Note attendue s'affiche (si spécifiée)
- [ ] Réponse s'affiche avec bon fond (vert/rouge)
- [ ] Notes corrigées s'affichent (si acceptée)
- [ ] Nouvelle moyenne s'affiche (si acceptée)
- [ ] Date de traitement s'affiche
- [ ] Message "En attente" s'affiche (si pas de réponse)
- [ ] Modal se ferme correctement

### Design
- [ ] Badges colorés selon le statut
- [ ] Icônes appropriées (✅, ❌, ⏳, 🔄)
- [ ] Fonds colorés selon le type de réponse
- [ ] Responsive sur mobile
- [ ] Animations fluides

---

## 🐛 PROBLÈMES POSSIBLES

### Modal ne s'ouvre pas
**Solution**: 
- Vérifier la console (F12)
- Vérifier que l'ID de la demande/réclamation est correct
- Rafraîchir la page

### Réponse ne s'affiche pas
**Solution**:
- Vérifier que la réponse a bien été envoyée (côté admin/enseignant)
- Rafraîchir la page étudiant
- Vérifier les logs Django

### Erreur 401/403
**Solution**:
- Se reconnecter
- Vérifier le token JWT

---

## 🎊 RÉSULTAT ATTENDU

Après tous les tests:

✅ Les étudiants peuvent voir les réponses à leurs demandes
✅ Les étudiants peuvent voir les réponses à leurs réclamations
✅ Les notes corrigées sont visibles
✅ Les nouvelles moyennes sont affichées
✅ Les messages d'état sont clairs
✅ Le design est moderne et intuitif

**Le système de communication bidirectionnelle est 100% opérationnel!** 🚀

---

Date: 26 février 2026
Version: 1.0

