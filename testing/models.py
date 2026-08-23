import uuid
from django.conf import settings
from django.db import models

# Create your models here.
class TestSuite(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    # We want to delete the test suite if the project is deleted, so we use CASCADE here
    project = models.ForeignKey(
        # This is the lazy reference to the Project model in the Projects app.
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="test_suites",
    )

    name = models.CharField(
        max_length = 150
    )

    description = models.TextField(
        blank = True
    )

    # We don't want historical test suites to be deleted if the user is deleted, so we use PROTECT here
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name="created_test_suites"
    )

    created_at = models.DateTimeField(
        auto_now_add = True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "name"],
                name="unique_test_suite_name_per_project"
            ),
        ]

    def __str__(self):
        return f"{self.project.key} - {self.name}"

class Tag(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    # We want tags to be deleted if the project is deleted, so we use CASCADE here
    project = models.ForeignKey(
        "projects.Project", 
        on_delete=models.CASCADE, 
        related_name="tags"
    )

    name = models.CharField(
        max_length=50
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "name"],
                name="unique_tag_name_per_project",
            ),
        ]

    def __str__(self):
        return self.name

class TestCase(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = 'CRITICAL', "Critical"

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', "draft"
        ACTIVE = "ACTIVE", "active"
        DEPRECATED = "DEPRECATED", "deprecated"

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    # We want the test cases to be deleted if the test suite is deleted, so we use CASCADE here
    suite = models.ForeignKey(
        TestSuite, 
        on_delete=models.CASCADE, 
        related_name="test_cases"
    )

    tags = models.ManyToManyField(
        Tag, 
        related_name="test_cases", 
        blank=True
    )

    case_key = models.CharField(
        max_length=20
    )

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    preconditions = models.TextField(
        blank=True
    )

    steps = models.TextField(
        blank=True
    )

    expected_results = models.TextField(
        blank=True
    )

    priority = models.CharField(
        max_length=10, 
        choices=Priority.choices, 
        default=Priority.MEDIUM
    )

    status = models.CharField(
        max_length=15, 
        choices=Status.choices, 
        default=Status.DRAFT
    )

    # We dont want historical test cases to be deleted if the user is deleted, so we use PROTECT here
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["suite", "case_key"],
                name = "unique_case_key_per_suite",
            ),
        ]
    
    def __str__(self):
        return f"{self.case_key} - {self.title}"

class TestRun(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        RUNNING = "RUNNING", "Running"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # We want the test runs to be protected if the test suite is deleted
    suite = models.ForeignKey(
        TestSuite,
        on_delete=models.PROTECT,
        related_name="test_runs",
    )

    name = models.CharField(
        max_length=150,
    )

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_test_runs",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.suite.project.key} - {self.name}"

class TestResult(models.Model):

    class Status(models.TextChoices):
        PASSED = "PASSED", "Passed"
        FAILED = "FAILED", "Failed"
        SKIPPED = "SKIPPED", "Skipped"
        BLOCKED = "BLOCKED", "Blocked"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # We want the test results to be deleted if the test run is deleted
    test_run = models.ForeignKey(
        TestRun,
        on_delete=models.CASCADE,
        related_name="results",
    )

    # We dont want test results to be delted if the test case is deleted
    test_case = models.ForeignKey(
        TestCase,
        on_delete=models.PROTECT,
        related_name="results",
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
    )

    duration = models.FloatField(
        null=True,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    executed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["test_run", "test_case"],
                name="unique_test_result_per_run",
            ),
        ]

    def __str__(self):
        return f"{self.test_run.name} - {self.test_case.case_key}"