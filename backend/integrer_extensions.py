"""
Script pour intégrer les extensions dans views.py
"""

print("""
=================================================================
INSTRUCTIONS POUR INTÉGRER LES EXTENSIONS
=================================================================

1. AJOUTER LE VIEWSET RÉCLAMATION NOTE
   Ajouter après la ligne 640 (après NotificationViewSet):

```python
# ===== RÉCLAMATION NOTE =====
class ReclamationNoteViewSet(viewsets.ModelViewSet):
    queryset = ReclamationNote.objects.select_related(
        'note', 'note__etudiant', 'note__matiere', 'note__matiere__enseignant'
    ).all()
    serializer_class = ReclamationNoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        if user.role == 'etudiant':
            try:
                qs = qs.filter(note__etudiant=user.etudiant)
            except:
                qs = qs.none()
        elif user.role == 'professeur':
            try:
                qs = qs.filter(note__matiere__enseignant=user.enseignant)
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
    
    def perform_create(self, serializer):
        if self.request.user.role != 'etudiant':
            raise permissions.PermissionDenied("Seuls les étudiants peuvent créer des réclamations")
        serializer.save()
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def traiter(self, request, pk=None):
        reclamation = self.get_object()
        user = request.user
        
        if user.role == 'professeur':
            try:
                if reclamation.note.matiere.enseignant != user.enseignant:
                    return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
            except:
                return Response({'error': 'Enseignant non trouvé'}, status=status.HTTP_403_FORBIDDEN)
        elif user.role not in ['admin', 'superadmin']:
            return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
        
        statut = request.data.get('statut')
        reponse = request.data.get('reponse_enseignant', '')
        corriger_note = request.data.get('corriger_note', False)
        nouvelle_note_cc = request.data.get('nouvelle_note_cc')
        nouvelle_note_examen = request.data.get('nouvelle_note_examen')
        
        if statut not in ['resolue', 'rejetee']:
            return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)
        
        reclamation.statut = statut
        reclamation.reponse_enseignant = reponse
        reclamation.date_traitement = timezone.now()
        reclamation.save()
        
        if corriger_note and statut == 'resolue':
            note = reclamation.note
            if nouvelle_note_cc is not None:
                note.note_cc = float(nouvelle_note_cc)
            if nouvelle_note_examen is not None:
                note.note_examen = float(nouvelle_note_examen)
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

2. MODIFIER DemandeAdministrativeViewSet (ligne 1130)
   Remplacer la méthode get_queryset par:

```python
def get_queryset(self):
    qs = super().get_queryset()
    user = self.request.user
    
    if user.role == 'etudiant':
        try:
            qs = qs.filter(etudiant=user.etudiant)
        except:
            qs = qs.none()
    elif user.role == 'professeur':
        try:
            qs = qs.filter(destinataire='professeur', professeur=user.enseignant)
        except:
            qs = qs.none()
    elif user.role in ['admin', 'superadmin']:
        qs = qs.filter(destinataire='administration')
    elif user.role == 'bureau_executif':
        pass
    else:
        qs = qs.none()
    
    statut = self.request.query_params.get('statut')
    if statut:
        qs = qs.filter(statut=statut)
    
    return qs.order_by('-date_creation')
```

   Ajouter la méthode repondre après traiter:

```python
@action(detail=True, methods=['post'])
def repondre(self, request, pk=None):
    demande = self.get_object()
    user = request.user
    
    if user.role == 'professeur':
        try:
            if demande.professeur != user.enseignant:
                return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({'error': 'Enseignant non trouvé'}, status=status.HTTP_403_FORBIDDEN)
    elif user.role not in ['admin', 'superadmin', 'bureau_executif']:
        return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    statut = request.data.get('statut')
    reponse = request.data.get('reponse', '')
    
    if statut not in ['en_cours', 'traitee', 'rejetee']:
        return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)
    
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

3. MODIFIER SondageViewSet (ligne 886)
   Ajouter ces méthodes:

```python
@action(detail=True, methods=['post'])
def repondre(self, request, pk=None):
    sondage = self.get_object()
    user = request.user
    
    if user.role != 'etudiant':
        return Response({'error': 'Seuls les étudiants peuvent répondre'}, status=status.HTTP_403_FORBIDDEN)
    
    if sondage.statut != 'actif':
        return Response({'error': 'Sondage non actif'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        etudiant = user.etudiant
        if ReponseSondage.objects.filter(sondage=sondage, etudiant=etudiant).exists():
            return Response({'error': 'Déjà répondu'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'error': 'Étudiant non trouvé'}, status=status.HTTP_403_FORBIDDEN)
    
    reponses = request.data.get('reponses', [])
    if not reponses:
        return Response({'error': 'Aucune réponse'}, status=status.HTTP_400_BAD_REQUEST)
    
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
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'detail': 'Réponses enregistrées',
        'nombre_reponses': len(reponses_creees)
    })

@action(detail=True, methods=['get'])
def resultats(self, request, pk=None):
    sondage = self.get_object()
    user = request.user
    
    if user.role not in ['admin', 'superadmin', 'bureau_executif']:
        if sondage.createur != user:
            return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    resultats = []
    for question in sondage.questions.all():
        stats = {
            'question_id': question.id,
            'question_texte': question.texte,
            'type_question': question.type_question,
            'total_reponses': ReponseSondage.objects.filter(question=question).count(),
            'options': []
        }
        
        if question.type_question in ['choix_unique', 'choix_multiple']:
            for option in question.options.all():
                count = ReponseSondage.objects.filter(question=question, option=option).count()
                stats['options'].append({
                    'option_id': option.id,
                    'texte': option.texte,
                    'nombre_reponses': count,
                    'pourcentage': (count / stats['total_reponses'] * 100) if stats['total_reponses'] > 0 else 0
                })
        elif question.type_question == 'texte':
            reponses_texte = ReponseSondage.objects.filter(question=question).values_list('reponse_texte', flat=True)
            stats['reponses_texte'] = list(reponses_texte)
        
        resultats.append(stats)
    
    return Response({
        'sondage': SondageSerializer(sondage).data,
        'total_participants': ReponseSondage.objects.filter(sondage=sondage).values('etudiant').distinct().count(),
        'resultats': resultats
    })
```

4. MODIFIER EvaluationViewSet (ligne 737)
   Ajouter ces méthodes:

```python
@action(detail=True, methods=['post'])
def repondre(self, request, pk=None):
    evaluation = self.get_object()
    user = request.user
    
    if user.role != 'etudiant':
        return Response({'error': 'Seuls les étudiants peuvent répondre'}, status=status.HTTP_403_FORBIDDEN)
    
    if not evaluation.actif:
        return Response({'error': 'Évaluation non active'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        etudiant = user.etudiant
        if NoteEvaluation.objects.filter(evaluation=evaluation, etudiant=etudiant).exists():
            return Response({'error': 'Déjà répondu'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'error': 'Étudiant non trouvé'}, status=status.HTTP_403_FORBIDDEN)
    
    reponses = request.data.get('reponses', {})
    commentaire = request.data.get('commentaire', '')
    
    if not reponses:
        return Response({'error': 'Aucune réponse'}, status=status.HTTP_400_BAD_REQUEST)
    
    note_eval = NoteEvaluation.objects.create(
        evaluation=evaluation,
        etudiant=etudiant,
        reponses=reponses,
        commentaire=commentaire
    )
    
    return Response({
        'detail': 'Évaluation soumise',
        'evaluation': NoteEvaluationSerializer(note_eval).data
    })

@action(detail=True, methods=['get'])
def resultats(self, request, pk=None):
    evaluation = self.get_object()
    user = request.user
    
    if user.role == 'professeur':
        try:
            if evaluation.matiere and evaluation.matiere.enseignant != user.enseignant:
                return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({'error': 'Enseignant non trouvé'}, status=status.HTTP_403_FORBIDDEN)
    elif user.role not in ['admin', 'superadmin']:
        return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    notes = NoteEvaluation.objects.filter(evaluation=evaluation)
    total_reponses = notes.count()
    
    resultats = {'total_participants': total_reponses, 'questions': []}
    
    if total_reponses > 0:
        premiere_note = notes.first()
        if premiere_note and premiere_note.reponses:
            for question_key, _ in premiere_note.reponses.items():
                reponses_question = []
                for note in notes:
                    if note.reponses and question_key in note.reponses:
                        reponses_question.append(note.reponses[question_key])
                
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
    
    commentaires = notes.exclude(commentaire='').values_list('commentaire', flat=True)
    resultats['commentaires'] = list(commentaires)
    
    return Response(resultats)
```

5. MODIFIER ObjetPerduViewSet (ligne 1186)
   Ajouter cette méthode:

```python
@action(detail=True, methods=['patch'])
def changer_statut(self, request, pk=None):
    objet = self.get_object()
    user = request.user
    
    if user.role not in ['admin', 'superadmin', 'bureau_executif']:
        return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    
    nouveau_statut = request.data.get('statut')
    
    if nouveau_statut not in ['actif', 'recupere', 'archive']:
        return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)
    
    objet.statut = nouveau_statut
    objet.save()
    
    return Response({
        'detail': f'Statut changé en {nouveau_statut}',
        'objet': ObjetPerduSerializer(objet).data
    })
```

6. AJOUTER DANS urls.py
   Ajouter cette ligne dans le router:

```python
router.register(r'reclamations', views.ReclamationNoteViewSet, basename='reclamation')
```

=================================================================
FICHIERS À MODIFIER:
- backend/api/views.py (ajouter les méthodes ci-dessus)
- backend/api/urls.py (ajouter la route reclamations)
=================================================================
""")
