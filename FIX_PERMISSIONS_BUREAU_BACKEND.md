# 🔧 Fix Permissions Bureau Exécutif (Backend)

**Date**: 28 février 2026  
**Problème**: Erreurs 403/500 pour le bureau exécutif sur plusieurs endpoints

---

## ❌ Erreurs Identifiées

### 1. Erreur 403 (Forbidden)

```
GET /api/dashboard/bureau/ → 403
error: Accès réservé au Bureau Exécutif

GET /api/presences/ → 403
Vous n'avez pas la permission d'effectuer cette action.

GET /api/matieres/ → 403
Vous n'avez pas la permission d'effectuer cette action.
```

### 2. Erreur 500 (Internal Server Error)

```
GET /api/demandes-administratives/ → 500
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

---

## 🔍 Analyse du Problème

### Cause Probable

Le backend vérifie les permissions mais:
1. Le rôle "bureau" ou "bureau_executif" n'est pas reconnu
2. Les permissions ne sont pas configurées pour ce rôle
3. Certains endpoints n'existent pas ou retournent du HTML au lieu de JSON

---

## ✅ Solutions à Appliquer sur PythonAnywhere

### 1. Vérifier le Rôle dans la Base de Données

```bash
cd ~/school/backend
python manage.py shell
```

```python
from api.models import Utilisateur

# Vérifier le compte bureau
bureau = Utilisateur.objects.filter(email='bureau@uan.bf').first()
print(f"Email: {bureau.email}")
print(f"Rôle: {bureau.role}")
print(f"Est actif: {bureau.is_active}")

# Le rôle doit être 'bureau_executif' ou 'bureau'
# Si ce n'est pas le cas, corriger:
if bureau.role not in ['bureau', 'bureau_executif']:
    bureau.role = 'bureau_executif'
    bureau.save()
    print("✅ Rôle corrigé")
```

### 2. Vérifier les Permissions dans `permissions.py`

Fichier: `backend/api/permissions.py`

```python
from rest_framework import permissions

class IsBureauExecutif(permissions.BasePermission):
    """
    Permission pour le Bureau Exécutif
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['bureau', 'bureau_executif']
        )

class IsBureauOrAdmin(permissions.BasePermission):
    """
    Permission pour Bureau Exécutif ou Admin
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['bureau', 'bureau_executif', 'admin', 'superadmin']
        )
