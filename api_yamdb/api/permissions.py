from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminPermission(BasePermission):
    """Доступ админу или суперпользователю."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class CommentReviewPermission(BasePermission):
    """Класс кастомных пермишенов."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin
