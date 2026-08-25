from rest_framework.permissions import BasePermission
from users.models import User
from users.permissions import HasRole

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

        if request.user.role == User.Role.ADMIN:
            return True

        return obj.created_by == request.user

class CanManageProjects(HasRole):
    allowed_roles = [
        User.Role.ADMIN,
        User.Role.QA_ENGINEER
    ]

class CanExecuteTests(HasRole):
    allowed_roles =[
        User.Role.QA_ENGINEER,
        User.Role.ADMIN,
        User.Role.DEVELOPER,
    ]

class CanManageTestCases(HasRole):
    allowed_roles = [
        User.Role.ADMIN,
        User.Role.QA_ENGINEER,
    ]

class CanManageTestSuite(HasRole):
    allowed_roles = [
        User.Role.ADMIN,
        User.Role.QA_ENGINEER,
    ]