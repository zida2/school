# Migration pour les réclamations de notes

## Commandes à exécuter

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## Modèle ajouté

- **ReclamationNote**: Permet aux étudiants de signaler des problèmes sur leurs notes
  - Champs: note, etudiant, type_probleme, description, note_attendue, statut, reponse_enseignant
  - Statuts: en_attente, en_cours, resolu, rejete

## API Endpoints ajoutés

- `GET /api/reclamations/` - Liste des réclamations (filtrée par rôle)
- `POST /api/reclamations/` - Créer une réclamation (étudiants uniquement)
- `GET /api/reclamations/{id}/` - Détail d'une réclamation
- `PUT /api/reclamations/{id}/` - Modifier/traiter une réclamation (enseignants/admins)
- `DELETE /api/reclamations/{id}/` - Supprimer une réclamation (étudiants, si en_attente)

## Fonctionnalités

1. **Étudiant**: Peut signaler un problème sur une note avec description
2. **Enseignant**: Reçoit les réclamations et peut y répondre
3. **Admin**: Peut voir toutes les réclamations

## Frontend

- Bouton "⚠️ Signaler" sur chaque note dans dashboard-etudiant.html
- Modal avec formulaire de réclamation
- Types de problèmes prédéfinis
