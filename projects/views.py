from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from users.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .permissions import ProjectPermission
from .permissions import CanExecuteTests, CanManageProjects

# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    # queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user

        # If not authenticated, nothing will return
        if not user.is_authenticated:
            return Project.objects.none()

        # Id Admin, it will return all objects
        if user.role == User.Role.ADMIN:
            return Project.objects.all()

        # else it will return based on the membership
        return Project.objects.filter(
            memberships__user=user
        ).distinct()

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated]

        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated]

        elif self.action == "create":
            permission_classes = [CanManageProjects]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [CanManageProjects, ProjectPermission]

        elif self.action == "archive":
            permission_classes = [CanManageProjects, ProjectPermission]

        elif self.action == "execute":
            permission_classes = [CanExecuteTests]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        project = self.get_object()

        return Response({
            "message": f"Project {project.name} archived successfully"
        })

    @action(detail=True, methods=["post"])
    def execute(self, request, pk=None):
        project = self.get_object()

        return Response({
                "message": f"Execution Started for project {project.name}"
            },
            status=202,
        )

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        return Response({
            "id": str(request.user.id),
            "email": request.user.email,
            "is_authenticated": request.user.is_authenticated,
            "is_staff": request.user.is_staff,
            "is_superuser": request.user.is_superuser,
        })

    @action(detail=False, methods=["get"], url_path="manage_test", permission_classes=[CanManageProjects])
    def manage_test(self, request):
        return Response({
            "id": str(request.user.id),
            "email": request.user.email,
            "is_authenticated": request.user.is_authenticated,
            "is_staff": request.user.is_staff,
            "is_superuser": request.user.is_superuser,
        })

    @action(detail=False, methods=["get"], url_path="execute_test", permission_classes=[CanExecuteTests])
    def execute_test(self, request):
        return Response({
            "id": str(request.user.id),
            "email": request.user.email,
            "is_authenticated": request.user.is_authenticated,
            "is_staff": request.user.is_staff,
            "is_superuser": request.user.is_superuser,
        })