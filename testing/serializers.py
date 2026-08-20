from rest_framework import serializers
from .models import TestCase, TestSuite

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = [
            "id",
            "suite",
            "case_key",
            "title",
            "description",
            "preconditions",
            "steps",
            "expected_results",
            "priority",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        status = attrs.get("status")
        steps = attrs.get("steps")
        expected_results = attrs.get("expected_results")

        if status == TestCase.Status.ACTIVE:
            if not steps:
                raise serializers.ValidationError({
                    "steps": "Active test cases must have execution steps"
                })

            if not expected_results:
                raise serializers.ValidationError({
                    "expected_results": (
                        "Active test cases must have an expected result"
                    )
                })
        return attrs

class TestSuiteSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSuite
        fields = [
            "id",
            "name",
        ]

class TestCaseSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = [
            "id",
            "case_key",
            "title",
            "priority",
            "status",
        ]

class TestSuiteSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSummarySerializer(
        many=True, 
        read_only=True,
    )
    class Meta:
        model = TestSuite
        fields = [
            "id",
            "project",
            "name",
            "description",
            "created_by",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]