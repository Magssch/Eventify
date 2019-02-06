from django.db import models

# Create your models here.

class Event(models.Model):
    event_title = models.CharField(max_length=200)
    event_description = models.TextField()
    event_published = models.DateTimeField('Date published')

    def __str__(self):
        return self.event_title