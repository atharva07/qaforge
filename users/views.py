from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserSummarySerializer,
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer

        return UserSerializer

    def get_permissions(self):

        if self.action == "me":
            permission_classes = [
                IsAuthenticated,
            ]

        else:
            permission_classes = [
                IsAdmin,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    @action(
        detail=False,
        methods=["get"],
    )
    def me(self, request):

        serializer = UserSummarySerializer(
            request.user
        )

        return Response(
            serializer.data
        )

