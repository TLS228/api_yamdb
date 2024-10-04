from rest_framework.permissions import (
    BasePermission, IsAdminUser, SAFE_METHODS
)

from reviews.constants import ADMIN, MODERATOR


class IsAdminModeratorAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
            or request.user.role in (
                ADMIN, MODERATOR
            )
        )


class IsAdmin(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == ADMIN
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or (
                request.user.is_authenticated and request.user.role == ADMIN
            )
        )