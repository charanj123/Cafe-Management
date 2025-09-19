from email.policy import default
from enum import unique
from operator import truediv
from pickle import TRUE
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    #creating a new user  (over Writing the existing one)
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email = self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    #creating a superuser  (over Writing the existing one)
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class userAccount(AbstractBaseUser):
    username        = models.CharField(max_length=20, unique=True)
    email           = models.EmailField(verbose_name = "email", max_length=60, unique=True)
    phone_number    = models.CharField(max_length=50)
    gender          = models.CharField(max_length=10, unique=False, null=True)
    Address         = models.CharField(max_length=100, unique=True, null=True)
    user_DOB        = models.DateField(null=True)
    date_joined     = models.DateTimeField(verbose_name="date joined", auto_now_add = True)
    last_login      = models.DateTimeField(verbose_name="last login", auto_now = True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    #imagefield need package PILLOW
    hide_email      = models.BooleanField(default=True)


    objects = MyAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    #this functions overwrite permission 
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
                  


#must add AUTH_USER_MODEL = "appname.class" in settings
