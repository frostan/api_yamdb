from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class AdminPermission(BasePermission):
    """Доступ админу или суперпользователю."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff
            or request.user.is_admin
            or request.user.is_superuser
        )


class ModeratorPermission(BasePermission):
    """Доступ модератору."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.is_staff


class Author(BasePermission):
    """Доступ автору."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class ReadOnlyAnonymousUser(BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
