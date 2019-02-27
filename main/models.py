from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Event(models.Model):
    name        = models.CharField(unique=True, max_length=30)
    organizer   = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date        = models.DateField()
    location    = models.CharField(max_length=30)
    price       = models.IntegerField()
    description = models.TextField()
    image       = models.ImageField(upload_to='event_image', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("event_info", kwargs={"my_id": self.id})
    

class Attendee(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    event = models.ForeignKey(Event, models.CASCADE)
    has_paid = models.BooleanField()



