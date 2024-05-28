from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class AdminPermission(BasePermission):
    """Доступ админу или суперпользователю."""
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


class CustomPermission(ReadOnlyAnonymousUser):
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
