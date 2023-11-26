from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    """Проверка на пользователя"""
    message = 'Это не ваш профиль'

    def has_object_permission(self, request, view, obj):
        return obj == request.user
