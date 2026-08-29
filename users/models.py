import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# user = username="atharva123", email="atharva123@gmail.com", password="TestAdmin"
# user2 = username="johnwick" email="johnwick@gmail.com", password="JohnAdmin"
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        QA_ENGINEER = "QA_ENGINEER", "QA Engineer"
        DEVELOPER = "DEVELOPER", "Developer"
        VIEWER = "VIEWER", "Viewer"

    username = None

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,   
        default=Role.VIEWER
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

    objects = UserManager()