# CAHIER DES CHARGES DÉTAILLÉ

## Projet de développement d'une application mobile étudiante et d'une plateforme administrative intelligente

---

## 1. Présentation du projet

Dans le cadre de la modernisation de la gestion académique et administrative, l'établissement souhaite développer une solution numérique intégrée composée de :

1. **Une application mobile destinée aux étudiants**
2. **Une plateforme web administrative destinée aux services internes**

Cette solution vise à centraliser les informations académiques, améliorer la communication administrative et automatiser certaines tâches.

**Contrairement aux systèmes traditionnels** qui diffusent des informations de manière générale, cette solution doit permettre une **communication individualisée et intelligente**, c'est-à-dire que chaque étudiant recevra uniquement les informations qui le concernent directement.

### Cela permettra :
- d'éviter la confusion des informations
- d'améliorer l'expérience des étudiants
- de faciliter la gestion interne
- de renforcer l'efficacité des services administratifs

---

## 2. Objectifs stratégiques du projet

### 2.1 Objectif principal
Mettre en place une plateforme numérique intelligente permettant de connecter les étudiants et les services administratifs autour d'un système centralisé de gestion académique, administrative et financière.

### 2.2 Objectifs spécifiques
La solution devra permettre de :
- diffuser les informations de manière personnalisée à chaque étudiant
- automatiser la gestion des programmes de cours
- permettre aux étudiants de consulter leurs notes et informations académiques
- informer les étudiants en temps réel des changements ou imprévus
- améliorer la gestion financière et la communication du service comptabilité
- faciliter la collecte de données stratégiques pour le marketing institutionnel
- améliorer l'expérience numérique des étudiants

---

## 3. Architecture générale de la solution

La solution doit être structurée autour de trois composantes principales.

### 3.1 Application mobile étudiant
L'application mobile sera l'interface principale des étudiants avec l'administration.

Elle permettra aux étudiants de :
- recevoir des notifications personnalisées
- consulter leurs programmes
- consulter leurs notes
- recevoir des informations administratives
- consulter leur situation financière
- participer à des sondages

### 3.2 Plateforme web administrative
La plateforme web permettra aux services administratifs de gérer l'ensemble des informations diffusées aux étudiants.

Elle sera utilisée par :
- Service Communication et Accueil
- Service Académique
- Service Comptabilité
- Administrateur général

### 3.3 Base de données centralisée
Une base de données centralisée permettra de stocker :
- les informations des étudiants
- les programmes de cours
- les notes
- les données financières
- les statistiques
- les données marketing

---

## 4. Principe fondamental du système : communication individualisée

Le système devra fonctionner selon un principe de **communication ciblée et personnalisée**.

Chaque étudiant doit recevoir uniquement les informations qui lui correspondent selon plusieurs critères :
- son matricule
- sa filière
- son niveau
- sa classe
- ses cours programmés
- sa situation financière

### Exemple :
Un étudiant en Licence 2 Marketing ne doit pas recevoir les informations destinées aux étudiants en Licence 3 Informatique.

De même :
- les notes doivent être strictement personnelles
- les notifications de paiement doivent être individuelles
- les programmes doivent être liés à la classe spécifique de l'étudiant

---

## 5. Fonctionnalités détaillées de l'application mobile

### 5.1 Module d'authentification et gestion du profil étudiant
Chaque étudiant devra disposer d'un compte personnel sécurisé.

Les informations associées au compte seront :
- Nom
- Prénom
- Matricule étudiant
- Filière
- Niveau
- Classe
- Numéro de téléphone
- Email
- **Lycée de provenance**
- **Ville d'origine**

Ces données permettront de personnaliser l'expérience utilisateur.

### 5.2 Tableau de bord étudiant
Lorsqu'un étudiant ouvre l'application, il doit accéder à un tableau de bord personnalisé affichant :
- les dernières notifications
- son programme du jour
- les nouvelles notes publiées
- les informations administratives importantes
- les notifications financières

### 5.3 Système avancé de notifications intelligentes
Le système devra intégrer un moteur de notifications intelligentes.

Les notifications peuvent être envoyées selon plusieurs niveaux :

#### Notification individuelle
Envoyée à un étudiant spécifique.

Exemple :
- rappel de paiement
- note publiée
- information administrative personnelle

#### Notification par classe
Exemple :
- changement de salle
- modification de programme

#### Notification par filière ou niveau
Exemple :
- conférence
- activité académique
- information pédagogique

#### Notification globale
Information destinée à tous les étudiants.

### 5.4 Module programme académique
Les étudiants doivent pouvoir consulter leur emploi du temps détaillé.

Les informations affichées doivent inclure :
- matière
- enseignant
- date
- heure
- salle
- statut du cours

Lorsqu'un programme est publié ou modifié :
- l'étudiant reçoit une notification immédiate
- l'enseignant reçoit également son programme automatiquement via WhatsApp

### 5.5 Module gestion des notes
Après correction des copies :

Le service académique pourra saisir les notes dans le système.

Les étudiants pourront consulter :
- leurs notes par matière
- leur moyenne
- l'historique des résultats

**Chaque étudiant ne doit pouvoir voir que ses propres notes.**

### 5.6 Module annonces et informations administratives
Ce module permettra à l'administration de diffuser :
- les annonces officielles
- les informations importantes
- les événements académiques
- les activités de l'établissement

### 5.7 Module sondages et enquêtes
Le service communication doit pouvoir lancer des sondages auprès des étudiants.

Exemples :
- satisfaction des étudiants
- participation à un événement
- évaluation d'un service

Les résultats pourront être analysés dans la plateforme administrative.

### 5.8 Module situation financière
Les étudiants pourront consulter leur situation financière.

Les informations disponibles seront :
- frais de scolarité total
- montant payé
- montant restant
- échéances

Le système devra envoyer des **notifications automatiques de rappel de paiement**.

---

## 6. Fonctionnalités de la plateforme administrative

### 6.1 Module Service Communication et Accueil
Fonctionnalités :
- publier des informations
- envoyer des notifications ciblées
- créer des sondages
- analyser les données des étudiants
- consulter les statistiques

Ce module permettra également d'exploiter les données suivantes :
- **lycée de provenance**
- **ville d'origine**
- **filière choisie**

Ces données permettront d'améliorer les stratégies de recrutement étudiant.

### 6.2 Module Service Académique
Fonctionnalités principales :

#### Gestion des programmes
- création des emplois du temps
- modification des programmes
- publication des programmes

#### Gestion des notes
- saisie des notes
- modification des notes
- validation des résultats

#### Gestion des imprévus
Le service académique pourra envoyer rapidement des notifications concernant :
- annulation de cours
- changement de salle
- modification d'horaire

### 6.3 Module Service Comptabilité
Fonctionnalités :
- gestion des paiements
- consultation des dossiers étudiants
- notification des paiements
- envoi de rappels

---

## 7. Fonctionnalités modernes

Afin de rendre la solution plus performante et moderne, certaines fonctionnalités sont fortement recommandées.

### Carte étudiante numérique
Chaque étudiant pourra disposer d'une carte étudiante digitale dans l'application.

### Historique académique
Les étudiants pourront consulter :
- leurs résultats
- leur évolution académique

### Statistiques pour l'administration
La plateforme devra permettre de générer des statistiques :
- nombre d'étudiants par filière
- origine géographique
- taux de paiement
- participation aux sondages

### Messagerie interne
Possibilité d'envoyer des messages directs entre :
- administration ↔ étudiants

---

## 8. Sécurité et protection des données

Le système devra garantir :
- la confidentialité des données
- l'accès sécurisé aux comptes
- la protection des notes et données financières

---

## RÉSUMÉ DES MODULES DEMANDÉS

### ✅ MODULES OBLIGATOIRES

#### Application Mobile Étudiante
1. ✅ Authentification et profil (avec lycée provenance + ville origine)
2. ✅ Tableau de bord personnalisé
3. ✅ Notifications intelligentes (individuelle, classe, filière, globale)
4. ✅ Programme académique (emploi du temps)
5. ✅ Consultation des notes
6. ✅ Annonces et informations administratives
7. ✅ Sondages et enquêtes
8. ✅ Situation financière (frais, paiements, rappels)

#### Plateforme Administrative
1. ✅ Service Communication et Accueil
   - Publications
   - Notifications ciblées
   - Sondages
   - Statistiques marketing (lycée, ville, filière)

2. ✅ Service Académique
   - Gestion emplois du temps
   - Gestion notes
   - Notifications imprévus

3. ✅ Service Comptabilité
   - Gestion paiements
   - Rappels automatiques
   - Consultation dossiers

#### Fonctionnalités Modernes
1. 📋 Carte étudiante numérique
2. 📋 Historique académique complet
3. 📋 Statistiques avancées
4. 📋 Messagerie interne

### ❌ MODULES NON MENTIONNÉS (à supprimer)
- Bureau Exécutif
- Objets perdus
- Événements
- Réclamations (non explicitement demandé)

---

**Date de livraison attendue : CE SOIR**
