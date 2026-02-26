# INTÉGRATION BACKEND - ÉTAPE 1
## Ajout du ReclamationNoteViewSet et extensions

Date: 26 février 2026

---

## 📝 INSTRUCTIONS D'INTÉGRATION

### 1. Ajouter ReclamationNoteViewSet

**Emplacement**: Après la ligne 663 (après `NotificationViewSet`)

**Code à ajouter**:

```python
# ===== RÉCLAMATION NOTE =====
class ReclamationNoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les réclamations sur les notes
    """
    queryset = ReclamationNote.objects.select_related(
        'note', 'note__etudiant', 'note__matiere', 'note__matiere__enseignant'
    ).all()
    serializer_class = ReclamationNoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        # Étudiant: voir uniquement ses réclamations
        if user.role == 'etudiant':
            try:
                qs = qs.filter(note__etudiant=user.etudiant)
            except:
                qs = qs.none()
        
        # Enseignant: voir les réclamations sur ses matières
        elif user.role == 'professeur':
            try:
                qs = qs.filter(note__matiere__enseignant=user.enseignant)
            except:
                qs = qs.none()
        
        # Admin: voir toutes les réclamations
        elif user.role in ['admin', 'superadmin']:
            pass
        
        else:
            qs = qs.none()
        
        # Filtres
        statut = self.request.query_params.get('statut')
        if statut:
            qs = qs.filter(statut=statut)
        
        return qs.order_by('-date_creation')
    
    def perform_create(self, serializer):
        """Créer une réclamation (étudiant uniquement)"""
        if self.request.user.role != 'etudiant':
            raise permissions.PermissionDenied("Seuls les étudiants peuvent créer des réclamations")
        
        serializer.save()
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def traiter(self, request, pk=None):
        """
        Traiter une réclamation (enseignant ou admin)
        """
        reclamation = self.get_object()
        user = request.user
        
        # Vérifier les permissions
        if user.role == 'professeur':
            try:
                if reclamation.note.matiere.enseignant != user.enseignant:
                    return Response(
                        {'error': 'Vous ne pouvez traiter que les réclamations de vos matières'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except:
                return Response(
                    {'error': 'Enseignant non trouvé'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif user.role not in ['admin', 'superadmin']:
            return Response(
                {'error': 'Non autorisé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Récupérer les données
        statut = request.data.get('statut')  # 'resolue' ou 'rejetee'
        reponse = request.data.get('reponse_enseignant', '')
        corriger_note = request.data.get('corriger_note', False)
        nouvelle_note_cc = request.data.get('nouvelle_note_cc')
        nouvelle_note_examen = request.data.get('nouvelle_note_examen')
        
        if statut not in ['resolue', 'rejetee']:
            return Response(
                {'error': 'Statut invalide. Utilisez "resolue" ou "rejetee"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mettre à jour la réclamation
        reclamation.statut = statut
        reclamation.reponse_enseignant = reponse
        reclamation.date_traitement = timezone.now()
        reclamation.save()
        
        # Si correction de note demandée et acceptée
        if corriger_note and statut == 'resolue':
            note = reclamation.note
            
            if nouvelle_note_cc is not None:
                note.note_cc = float(nouvelle_note_cc)
            
            if nouvelle_note_examen is not None:
                note.note_examen = float(nouvelle_note_examen)
            
            # Recalculer la moyenne
            if note.note_cc is not None and note.note_examen is not None:
                note.moyenne = (note.note_cc + note.note_examen) / 2
            elif note.note_cc is not None:
                note.moyenne = note.note_cc
            elif note.note_examen is not None:
                note.moyenne = note.note_examen
            
            note.save()
            
            return Response({
                'detail': 'Réclamation traitée et note corrigée',
                'reclamation': ReclamationNoteSerializer(reclamation).data,
                'note_corrigee': {
                    'note_cc': note.note_cc,
                    'note_examen': note.note_examen,
                    'moyenne': note.moyenne
                }
            })
        
        return Response({
            'detail': f'Réclamation {statut}',
            'reclamation': ReclamationNoteSerializer(reclamation).data
        })
```

---

### 2. Modifier DemandeAdministrativeViewSet

**Emplacement**: Ligne 1130 - Remplacer la méthode `get_queryset`

**Code à remplacer**:
```python
def get_queryset(self):
    qs = super().get_queryset()
    user = self.request.user
    
    if user.role == 'etudiant':
        try:
            qs = qs.filter(etudiant=user.etudiant)
        except:
            qs = qs.none()
    elif user.role in ['admin', 'superadmin']:
        pass
    else:
        qs = qs.none()
    
    statut = self.request.query_params.get('statut')
    if statut:
        qs = qs.filter(statut=statut)
    
    return qs.order_by('-date_creation')
```

