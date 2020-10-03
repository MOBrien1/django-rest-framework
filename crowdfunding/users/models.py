from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    organisation = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.CharField(max_length=1000)
    profile_pic = models.URLField()
    pet_pic = models.URLField()
    location = models.CharField(max_length=100)


@receiver(post_save, sender=CustomUser)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        instance.profile= UserProfile.objects.create(user=instance)