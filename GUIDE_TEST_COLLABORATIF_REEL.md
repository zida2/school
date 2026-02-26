# 🎯 GUIDE DE TEST COLLABORATIF EN TEMPS RÉEL
## Test avec 4 personnes réelles

Date: 26 février 2026

---

## 👥 ÉQUIPE DE TEST

### Vous (Super Admin)
- Accès à tous les comptes
- Supervision générale
- Vérification que tout fonctionne

### Testeur 1 - Admin
- **Email**: admin@uan.bf
- **Password**: admin123
- **Rôle**: Gérer les demandes administratives

### Testeur 2 - Enseignant
- **Email**: j.ouedraogo@uan.bf
- **Password**: enseignant123
- **Rôle**: Traiter les réclamations et demandes

### Testeur 3 - Étudiant
- **Email**: m.diallo@etu.bf
- **Password**: etudiant123
- **Rôle**: Créer des demandes et réclamations

### Testeur 4 - Bureau
- **Email**: bureau@uan.bf
- **Password**: bureau123
- **Rôle**: Créer des publications et sondages

---

## ✅ CONFIGURATION VÉRIFIÉE

```
✅ Étudiant: Moussa Diallo (L1 Informatique)
✅ Enseignant: Jean Ouedraogo (9 matières)
✅ Lien établi: 7 notes communes
✅ Admin: Prêt à répondre
✅ Bureau: Prêt à publier
```

---

## 🎬 SCÉNARIOS DE TEST

### Scénario 1: Réclamation sur une Note (10 min)

#### Étape 1: Étudiant crée une réclamation
```
Testeur 3 (Étudiant):
1. Se connecter: m.diallo@etu.bf / etudiant123
2. Aller dans "Mes notes"
3. Choisir une note (ex: Algorithmique CC=14)
4. Cliquer sur "⚠️ Signaler"
5. Remplir:
   - Type: Note incorrecte
   - Description: "Ma note devrait être 16/20 au lieu de 14/20"
6. Envoyer
7. DIRE À HAUTE VOIX: "Réclamation envoyée!"
```

#### Étape 2: Enseignant traite la réclamation
```
Testeur 2 (Enseignant):
1. ATTENDRE le signal de l'étudiant
2. Rafraîchir la page (F5)
3. Vérifier le badge rouge sur "Réclamations"
4. Cliquer sur "Réclamations"
5. Voir la réclamation de Moussa Diallo
6. Cliquer sur "Traiter"
7. Choisir "Accepter"
8. Entrer nouvelle note CC: 16
9. Écrire réponse: "Note corrigée après vérification"
10. Envoyer
11. DIRE À HAUTE VOIX: "Réclamation traitée!"
```

#### Étape 3: Étudiant vérifie
```
Testeur 3 (Étudiant):
1. ATTENDRE le signal de l'enseignant
2. Rafraîchir la page (F5)
3. Aller dans "Mes notes"
4. VÉRIFIER: Note CC = 16/20 ✅
5. VÉRIFIER: Moyenne recalculée ✅
6. Aller dans "Services" → "Réclamations"
7. Cliquer sur "👁️ Voir réponse"
8. LIRE la réponse de l'enseignant
9. DIRE À HAUTE VOIX: "Note corrigée reçue!"
```

---

### Scénario 2: Demande à l'Enseignant (8 min)

#### Étape 1: Étudiant contacte l'enseignant
```
Testeur 3 (Étudiant):
1. Aller dans "👨‍🏫 Mes enseignants"
2. Voir la carte de Jean Ouedraogo
3. Cliquer sur "📨 Contacter"
4. Le modal s'ouvre (pré-rempli)
5. Remplir:
   - Type: Demande de rendez-vous
   - Objet: "Discussion sur le projet final"
   - Description: "Je souhaite discuter de mon projet..."
6. Envoyer
7. DIRE: "Demande envoyée à l'enseignant!"
```

#### Étape 2: Enseignant répond
```
Testeur 2 (Enseignant):
1. ATTENDRE le signal
2. Rafraîchir (F5)
3. Vérifier les notifications
4. Aller dans "Demandes" (si disponible)
5. Voir la demande de Moussa
6. Répondre: "RDV accepté, vendredi 14h"
7. DIRE: "Réponse envoyée!"
```

#### Étape 3: Étudiant vérifie
```
Testeur 3 (Étudiant):
1. ATTENDRE le signal
2. Rafraîchir (F5)
3. Aller dans "Demandes"
4. Cliquer sur "👁️ Voir"
5. LIRE la réponse de Jean Ouedraogo
6. DIRE: "Réponse reçue!"
```

---

### Scénario 3: Demande Administrative (8 min)

#### Étape 1: Étudiant crée une demande
```
Testeur 3 (Étudiant):
1. Aller dans "Services" → "Demandes"
2. Cliquer sur "+ Nouvelle demande"
3. Remplir:
   - Destinataire: Administration
   - Type: Certificat de scolarité
   - Objet: "Demande de certificat pour stage"
   - Description: "J'ai besoin d'un certificat..."
4. Envoyer
5. DIRE: "Demande admin envoyée!"
```

#### Étape 2: Admin répond
```
Testeur 1 (Admin):
1. ATTENDRE le signal
2. Rafraîchir (F5)
3. Vérifier le badge sur "Demandes"
4. Aller dans "Demandes"
5. Voir la demande de Moussa Diallo
6. Cliquer sur "💬 Répondre"
7. Statut: Traitée
8. Réponse: "Certificat prêt, à retirer au secrétariat"
9. Envoyer
10. DIRE: "Réponse admin envoyée!"
```

