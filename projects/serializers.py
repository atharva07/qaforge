import re
from rest_framework import serializers
from testing.serializers import TestSuiteSummarySerializer

from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    test_suites = TestSuiteSummarySerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "key",
            "description",
            "created_by",
            "created_at",
            "updated_at",
            "test_suites",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
            "test_suites",
        ]

    def validate_key(self, value):
        if not 2 <= len(value) <= 10:
            raise serializers.ValidationError(
                "Project key must be between 2 and 10 characters"
            )

        if not re.fullmatch(r"[A-Z0-9]+", value):
            raise serializers.ValidationError(
                "Project key must contain only upper case letters an numbers."
            )

        return value

class ProjectTestReportSerializer(serializers.Serializer):
    project = serializers.CharField()
    total_results = serializers.IntegerField()
    passed = serializers.IntegerField()
    failed = serializers.IntegerField()
    skipped = serializers.IntegerField()
    blocked = serializers.IntegerField()
    average_duration = serializers.FloatField(
        allow_null=True
    )
    pass_rate = serializers.FloatField()