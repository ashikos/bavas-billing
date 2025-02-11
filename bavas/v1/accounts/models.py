from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserMaster(AbstractUser):
    """
    Model to User Master Data
    """
    user_type = models.CharField(default="", max_length=100, null=True, blank=True)

    groups = None
    user_permissions = None

