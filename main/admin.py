from django.contrib import admin

from .models import Event, Attendee

# Register models here.

admin.site.register(Event)
admin.site.register(Attendee)
