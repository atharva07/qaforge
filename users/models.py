import uuid
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

# user = username="atharva123", email="atharva123@gmail.com", password="TestAdmin"
# user2 = username="johnwick"m email="johnwick@gmail.com", password="JohnAdmin"
# Create your models here.
class User(AbstractUser, PermissionsMixin):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin",
        QA_ENGINEER = "QA_ENGINEER", "QA Engineer"
        DEVELOPER = "DEVELOPER", "Developer"
        VIEWER = "VIEWER", "Viewer"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,   
        default=Role.VIEWER
    )

    username = None

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )