from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project
from .serializers import ProjectSerializer
from users.models import User
from rest_framework import status
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .permissions import ProjectPermission
from .permissions import IsQAEngineer

# Create your views here.
# class ProjectListCreateAPIView(APIView):
#     def get(self, request):
#         projects = Project.objects.all()

#         sreializer = ProjectSerializer(
#             projects,
#             many=True
#         )

#         return Response(sreializer.data)

#     def post(self, request):
#         serializer = ProjectSerializer(
#             data=request.data,
#         )

#         if serializer.is_valid():
#             user = User.objects.first()
#             project = serializer.save(
#                 created_by = user,
#             )

#             return Response(
#                 ProjectSerializer(project).data,
#                 status=201
#             )

#         return Response(
#             serializer.errors,
#             status=400,
#         )

# class ProjectDetailAPIView(APIView):
#     def get(self, request, project_id):
#         try:
#             project = Project.objects.get(id=project_id)
#         except Project.DoesNotExist:
#             return Response(
#                 {
#                     "detail": "Project not found"
#                 },
#                 status = status.HTTP_200_OK,
#             )

#         serializer = ProjectSerializer(project)

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK,
#         )

#     def put(self, request, project_id):
#         try:
#             project = Project.objects.get(id=project_id)
#         except:
#             return Response(
#                 {"detail": "Project Not Found"},
#                 status = status.HTTP_404_NOT_FOUND,
#             )

#         serializer = ProjectSerializer(
#             project,
#             data=request.data
#         )

#         if serializer.is_valid():
#             update_project = serializer.save()

#             return Response(
#                 ProjectSerializer(update_project).data,
#                 status=status.HTTP_200_OK,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     def patch(self, request, project_id):
#         try:
#             project = Project.objects.get(id=project_id)
#         except:
#             return Response(
#                 {"details": "Project Not Found"},
#                 status = status.HTTP_404_NOT_FOUND,
#             )

#         serializer = ProjectSerializer(
#             project,
#             data=request.data,
#             # Keeping partial = true, since this is a patch request
#             partial=True,
#         )

#         if serializer.is_valid():
#             update_project = serializer.save()

#             return Response(
#                 ProjectSerializer(update_project).data,
#                 status=status.HTTP_200_OK,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     def delete(self, request, project_id):
#         try:
#             project = Project.objects.get(id=project_id)
#         except:
#             return Response(
#                 {"detail":"Project Not Found"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         project.delete()

#         return Response(
#             status=status.HTTP_204_NO_CONTENT,
#         )

# class ProjectListCreateView(generics.ListCreateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

#     def perform_create(self, serializer):
#         serializer.save(created_by=User.objects.first())

# class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     lookup_url_kwarg = "project_id"

# class ProjectListCreateMixinView(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     generics.GenericAPIView
# ):

#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def perform_create(self, serializer):
#             serializer.save(created_by=User.objects.first())

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [
        ProjectPermission
    ]

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

    @action(detail=False, methods=["get"], permission_classes=[IsQAEngineer])
    def qa_only(self, request):
        return Response({
            "message": "You are allowed to access the QA Engineer endpoint",
            "user": request.user.email,
            "role": request.user.role
        })
    