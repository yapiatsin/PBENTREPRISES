from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models import Q
from django.conf import settings


GENDER_SELECTION = (
    ('Homme', 'Homme'),
    ('Femme', 'Femme'),
)
class User(AbstractUser):
    email = models.EmailField(unique=True, null= False)
    username = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER_SELECTION)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "gender"]
    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profession = models.CharField(max_length=50, null=True, blank="True")
    profile_pic = models.ImageField(upload_to='profile/', blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_SELECTION)
    commune = models.CharField(max_length=50, null=True, blank="True")
    def __str__(self):
        return f'{self.user.username} Profile'
    
            
    
