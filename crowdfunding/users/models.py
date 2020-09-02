from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    organisation = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.CharField(max_length=1000)
    profile_pic = models.FilePathField()
    pet_pic = models.FilePathField()
    location = models.CharField(max_length=100)



