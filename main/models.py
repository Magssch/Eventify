from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_level = models.IntegerField()
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    address = models.CharField(max_length=30)
    accept_notifications = models.BooleanField()
    accept_newsletter = models.BooleanField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Event(models.Model):
    name        = models.CharField(max_length=30)
    organizer   = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date        = models.DateTimeField()
    location    = models.CharField(max_length=30)
    price       = models.IntegerField()
    description = models.TextField()
    image       = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("event_info",kwargs={"my_id": self.id})
    

class Attendee(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    event = models.ForeignKey(Event, models.CASCADE)
    has_paid = models.BooleanField()



