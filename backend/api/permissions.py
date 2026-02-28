from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """Accès réservé aux Super Administrateurs uniquement."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'superadmin'


class IsAdminOrSuperAdmin(BasePermission):
    """Accès pour les Admins et Super Admins."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('admin', 'superadmin')
        )


class IsEnseignant(BasePermission):
    """Accès pour les Enseignants (et Admins/SuperAdmins)."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('enseignant', 'professeur', 'admin', 'superadmin')
        )


class IsEtudiant(BasePermission):
    """Accès pour les Étudiants uniquement (ou admin)."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('etudiant', 'admin', 'superadmin')
        )


class IsBureauExecutif(BasePermission):
    """Accès pour le Bureau Exécutif."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('bureau', 'bureau_executif', 'admin', 'superadmin')
        )


class IsBureauOrAdmin(BasePermission):
    """Accès pour Bureau Exécutif, Admin et SuperAdmin."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('bureau', 'bureau_executif', 'admin', 'superadmin')
        )
