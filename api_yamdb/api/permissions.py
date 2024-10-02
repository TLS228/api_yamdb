from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class AdminModeratorAuthor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin
        )


# class IsReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.method in SAFE_METHODS or request.user.is_authenticated
#         )

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role == 'admin')
        )
