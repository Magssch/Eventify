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
    

"""
Model that holds list of all attendees for events. Uses foreign key from user and Event 
to connect the tables. verbose_name adds label to database field making it more human relatable
while models.CASCADE ensure that on_delete both the user and event connection is deleted.
"""
class Attendee(models.Model):
    user = models.ForeignKey(User, verbose_name='Event', models.CASCADE)
    event = models.ForeignKey(Event, verbose_name='Attendee' models.CASCADE)
    has_paid = models.BooleanField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Attendee for Event'
        verbose_name_plural = 'Attendees for Events'
        unique_together = ('event', 'user')

    def save(self, *args, **kwargs):
        super(Attendee, self).save(*args, **kwargs)



