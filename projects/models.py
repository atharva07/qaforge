import uuid
from django.conf import settings
from django.db import models

# Create your models here.
class Project(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=150,
    )

    key = models.CharField(
        max_length=20,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    # We don't want historical projects to be deleted if the user is deleted, so we use PROTECT here
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_projects",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.key} - {self.name}"

class ProjectMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        MEMBER = "MEMBER", "Member"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # We want to delete the membership if the user is deleted, so we use CASCADE here
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_memberships",
    )

    # We want to delete the membership if the project is deleted
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # This class gives us the addional instructions about how this model should behave. 
    # In this case, we are adding a unique constraint to ensure that a user can only be a member of a project once.
    # A constraint is a rule that database must enforce.
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["project", "user"],
                name = "unique_project_membership",
            ),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.project.key}"