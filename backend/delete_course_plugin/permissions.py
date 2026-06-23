from rest_framework.permissions import BasePermission


class IsSuperUserOnly(BasePermission):
    """Allow access only for authenticated Django superusers."""

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and user.is_superuser)
