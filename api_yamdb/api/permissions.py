from rest_framework.permissions import BasePermission

class AdminModeratorAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.user.is_authenticated:
            if request.user == obj.author or request.user.role in ['admin', 'moderator']:
                return True
        return False