**Par**:
```python
def get_queryset(self):
    qs = super().get_queryset()
    user = self.request.user
    
    # Étudiant: voir uniquement ses demandes
    if user.role == 'etudiant':
        try:
            qs = qs.filter(etudiant=user.etudiant)
        except:
            qs = qs.none()
    
    # Enseignant: voir les demandes qui lui sont adressées
    elif user.role == 'professeur':
        try:
            qs = qs.filter(
                destinataire='professeur',
                professeur=user.enseignant
            )
        except:
            qs = qs.none()
    
    # Admin: voir les demandes administratives
    elif user.role in ['admin', 'superadmin']:
        qs = qs.filter(destinataire='administration')
    
    # Bureau: voir toutes les demandes
    elif user.role == 'bureau_executif':
        pass
    
    else:
        qs = qs.none()
    
    # Filtres
    statut = self.request.query_params.get('statut')
    if statut:
        qs = qs.filter(statut=statut)
    
    return qs.order_by('-date_creation')
```

**Ajouter après la méthode `traiter`** (ligne ~1180):
```python
@action(detail=True, methods=['post'])
def repondre(self, request, pk=None):
    """
    Répondre à une demande
    """
    demande = self.get_object()
    user = request.user
    
    # Vérifier les permissions
    if user.role == 'professeur':
        try:
            if demande.professeur != user.enseignant:
                return Response(
                    {'error': 'Vous ne pouvez répondre qu\'aux demandes qui vous sont adressées'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except:
            return Response(
                {'error': 'Enseignant non trouvé'},
                status=status.HTTP_403_FORBIDDEN
            )
    elif user.role not in ['admin', 'superadmin', 'bureau_executif']:
        return Response(
            {'error': 'Non autorisé'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Récupérer les données
    statut = request.data.get('statut')  # 'en_cours', 'traitee', 'rejetee'
    reponse = request.data.get('reponse', '')
    
    if statut not in ['en_cours', 'traitee', 'rejetee']:
        return Response(
            {'error': 'Statut invalide'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Mettre à jour la demande
    demande.statut = statut
    demande.reponse = reponse
    demande.traite_par = user
    demande.date_traitement = timezone.now()
    demande.save()
    
    return Response({
        'detail': f'Demande {statut}',
        'demande': DemandeAdministrativeSerializer(demande).data
    })
```

---

### 3. Modifier SondageViewSet

**Ajouter après la méthode `resultats`** (ligne ~935):

```python
@action(detail=True, methods=['post'])
def repondre(self, request, pk=None):
    """
    Répondre à un sondage
    """
    sondage = self.get_object()
    user = request.user
    
    # Vérifier que l'utilisateur est étudiant
    if user.role != 'etudiant':
        return Response(
            {'error': 'Seuls les étudiants peuvent répondre aux sondages'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Vérifier que le sondage est actif
    if sondage.statut != 'actif':
        return Response(
            {'error': 'Ce sondage n\'est plus actif'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Vérifier que l'étudiant n'a pas déjà répondu
    try:
        etudiant = user.etudiant
        if ReponseSondage.objects.filter(sondage=sondage, etudiant=etudiant).exists():
            return Response(
                {'error': 'Vous avez déjà répondu à ce sondage'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except:
        return Response(
            {'error': 'Étudiant non trouvé'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Récupérer les réponses
    reponses = request.data.get('reponses', [])
    
    if not reponses:
        return Response(
            {'error': 'Aucune réponse fournie'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Créer les réponses
    reponses_creees = []
    for reponse_data in reponses:
        question_id = reponse_data.get('question_id')
        option_id = reponse_data.get('option_id')
        reponse_texte = reponse_data.get('reponse_texte', '')
        
        try:
            question = sondage.questions.get(id=question_id)
            
            reponse = ReponseSondage.objects.create(
                sondage=sondage,
                question=question,
                etudiant=etudiant,
                option_id=option_id if option_id else None,
                reponse_texte=reponse_texte
            )
            reponses_creees.append(reponse)
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la création de la réponse: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response({
        'detail': 'Réponses enregistrées avec succès',
        'nombre_reponses': len(reponses_creees)
    })
```

---

### 4. Modifier EvaluationViewSet

**Ajouter après la méthode `generer_notes`** (ligne ~800):