```

### 3. Mettre à Jour les Vues

Fichier: `backend/api/views.py`

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBureauExecutif, IsBureauOrAdmin

# Dashboard Bureau
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsBureauExecutif])
def dashboard_bureau(request):
    """Dashboard pour le Bureau Exécutif"""
    try:
        # Statistiques
        total_etudiants = Etudiant.objects.count()
        total_enseignants = Enseignant.objects.count()
        total_matieres = Matiere.objects.count()
        
        # Paiements récents
        paiements_recents = Paiement.objects.select_related(
            'etudiant', 'etudiant__utilisateur'
        ).order_by('-date_paiement')[:5]
        
        # Demandes en attente
        demandes_attente = DemandeAdministrative.objects.filter(
            statut='en_attente'
        ).count()
        
        return Response({
            'statistiques': {
                'total_etudiants': total_etudiants,
                'total_enseignants': total_enseignants,
                'total_matieres': total_matieres,
                'demandes_attente': demandes_attente,
            },
            'paiements_recents': PaiementSerializer(paiements_recents, many=True).data,
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Présences - Accessible au Bureau
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsBureauOrAdmin])
def liste_presences(request):
    """Liste des présences - accessible au bureau"""
    try:
        presences = Presence.objects.select_related(
            'etudiant', 'matiere', 'enseignant'
        ).order_by('-date')
        
        serializer = PresenceSerializer(presences, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Matières - Accessible au Bureau
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Tous les utilisateurs authentifiés
def liste_matieres(request):
    """Liste des matières"""
    try:
        matieres = Matiere.objects.all()
        serializer = MatiereSerializer(matieres, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

### 4. Vérifier les URLs

Fichier: `backend/api/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard Bureau
    path('dashboard/bureau/', views.dashboard_bureau, name='dashboard-bureau'),
    
    # Présences
    path('presences/', views.liste_presences, name='liste-presences'),
    
    # Matières
    path('matieres/', views.liste_matieres, name='liste-matieres'),
    
    # Demandes administratives
    path('demandes-administratives/', views.liste_demandes_administratives, name='liste-demandes'),
]
```

### 5. Créer les Vues Manquantes

Si certaines vues n'existent pas, les créer:

```python
# Demandes Administratives
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def liste_demandes_administratives(request):
    """Liste des demandes administratives"""
    if request.method == 'GET':
        try:
            # Bureau peut voir toutes les demandes
            if request.user.role in ['bureau', 'bureau_executif', 'admin', 'superadmin']:
                demandes = DemandeAdministrative.objects.all()
            else:
                # Étudiant ne voit que ses demandes
                demandes = DemandeAdministrative.objects.filter(
                    etudiant__utilisateur=request.user
                )
            
            demandes = demandes.select_related(
                'etudiant', 'etudiant__utilisateur'
            ).order_by('-date_demande')
            
            serializer = DemandeAdministrativeSerializer(demandes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'POST':
        # Créer une nouvelle demande
        serializer = DemandeAdministrativeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

---

## 📝 Commandes à Exécuter sur PythonAnywhere

### 1. Se Connecter

```bash
ssh wendlasida@ssh.pythonanywhere.com
```

### 2. Aller dans le Projet

```bash
cd ~/school/backend
source ~/.virtualenvs/myenv/bin/activate
```

### 3. Vérifier le Rôle Bureau

```bash
python manage.py shell
```

```python
from api.models import Utilisateur

bureau = Utilisateur.objects.filter(email='bureau@uan.bf').first()
print(f"Rôle actuel: {bureau.role}")

# Corriger si nécessaire
if bureau.role not in ['bureau', 'bureau_executif']:
    bureau.role = 'bureau_executif'
    bureau.save()
    print("✅ Rôle corrigé en 'bureau_executif'")

exit()
```

### 4. Mettre à Jour le Code

```bash
# Récupérer les dernières modifications
git pull origin main

# Appliquer les migrations si nécessaire
python manage.py makemigrations
python manage.py migrate
```

### 5. Recharger l'Application

1. Aller sur https://www.pythonanywhere.com/user/Wendlasida/
2. Cliquer sur l'onglet "Web"
3. Cliquer sur "Reload wendlasida.pythonanywhere.com"

---

## 🧪 Test

### 1. Tester l'Authentification

```bash
curl -X POST https://wendlasida.pythonanywhere.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"bureau@uan.bf","password":"bureau123"}'
```

Devrait retourner un token.

### 2. Tester le Dashboard Bureau

```bash
curl -X GET https://wendlasida.pythonanywhere.com/api/dashboard/bureau/ \
  -H "Authorization: Bearer <TOKEN>"
```

Devrait retourner les statistiques.

### 3. Tester les Présences

```bash
curl -X GET https://wendlasida.pythonanywhere.com/api/presences/ \
  -H "Authorization: Bearer <TOKEN>"
```

Devrait retourner la liste des présences.

---

## 🎯 Résultat Attendu

Après ces corrections:
- ✅ Le bureau exécutif peut accéder à son dashboard
- ✅ Les présences sont accessibles
- ✅ Les matières sont accessibles
- ✅ Les demandes administratives fonctionnent
- ✅ Pas d'erreur 403 ou 500

---

## ⚠️ Important

### Rôles Valides

Le backend doit reconnaître ces rôles:
- `superadmin`
- `admin`
- `enseignant`
- `etudiant`
- `bureau_executif` ou `bureau`

### Permissions par Rôle

| Endpoint | SuperAdmin | Admin | Bureau | Enseignant | Étudiant |
|----------|------------|-------|--------|------------|----------|
| Dashboard Bureau | ✅ | ✅ | ✅ | ❌ | ❌ |
| Présences | ✅ | ✅ | ✅ | ✅ | ❌ |
| Matières | ✅ | ✅ | ✅ | ✅ | ✅ |
| Demandes Admin | ✅ | ✅ | ✅ | ❌ | ✅ (ses demandes) |

---

## 📦 Fichiers à Modifier sur PythonAnywhere

1. **backend/api/permissions.py**
   - Ajouter `IsBureauExecutif`
   - Ajouter `IsBureauOrAdmin`

2. **backend/api/views.py**
   - Ajouter `dashboard_bureau`
   - Mettre à jour permissions des vues existantes
   - Ajouter vues manquantes

3. **backend/api/urls.py**
   - Ajouter routes manquantes

4. **Base de données**
   - Vérifier/corriger le rôle du compte bureau

---

## 🔄 Après les Modifications

```bash
# Sur PythonAnywhere
cd ~/school/backend
git pull origin main
python manage.py migrate
```

Puis recharger l'application web.

---

**Ces corrections permettront au bureau exécutif d'accéder à toutes les fonctionnalités!** 🔧✨
