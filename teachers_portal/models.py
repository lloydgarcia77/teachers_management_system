from django.conf import settings
from django.db import models
from django.db.models.base import Model
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your views here.

class UserManager(BaseUserManager):
    """Manger for user profiles"""

    def create_user(self, email, password=None):
        """Create a new user profile"""

        if not email:
            raise ValueError('User must have email address')

        email = self.normalize_email(email)
        user = self.model(email=email, password=password)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email=email, password=password)
        user.staff = True
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password):
        """Create and save a new superuser with the given details"""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Customized model for user in django"""

 
    email = models.EmailField(max_length=50, unique=True)  
    date_added = models.DateTimeField(auto_now=True) 
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are  

    def __str__(self):
        return self.email
      
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
   
      