```python
@action(detail=True, methods=['post'])
def repondre(self, request, pk=None):
    """
    Répondre à un questionnaire d'évaluation
    """
    evaluation = self.get_object()
    user = request.user
    
    # Vérifier que l'utilisateur est étudiant
    if user.role != 'etudiant':
        return Response(
            {'error': 'Seuls les étudiants peuvent répondre aux évaluations'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Vérifier que l'évaluation est active
    if not evaluation.actif:
        return Response(
            {'error': 'Cette évaluation n\'est plus active'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Vérifier que l'étudiant n'a pas déjà répondu
    try:
        etudiant = user.etudiant
        if NoteEvaluation.objects.filter(evaluation=evaluation, etudiant=etudiant).exists():
            return Response(
                {'error': 'Vous avez déjà répondu à cette évaluation'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except:
        return Response(
            {'error': 'Étudiant non trouvé'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Récupérer les réponses
    reponses = request.data.get('reponses', {})
    commentaire = request.data.get('commentaire', '')
    
    if not reponses:
        return Response(
            {'error': 'Aucune réponse fournie'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Créer la note d'évaluation
    note_eval = NoteEvaluation.objects.create(
        evaluation=evaluation,
        etudiant=etudiant,
        reponses=reponses,
        commentaire=commentaire
    )
    
    return Response({
        'detail': 'Évaluation soumise avec succès',
        'evaluation': NoteEvaluationSerializer(note_eval).data
    })

@action(detail=True, methods=['get'])
def resultats(self, request, pk=None):
    """
    Obtenir les résultats d'une évaluation (anonymes)
    """
    evaluation = self.get_object()
    user = request.user
    
    # Seuls admin et l'enseignant concerné peuvent voir les résultats
    if user.role == 'professeur':
        try:
            if evaluation.matiere and evaluation.matiere.enseignant != user.enseignant:
                return Response(
                    {'error': 'Non autorisé'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except:
            return Response(
                {'error': 'Enseignant non trouvé'},
                status=status.HTTP_403_FORBIDDEN
            )
    elif user.role not in ['admin', 'superadmin']:
        return Response(
            {'error': 'Non autorisé'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Calculer les statistiques (anonymes)
    notes = NoteEvaluation.objects.filter(evaluation=evaluation)
    total_reponses = notes.count()
    
    # Agréger les réponses
    resultats = {
        'total_participants': total_reponses,
        'questions': []
    }
    
    # Extraire les questions du premier questionnaire
    if total_reponses > 0:
        premiere_note = notes.first()
        if premiere_note and premiere_note.reponses:
            for question_key, _ in premiere_note.reponses.items():
                # Collecter toutes les réponses pour cette question
                reponses_question = []
                for note in notes:
                    if note.reponses and question_key in note.reponses:
                        reponses_question.append(note.reponses[question_key])
                
                # Calculer la moyenne si numérique
                if reponses_question and isinstance(reponses_question[0], (int, float)):
                    moyenne = sum(reponses_question) / len(reponses_question)
                    resultats['questions'].append({
                        'question': question_key,
                        'type': 'numerique',
                        'moyenne': round(moyenne, 2),
                        'min': min(reponses_question),
                        'max': max(reponses_question)
                    })
                else:
                    resultats['questions'].append({
                        'question': question_key,
                        'type': 'texte',
                        'reponses': reponses_question
                    })
    
    # Commentaires (anonymes)
    commentaires = notes.exclude(commentaire='').values_list('commentaire', flat=True)
    resultats['commentaires'] = list(commentaires)
    
    return Response(resultats)
```

---

### 5. Modifier ObjetPerduViewSet

**Ajouter après la méthode `marquer_recupere`** (ligne ~1210):

```python
@action(detail=True, methods=['patch'])
def changer_statut(self, request, pk=None):
    """
    Changer le statut d'un objet perdu
    """
    objet = self.get_object()
    user = request.user
    
    # Seuls admin et bureau peuvent changer le statut
    if user.role not in ['admin', 'superadmin', 'bureau_executif']:
        return Response(
            {'error': 'Non autorisé'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    nouveau_statut = request.data.get('statut')
    
    if nouveau_statut not in ['actif', 'recupere', 'archive']:
        return Response(
            {'error': 'Statut invalide'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    objet.statut = nouveau_statut
    objet.save()
    
    return Response({
        'detail': f'Statut changé en {nouveau_statut}',
        'objet': ObjetPerduSerializer(objet).data
    })
```

---

### 6. Ajouter la route dans urls.py

**Fichier**: `backend/api/urls.py`

**Ajouter dans la liste des routes**:
```python
router.register(r'reclamations', views.ReclamationNoteViewSet, basename='reclamation')
```

---

## ✅ CHECKLIST

- [ ] Ajouter ReclamationNoteViewSet dans views.py
- [ ] Modifier DemandeAdministrativeViewSet.get_queryset()
- [ ] Ajouter DemandeAdministrativeViewSet.repondre()
- [ ] Ajouter SondageViewSet.repondre()
- [ ] Ajouter EvaluationViewSet.repondre()
- [ ] Ajouter EvaluationViewSet.resultats()
- [ ] Ajouter ObjetPerduViewSet.changer_statut()
- [ ] Ajouter route dans urls.py
- [ ] Redémarrer le serveur Django
- [ ] Tester les endpoints

---

## 🧪 TESTS

```bash
# Redémarrer le serveur
cd backend
python manage.py runserver

# Tester les endpoints
curl -X GET http://127.0.0.1:8000/api/reclamations/ \
  -H "Authorization: Bearer YOUR_TOKEN"

curl -X GET http://127.0.0.1:8000/api/demandes-administratives/ \
  -H "Authorization: Bearer YOUR_TOKEN"

curl -X GET http://127.0.0.1:8000/api/sondages/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

Date: 26 février 2026
