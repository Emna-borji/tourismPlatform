
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, date



class CustomUserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, password=None, **extra_fields):
        """
        Creates and returns a regular user with an email, first name, last name, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, lastname=lastname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email, first name, last name, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, firstname, lastname, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=150)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)  # Add this line
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    dateofbirth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    profilepic = models.CharField(max_length=255, blank=True, null=True)
    tripstatus = models.CharField(max_length=50, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    blockstartdate = models.DateTimeField(blank=True, null=True)
    blockenddate = models.DateTimeField(blank=True, null=True)
    role = models.CharField(max_length=20, default="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname", "lastname"]

    objects = CustomUserManager()

    class Meta:
        db_table = "user"  # Match the existing PostgreSQL table
        managed = False  # Prevent Django from managing migrations for this table

    def __str__(self):
        return self.email
    
    def block_user(self, start_date, end_date):
        """Sets block start and end dates for a user."""
        self.blockstartdate = start_date
        self.blockenddate = end_date
        self.save()
    
    @property
    def is_blocked(self):
        """Check if the user is currently blocked based on blockstartdate and blockenddate."""
        now = timezone.now()  # Get the current time with timezone
        if self.blockstartdate and self.blockenddate:
            start = timezone.make_aware(self.blockstartdate, timezone.get_current_timezone()) if self.blockstartdate.tzinfo is None else self.blockstartdate
            end = timezone.make_aware(self.blockenddate, timezone.get_current_timezone()) if self.blockenddate.tzinfo is None else self.blockenddate
            return start <= now <= end
        return False

    