from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200) # event title
    seekgeek_id = models.IntegerField() # seekgeek title_id
    url = models.URLField(max_length=200)
    pub = models.DateTimeField()
    performer = models.CharField(max_length=200)
    kind = models.CharField(max_length=200) # <-- type of event sport, concert ect..
    










