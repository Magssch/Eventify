from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date

class Event(models.Model):
    name        = models.CharField(unique=True, max_length=30)
    organizer   = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date        = models.DateField()
    registration_starts    = models.DateField(default=timezone.now)
    location    = models.CharField(max_length=30)
    price       = models.IntegerField()
    description = models.TextField()
    image       = models.ImageField(upload_to='event_image', blank=True, null=True)
    capacity    = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    @property
    def registration_open(self):
        return date.today() >= self.registration_starts

    def get_absolute_url(self):
        return reverse("event_info", kwargs={"my_id": self.id})
    

class Attendee(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    event = models.ForeignKey(Event, models.CASCADE)
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " attending " + self.event.name

    class Meta:
        unique_together = ('event', 'user')