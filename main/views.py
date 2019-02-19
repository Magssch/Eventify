from django.shortcuts import render
from .models import Event

# Create your views here.

def homepage(request):


	
	return render(request = request,
                  template_name ="main/home.html",
                  context = {"events":Event.objects.all})

