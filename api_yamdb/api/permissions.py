from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                or request.user.is_staff
                or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class ModeratorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class MyPermission(BasePermission):
    """Класс кастомных пермишенов."""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                or request.user.is_staff
                or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.method in SAFE_METHODS
        return obj.author == request.user or (
            request.user.role == 'moderator'
            or request.user.role == 'admin'
        )
