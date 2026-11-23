from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Student/teacher/admin. The email is used as the login username."""
    class Role(models.TextChoices):
        STUDENT = "student", "طالب"
        TEACHER = "teacher", "مدرس"
        ADMIN = "admin", "مسؤول"
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField("الهاتف", max_length=20, blank=True)
    stage = models.CharField("المرحلة", max_length=20, blank=True)
    grade = models.CharField("الصف", max_length=40, blank=True)
    email = models.EmailField(unique=True)
