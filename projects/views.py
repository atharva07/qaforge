from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project
from .serializers import ProjectSerializer
from users.models import User
from rest_framework import status

# Create your views here.
class ProjectListCreateAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()

        sreializer = ProjectSerializer(
            projects,
            many=True
        )

        return Response(sreializer.data)

    def post(self, request):
        serializer = ProjectSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            user = User.objects.first()
            project = serializer.save(
                created_by = user,
            )

            return Response(
                ProjectSerializer(project).data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400,
        )

class ProjectDetailAPIView(APIView):
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {
                    "detail": "Project not found"
                },
                status = status.HTTP_200_OK,
            )

        serializer = ProjectSerializer(project)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except:
            return Response(
                {"detail": "Project Not Found"},
                status = status.HTTP_404_NOT_FOUND,
            )

        serializer = ProjectSerializer(
            project,
            data=request.data
        )

        if serializer.is_valid():
            update_project = serializer.save()

            return Response(
                ProjectSerializer(update_project).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except:
            return Response(
                {"details": "Project Not Found"},
                status = status.HTTP_404_NOT_FOUND,
            )

        serializer = ProjectSerializer(
            project,
            data=request.data,
            # Keeping partial = true, since this is a patch request
            partial=True,
        )

        if serializer.is_valid():
            update_project = serializer.save()

            return Response(
                ProjectSerializer(update_project).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except:
            return Response(
                {"detail":"Project Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        project.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
