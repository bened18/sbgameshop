from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_editor = models.BooleanField(
        default=False
    )

    REQUIRED_FIELDS = ['email']
