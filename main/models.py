from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_level = models.IntegerField()
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()
    address = models.CharField(max_length=30)
    accept_notifications = models.BooleanField()
    accept_newsletter = models.BooleanField()


class Event(models.Model):
    name = models.CharField(max_length=30)
    organizer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField()
    location = models.CharField(max_length=30)
    price = models.IntegerField()
    

class Attendee(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    event = models.ForeignKey(Event, models.CASCADE)
    has_paid = models.BooleanField()

