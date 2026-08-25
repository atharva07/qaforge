from rest_framework import serializers
from .models import User

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = [
            "id",
            "email",
            "role",
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = [
            "id",
            "email",
            "role",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only = True,
        min_length = 8,
    )

    class Meta:
        model = User

        fields = [
            "email",
            "password",
            "role",
            "created_at",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(
            **validated_data
        )    

        user.set_password(password)
        user.save()

        return user