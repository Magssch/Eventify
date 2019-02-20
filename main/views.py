from django.shortcuts import render
from .models import Event
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegistrationForm

# Create your views here.

def homepage(request):
	return render(request = request,
                  template_name ="main/home.html",
                  context = {"events":Event.objects.all})


class SignUp(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def profile(request):
	return render(request = request,
                  template_name ="main/profile.html",
                  context = {"events":Event.objects.all})
