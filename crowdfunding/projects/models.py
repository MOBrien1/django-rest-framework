from django.db import models
from django.contrib.auth import get_user_model

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    post_code = models.CharField(max_length=200, default='Unknown')
    suburb = models.CharField(max_length=50, default='Unknown')
    seeking = models.CharField(max_length=200, default='Unknown')
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField()
    #owner = models.CharField(max_length=200)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owner_projects'
    )

#pledge through comment system---can you add multilpe comment threads determined by users??
class Pledge(models.Model):
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    #supporter = models.CharField(max_length=200)
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )

# comment response system 
#class Pledge_response(models.Model):
#    comment = models.CharField(max_length=200)
#    project = models.ForeignKey(
#        'Project',
#        on_delete=models.CASCADE,
#        related_name='pledges'
#    )
#    owner = models.ForeignKey(
#        get_user_model(),
#        on_delete=models.CASCADE,
#        related_name='owner_pledge_'
#    )

class Donations(models.Model):
    item = models.CharField(max_length=200)
    quantity = models.IntegerField()
    img = models.URLField()
    location = models.CharField(max_length=200)
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_donation'
    )

class DonationItems(models.Model):
    item = models.CharField(max_length=100)

