from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    campus = models.CharField(max_length=20, blank=False)
    faculty = models.CharField(max_length=20, blank=False)
    department = models.CharField(max_length=20, blank=False)
    matriculation_number = models.CharField(max_length=14, blank=False, unique=True)
    session = models.CharField(max_length=5, blank=False)

 

    def __str__(self):
        return self.username
    
