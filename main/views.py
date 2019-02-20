from django.shortcuts import render
from .models import Event
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegistrationForm, EditProfileForm
from django.shortcuts import redirect, reverse

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

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'registration/edit_profile.html', args)
