from rest_framework import permissions
from .models import UserRoles


class IsSuperUser(permissions.IsAuthenticated):
    """Уровень доступа Суперпользователь
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False


class IsCurator(permissions.BasePermission):
    """Уровень доступа Куратор
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == UserRoles.curator:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.role == UserRoles.curator:
                return True
        return False


class IsAdmin(permissions.BasePermission):
    """Уровень доступа Администратор
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == UserRoles.admin:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.role == UserRoles.admin:
                return True
        return False
