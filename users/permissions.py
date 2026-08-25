from rest_framework.permissions import BasePermission
from .models import User

class IsAdmin(BasePermission):
    """
    Allows access only to QAForge administration    
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.role == User.Role.ADMIN
        )   

class HasRole(BasePermission):
    """
    Generic Role Based Permissions
    """

    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in self.allowed_roles
        )