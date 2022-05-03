from django.db import models
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    events = models.CharField(max_length=50)


class Event(models.Model):
    title = models.CharField(max_length=200)  # event title
    seekgeek_id = models.IntegerField()  # seekgeek title_id
    url = models.URLField(max_length=200)
    pub = models.DateTimeField()
    performer = models.CharField(max_length=200)
    # <-- type of event sport, concert ect..
    kind = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)



