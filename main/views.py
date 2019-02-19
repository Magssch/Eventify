from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm

# Create your views here.

def homepage(request):


	
	return render(request = request,
                  template_name = "main/home.html",
                  context = {"events":Event.objects.all})


def create_event(request):
	if request.method=='POST':
		form = EventForm(request=request, data=request.POST)
		if form.is_valid():
			form.save()
			redirect('/')

	form = EventForm()
	return render(request = request,
				  template_name = "main/create_event.html",
				  context={"form":form})