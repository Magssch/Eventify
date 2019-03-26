from django.contrib import admin
from .models import User, Event, Attendee, Profile

# Register your models here.

admin.site.register(Event)
admin.site.register(Attendee)
admin.site.register(Profile)