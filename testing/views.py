from rest_framework import viewsets

from users.models import User
from .models import (
    TestSuite, TestCase, TestRun, TestResult
)
from .serializers import (
    TestSuiteSerializer, TestCaseSerializer, TestRunSerializer, TestResultSerializer,
)
from .permissions import (
    CanManageTestSuite, CanManageTestCases,
    CanExecuteTests, TestSuiteObjectPermission,
    TestCasePermission, TestRunPermission, TestResultPermission
)
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
class TestSuiteViewSet(viewsets.ModelViewSet):
    # queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return TestSuite.objects.none()

        if user.role == User.Role.ADMIN:
            return TestSuite.objects.all()

        return TestSuite.objects.filter(
            project__memberships__user = user
        ).distinct()

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [TestSuiteObjectPermission]

        elif self.action == "retrieve":
            permission_classes = [TestSuiteObjectPermission]

        elif self.action == "create":
            permission_classes = [CanManageTestSuite]

        elif self.action in [
            "update",
            "partial_update",
            "destroy"
        ]:
            permission_classes = [
                CanManageTestSuite,
                TestSuiteObjectPermission,
            ]

        else:
            permission_classes = [
                TestSuiteObjectPermission
            ]

        return [
            permission() for permission in permission_classes
        ]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user
        )

class TestCaseViewSet(viewsets.ModelViewSet):
    # queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return TestCase.objects.none()

        if user.role == User.Role.ADMIN:
            return TestCase.objects.all()

        return TestCase.objects.filter(
            suite__project__memberships__user = user
        ).distinct()

    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve"
        ]:
            permission_classes = [
                TestCasePermission
            ]

        elif self.action == "create":
            permission_classes = [
                CanManageTestCases,
            ]

        elif self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [
                CanManageTestCases,
                TestCasePermission,
            ]

        elif self.action == "testexecute":
            permission_classes = [
                CanExecuteTests,
            ]

        else:
            permission_classes = [
                TestCasePermission,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user
        )

    @action(detail=True, methods=["post"], permission_classes=[CanExecuteTests])
    def testexecute(self, request, pk=None):
        test_case = self.get_object()

        return Response({
            "message": "Test case execution authorized.",
            "test_case": str(test_case.id),
            "case_key": test_case.case_key,
            "executed_by": request.user.email,
            "role": request.user.role,
        })

class TestRunViewSet(viewsets.ModelViewSet):
    # queryset = TestRun.objects.all()
    serializer_class = TestRunSerializer  

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return TestRun.objects.none()

        if user.role == User.Role.ADMIN:
            return TestRun.objects.all()

        return TestRun.objects.filter(
            suite__project__memberships__user = user
        ).distinct()  

    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve"
        ]:
            permission_classes = [
                TestRunPermission
            ]

        elif self.action == "create":
            permission_classes = [
                CanExecuteTests
            ]

        elif self.action in [
            "update",
            "partial_update"
        ]:
            permission_classes = [
                CanExecuteTests,
                TestRunPermission
            ]

        elif self.action == "testexecute":
            permission_classes = [
                CanExecuteTests
            ]

        else:
            permission_classes = [
                TestRunPermission
            ]

        return [
            permission() for permission in permission_classes
        ]

    def perform_create(self, serializer):
        serializer.save(
            created_by = self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[CanExecuteTests],
    )
    def testrun(self, request, pk=None):
        test_run = self.get_object()

        return Response({
            "message": "Test run execution authorized.",
            "test_run": str(test_run.id),
            "name": test_run.name,
            "executed_by": request.user.email,
            "role": request.user.role,
        })

class TestResultViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = TestResult.objects.all()
    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return TestResult.objects.none()

        if user.role == User.Role.ADMIN:
            return TestResult.objects.all()

        return TestResult.objects.filter(
            test_run__suite__project__memberships__user = user
        ).distinct()
    
    serializer_class = TestResultSerializer
    permission_classes = [
        TestResultPermission
    ]