from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegistrationForm
from django.contrib.auth.models import User

# Create your views here.

def homepage(request):
	return render(request = request,
                  template_name = "main/home.html",
                  context = {"events":Event.objects.all})



def create_event(request):
	user = User.objects.get(pk=1)
	if not user.get('is_staff'):
		redirect('/')

	if request.method=='POST':
		form = EventForm(request=request, data=request.POST)
		if form.is_valid():
			form.save()
			redirect('/')

	form = EventForm()
	return render(request = request,
				  template_name = "main/create_event.html",
				  context={"form":form})

class SignUp(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'