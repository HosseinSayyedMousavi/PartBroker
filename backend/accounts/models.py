from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers for authentication instead of usernames
    """
    def create_user(self,phone_number,password,**extra_fields):
        """
        Create and save a User with the given email and password and extra fields
        """
        if not phone_number:
            raise ValueError(_("the phone number must be set"))
        if extra_fields.get("email"):
            email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,phone_number,password,**extra_fields):
        """
        Create and save a SuperUser with the given email and password and extra fields
        """
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_staff",True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    """
    Custom user model for our app
    """
    email = models.EmailField(max_length=255,null=True,blank=True)
    phone_number = models.CharField(max_length=11,unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser =  models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20,null=True,blank=True)
    last_name = models.CharField(max_length=20,null=True,blank=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["phone_number"]

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()
    def __str__(self):
        return self.phone_number

