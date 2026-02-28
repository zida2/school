# 📊 Plan: Historique des Notes et Présences

## 🎯 Objectifs

1. **Historique des modifications de notes** - Tracer qui a modifié quoi et quand
2. **Historique des présences** - Voir toutes les présences/absences d'un étudiant
3. **Statistiques détaillées** - Taux de présence, évolution des notes, etc.

## 📋 Fonctionnalités à Ajouter

### 1. Historique des Notes

#### Modèle Backend: `HistoriqueNote`
```python
class HistoriqueNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='historique')
    action = models.CharField(max_length=20, choices=[
        ('creation', 'Création'),
        ('modification', 'Modification'),
        ('publication', 'Publication'),
        ('confirmation', 'Confirmation étudiant'),
        ('reclamation', 'Réclamation')
    ])
    note_cc_avant = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    note_cc_apres = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    note_examen_avant = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    note_examen_apres = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    modifie_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True)
```

#### Interface Frontend
- **Onglet "Historique"** dans la page de saisie des notes
- Afficher toutes les modifications avec:
  - Date et heure
  - Qui a modifié
  - Anciennes valeurs → Nouvelles valeurs
  - Action effectuée

### 2. Historique des Présences

#### Utiliser le modèle existant: `Presence`
Le modèle existe déjà avec:
- `etudiant`, `emploi`, `date_cours`
- `present`, `justifie`, `observation`
- `enregistre_par`

#### Interface Frontend
- **Page "Statistiques de présence"** pour chaque étudiant
- Afficher:
  - Calendrier des présences/absences
  - Taux de présence global
  - Taux par matière
  - Liste des absences justifiées/non justifiées
  - Graphique d'évolution

### 3. Dashboard Étudiant - Statistiques

#### Ajouter dans le dashboard étudiant:
- **Carte "Mes Présences"**:
  - Taux de présence global
  - Nombre d'absences justifiées/non justifiées
  - Alerte si trop d'absences
  
- **Carte "Évolution de mes notes"**:
  - Graphique d'évolution des moyennes
  - Comparaison avec la moyenne de classe
  - Matières en difficulté

## 🔧 Implémentation

### Phase 1: Corriger le message "0 note publiée" ✅
- Améliorer le message backend pour être plus clair
- Afficher "Toutes les notes sont déjà publiées" si aucune note en brouillon

### Phase 2: Ajouter le modèle HistoriqueNote
1. Créer le modèle dans `models.py`
2. Créer la migration
3. Modifier les vues pour enregistrer l'historique automatiquement
4. Créer l'endpoint API pour récupérer l'historique

### Phase 3: Interface Historique des Notes
1. Ajouter un bouton "📜 Historique" dans la page de saisie
2. Modal/Page pour afficher l'historique
3. Filtres: Par étudiant, par date, par action

### Phase 4: Statistiques de Présence
1. Endpoint API pour les statistiques de présence
2. Page "Mes Présences" dans le dashboard étudiant
3. Graphiques et visualisations

### Phase 5: Rapports et Exports
1. Export Excel des présences
2. Export PDF des bulletins avec historique
3. Rapports pour l'administration

## 📊 Exemples d'Interface

### Historique des Notes (Modal)
```
📜 Historique des modifications - Diallo Moussa - Algorithmique

┌─────────────────────────────────────────────────────────────┐
│ 15/01/2025 14:30 - Jean OUEDRAOGO                          │
│ Action: Modification                                         │
│ CC: 14.00 → 15.00                                           │
│ Examen: 13.58 → 17.00                                       │
│ Moyenne: 13.85 → 16.20                                      │
├─────────────────────────────────────────────────────────────┤
│ 10/01/2025 10:15 - Jean OUEDRAOGO                          │
│ Action: Publication                                          │
│ Statut: Brouillon → Publié                                  │
├─────────────────────────────────────────────────────────────┤
│ 08/01/2025 16:45 - Jean OUEDRAOGO                          │
│ Action: Création                                             │
│ CC: 14.00, Examen: 13.58                                    │
└─────────────────────────────────────────────────────────────┘
```

### Statistiques de Présence (Dashboard Étudiant)
```
📊 Mes Présences - Semestre 1

Taux de présence global: 85% ✅

Par matière:
┌──────────────────────────┬──────────┬─────────┬──────────┐
│ Matière                  │ Présent  │ Absent  │ Taux     │
├──────────────────────────┼──────────┼─────────┼──────────┤
│ Algorithmique            │ 12/14    │ 2       │ 86%      │
│ Bases de Données         │ 10/12    │ 2       │ 83%      │
│ Mathématiques            │ 14/15    │ 1       │ 93%      │
└──────────────────────────┴──────────┴─────────┴──────────┘

⚠️ Absences non justifiées: 3
✅ Absences justifiées: 2
```

## 🚀 Priorités

### Priorité 1 (Urgent)
1. ✅ Corriger le message "0 note publiée"
2. Ajouter le modèle HistoriqueNote
3. Enregistrer automatiquement l'historique

### Priorité 2 (Important)
1. Interface d'affichage de l'historique des notes
2. Statistiques de présence dans le dashboard étudiant

### Priorité 3 (Nice to have)
1. Graphiques d'évolution
2. Exports Excel/PDF
3. Rapports administratifs

## 📝 Notes Techniques

### Enregistrement Automatique de l'Historique
Utiliser les signaux Django:
```python
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

@receiver(pre_save, sender=Note)
def enregistrer_historique_note(sender, instance, **kwargs):
    if instance.pk:  # Si la note existe déjà (modification)
        ancienne_note = Note.objects.get(pk=instance.pk)
        HistoriqueNote.objects.create(
            note=instance,
            action='modification',
            note_cc_avant=ancienne_note.note_cc,
            note_cc_apres=instance.note_cc,
            # ...
        )
```

### Performance
- Indexer les champs de recherche fréquents
- Paginer l'historique (max 50 entrées par page)
- Cache pour les statistiques

## ✅ Checklist

- [ ] Corriger message "0 note publiée"
- [ ] Créer modèle HistoriqueNote
- [ ] Créer migration
- [ ] Ajouter signaux pour enregistrement auto
- [ ] Créer endpoint API historique
- [ ] Interface frontend historique notes
- [ ] Endpoint API statistiques présence
- [ ] Interface frontend statistiques présence
- [ ] Tests unitaires
- [ ] Documentation

---

**Voulez-vous que je commence par quelle partie?**
