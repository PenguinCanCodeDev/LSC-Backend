from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(
        unique=True, 
        help_text="The student's unique email address."
    )
    first_name = models.CharField(
        max_length=30, 
        help_text="The student's first name."
    )
    last_name = models.CharField(
        max_length=30, 
        help_text="The student's last name."
    )
    campus = models.CharField(
        max_length=20,
        help_text="The student's campus"
    )
    faculty = models.CharField(
        max_length=20, 
         help_text="The student's faculty"
    )
    department = models.CharField(
        max_length=20, 
        help_text="The student's department"
    )
    matriculation_number = models.CharField(
        max_length=14, 
        unique=True,
        help_text="The student's matriculation number"
    )
    session = models.CharField(max_length=5, blank=False)

    is_staff =  models.BooleanField(
        default=False,
        help_text='Indicates if this user is a staff of LSC'
    )
    is_superuser = models.BooleanField(
        default=False, 
        help_text='Indicates whether the user has all admin permissions. Defaults to False.'
    )
    is_active = models.BooleanField(
        default=True, 
        help_text='Indicates whether the user account is active. Defaults to False and user needs to verify email on signup before it can be set to True.'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True, 
        help_text='The date and time when the user joined.',
        null=True, 
        blank=True
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date and time this user last logged in'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def auth_tokens(self):
        refresh = RefreshToken.for_user(self)

        # update last login date
        self.last_login = timezone.now()
        self.save()
        
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }