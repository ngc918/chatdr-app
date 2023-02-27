from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionManager, BaseUserManager

# Create your models here.

class CustomUser(BaseUserManager):
    def _create_user(self, username, password, **extrafields):
        if not username:
            raise ValueError("Username is required")
        
        user = self.model(username=username, **extrafields)
        user.set_password(password)
        user.save()
        return user
