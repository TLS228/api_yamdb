from rest_framework.permissions import (
    BasePermission, IsAdminUser, SAFE_METHODS
)


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
            or request.user.role in (
                'admin', 'moderator'
            ) or request.user.is_staff
        )


class IsAdmin(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == 'admin'
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or (
                request.user.is_authenticated and request.user.role == 'admin'
            )
        )
