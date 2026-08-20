from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project
from .serializers import ProjectSerializer

# Create your views here.
class ProjectListCreateAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        