#### Étape 3: Étudiant vérifie
```
Testeur 3 (Étudiant):
1. ATTENDRE le signal
2. Rafraîchir (F5)
3. Aller dans "Demandes"
4. Cliquer sur "👁️ Voir"
5. LIRE la réponse de l'administration
6. DIRE: "Réponse admin reçue!"
```

---

### Scénario 4: Publication du Bureau (5 min)

#### Étape 1: Bureau crée une publication
```
Testeur 4 (Bureau):
1. Se connecter: bureau@uan.bf / bureau123
2. Aller dans "Publications"
3. Créer une nouvelle publication
4. Titre: "Journée portes ouvertes"
5. Contenu: "Samedi 15 mars, venez découvrir..."
6. Publier
7. DIRE: "Publication créée!"
```

#### Étape 2: Étudiant voit la publication
```
Testeur 3 (Étudiant):
1. ATTENDRE le signal
2. Rafraîchir (F5)
3. Aller dans "Publications"
4. VOIR la nouvelle publication
5. DIRE: "Publication reçue!"
```

---

## 📊 CHECKLIST DE VÉRIFICATION

### Communication Étudiant ↔️ Enseignant
- [ ] Réclamation créée par l'étudiant
- [ ] Badge notification chez l'enseignant
- [ ] Réclamation visible par l'enseignant
- [ ] Traitement et correction de note
- [ ] Note mise à jour chez l'étudiant
- [ ] Réponse visible par l'étudiant
- [ ] Demande créée par l'étudiant
- [ ] Réponse de l'enseignant
- [ ] Réponse visible par l'étudiant

### Communication Étudiant ↔️ Admin
- [ ] Demande créée par l'étudiant
- [ ] Badge notification chez l'admin
- [ ] Demande visible par l'admin
- [ ] Réponse de l'admin
- [ ] Réponse visible par l'étudiant

### Communication Bureau → Étudiant
- [ ] Publication créée par le bureau
- [ ] Publication visible par l'étudiant

---

## 🎯 CONSEILS POUR LE TEST

### Avant de Commencer
1. **Tous les testeurs** doivent avoir le lien: `http://127.0.0.1:8080/`
2. **Vérifier** que le serveur Django tourne
3. **Se connecter** chacun avec son compte
4. **Tester** la connexion avant de commencer

### Pendant le Test
1. **Communiquer** à haute voix à chaque étape
2. **Rafraîchir** (F5) après chaque action de l'autre
3. **Vérifier** les badges de notification
4. **Prendre des captures** d'écran si problème
5. **Noter** les bugs ou comportements étranges

### En Cas de Problème
1. **Vérifier** la console (F12)
2. **Vérifier** les logs Django
3. **Rafraîchir** la page
4. **Se reconnecter** si nécessaire
5. **Appeler** le super admin (vous)

---

## 🐛 PROBLÈMES COURANTS

### Badge ne se met pas à jour
**Solution**: Rafraîchir la page (F5)

### Réclamation non visible
**Solution**: 
- Vérifier que l'enseignant enseigne à l'étudiant
- Vérifier les logs Django

### Demande non visible
**Solution**:
- Vérifier le destinataire
- Rafraîchir la page

### Note non mise à jour
**Solution**:
- Vérifier que la réclamation est "acceptée"
- Rafraîchir la page de l'étudiant

---

## 📞 COMMANDES UTILES (Pour Vous)

### Vérifier la configuration
```bash
cd backend
python verifier_configuration_test.py
```

### Voir les logs Django
```bash
cd backend
python manage.py runserver
# Les logs s'affichent dans le terminal
```

### Vérifier la base de données
```bash
cd backend
python manage.py shell
>>> from api.models import ReclamationNote, DemandeAdministrative
>>> ReclamationNote.objects.all()
>>> DemandeAdministrative.objects.all()
```

---

## 🎊 RÉSULTAT ATTENDU

Après tous les tests:

✅ **Étudiant** a:
- Créé 1 réclamation → Traitée par l'enseignant
- Créé 1 demande à l'enseignant → Réponse reçue
- Créé 1 demande à l'admin → Réponse reçue
- Vu 1 publication du bureau
- Vu ses notes corrigées

✅ **Enseignant** a:
- Traité 1 réclamation
- Corrigé 1 note
- Répondu à 1 demande

✅ **Admin** a:
- Répondu à 1 demande

✅ **Bureau** a:
- Créé 1 publication

✅ **Communication bidirectionnelle** fonctionne!

---

## 🚀 DÉMARRAGE DU TEST

### Ordre de Connexion
1. **Vous** (Super Admin) - Supervision
2. **Testeur 3** (Étudiant) - Se connecte en premier
3. **Testeur 2** (Enseignant) - Se connecte
4. **Testeur 1** (Admin) - Se connecte
5. **Testeur 4** (Bureau) - Se connecte

### Ordre des Scénarios
1. Scénario 1: Réclamation (10 min)
2. Scénario 2: Demande à l'enseignant (8 min)
3. Scénario 3: Demande à l'admin (8 min)
4. Scénario 4: Publication (5 min)

**Durée totale**: ~30 minutes

---

## 📝 NOTES POUR VOUS (Super Admin)

### Avant le Test
- [ ] Serveur Django démarré
- [ ] Configuration vérifiée (script exécuté)
- [ ] Lien partagé aux testeurs
- [ ] Comptes communiqués

### Pendant le Test
- [ ] Observer les actions de chacun
- [ ] Vérifier les logs Django
- [ ] Noter les bugs
- [ ] Aider en cas de problème

### Après le Test
- [ ] Demander le feedback
- [ ] Noter les améliorations
- [ ] Corriger les bugs trouvés

---

Date: 26 février 2026
Version: 1.0
Statut: ✅ PRÊT POUR LE TEST COLLABORATIF

**Bon test!** 🎉
