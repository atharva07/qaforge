from rest_framework.permissions import BasePermission
from users.models import User

class ProjectPermission(BasePermission):

    # Here there are two levels of permission checks
    # 1. If the Request has permission
    # 2. If this involves specific object
    # The authenticated user is allowed to access this Project only if they created it
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return obj.created_by == request.user

class IsQAEngineer(BasePermission):
    """
    Allows access only to QA Engineers
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.QA_ENGINEER
        )