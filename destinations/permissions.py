from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admins can do anything.
    Others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class IsAgentOrAdminOrReadOnly(permissions.BasePermission):
    """
    Agents can create and edit their own Destinations & Packages.
    Admins can do anything.
    Users can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['agent', 'admin']

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Admin can edit any object
        if request.user.role == 'admin':
            return True
        # Agents can edit their own objects
        return obj.created_by == request.user
