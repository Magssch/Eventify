from django import forms
from django.shortcuts import get_object_or_404
from .models import Event

class EventForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = ['name', 'date', 'location', 'price', 'description']

