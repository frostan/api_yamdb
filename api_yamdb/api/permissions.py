from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminPermission(BasePermission):
    """Доступ админу или суперпользователю."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff
            or request.user.is_superuser
        )


class ModeratorPermission(BasePermission):
    """Доступ модеру, остальным чтение."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.is_staff


class IsAuthor(BasePermission):
    """Доступ автору остальным чтение."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
