"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from projects.views import ProjectViewSet
from testing.views import TestSuiteViewSet, TestCaseViewSet, TestRunViewSet, TestResultViewSet
from users.views import UserViewSet
from rest_framework.routers import DefaultRouter
# from projects.views import ProjectListCreateAPIView, ProjectDetailAPIView
# from projects.views import ProjectListCreateView, ProjectDetailView, ProjectListCreateMixinView

router = DefaultRouter()

router.register(
    "projects",
    ProjectViewSet,
    basename="project"
)

router.register(
    r"test-suites",
    TestSuiteViewSet,
    basename="test-suite",
)

router.register(
    r"test-cases",
    TestCaseViewSet,
    basename="test-case",
)

router.register(
    r"test-runs",
    TestRunViewSet,
    basename="test-run",
)

router.register(
    r"test-results",
    TestResultViewSet,
    basename="test-result",
)

router.register(
    r"users",
    UserViewSet,
    basename="users"
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # path("api/projects/", ProjectListCreateView.as_view(), name="project-list-create"),
    # path("api/projects/<uuid:project_id>/", ProjectDetailView.as_view(), name="project-detail"),
    # path("api/projects-mixin/", ProjectListCreateMixinView.as_view(), name="project-list-create-mixin"),
]

urlpatterns += router.urls