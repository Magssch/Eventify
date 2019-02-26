from django.shortcuts import render, redirect, reverse
from .models import Event
from .forms import EventForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RegistrationForm, EditProfileForm
from django.core.paginator import Paginator
from django.utils import timezone

# Create your views here.

def homepage(request):
	return render(request = request,
                  template_name = "main/home.html",
                  context = {"events":Event.objects.all})


# @staff_member_required
def create_event(request):
  if not request.user.is_staff:
    return redirect('/')

  form = EventForm(request.POST or None)
  if form.is_valid():
    form.save()
    return redirect('/')

  form = EventForm()
  context = {
      'form': form
  }
  return render(request, "main/create_event.html", context)

class SignUp(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def profile(request):
	return render(request = request,
                  template_name ="main/profile.html",
                  context = {"events":Event.objects.all})

def terms(request):
	return render(request = request,
                  template_name ="main/terms.html",
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

def events(request):
    now = timezone.now()
    view_past = request.GET.get('view_past', False) == 'True'
    if view_past:
        events_list = Event.objects.all()
    else:
        events_list = Event.objects.filter(date__gte=now).order_by('date')
    paginator = Paginator(events_list, 4)  # Show 25 contacts per page
    page = request.GET.get('page')
    events = paginator.get_page(page)
    return render(request, 'main/events.html', {'events': events, 'view_past': view_past})

