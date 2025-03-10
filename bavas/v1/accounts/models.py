import jwt
import uuid

from django.contrib.auth.models import AbstractUser
from bavas.settings import JWT_SECRET_KEY
from django.db import models

# Create your models here.

class UserMaster(AbstractUser):
    """
    Model to User Master Data
    """
    user_type = models.CharField(default="", max_length=100, null=True, blank=True)

    groups = None
    user_permissions = None

    @property
    def create_access_token(self):
        """function to create access token"""
        token = jwt.encode({'id': str(uuid.uuid1())},
                           JWT_SECRET_KEY + str(self.id),
                           algorithm='HS256')
        session = UserSession.objects.create(user=self, auth_key=token)
        return token



class UserSession(models.Model):
    """Model to store auth keys"""

    user = models.ForeignKey(
        UserMaster, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='user_sessions')
    is_active = models.IntegerField(default=1)
    auth_key = models.CharField(max_length=1000, default='', null=True, blank=True, )
    auth_key_expiry = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_sessions'

    def __str__(self):
        """Object Name in Django Model."""
        return f'{self.id}: '


