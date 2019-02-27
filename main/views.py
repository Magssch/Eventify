# Django imports
# djano.utils
from django.utils import timezone
# django shortcuts
from django.shortcuts import render, redirect, reverse, get_object_or_404
# django.contrib
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
# django.urls and django.views
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView
# django.core:
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage

# Local project imports
from .models import Event
from .forms import RegistrationForm, EditProfileForm, EventForm


# Create your views here.

def homepage(request):
	return render(request = request,
				  template_name = "main/home.html",
				  context = {"events":Event.objects.all})

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
			messages.success(request, f"Successfully edited profile")
			return redirect(reverse('profile'))
	else:
		form = EditProfileForm(instance=request.user)
		args = {'form': form}
		return render(request, 'registration/edit_profile.html', args)

def create_event(request):
	if not request.user.is_staff:
		return redirect('/')
  
	form = EventForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		event = form.save(commit=False)
		event.organizer = request.user
		event.save()
		messages.success(request, f"New event made: {form.cleaned_data.get('name')}")
		obj_name = form.cleaned_data.get('name')
		obj = get_object_or_404(Event, name=obj_name)
		return redirect(obj)

	form = EventForm()
	context = {
		'form': form
	}
	return render(request, "main/create_event.html", context)

def events(request):
	now = timezone.now()
	view_past = request.GET.get('view_past', False) == 'True'
	organizer = request.GET.get('organizer', False)

	if organizer != False:
		events_list = Event.objects.filter(organizer = request.user)
	elif view_past:
		events_list = Event.objects.all()
	else:
		events_list = Event.objects.filter(date__gte=now).order_by('date')

	paginator = Paginator(events_list, 4)  # Show 25 contacts per page
	page = request.GET.get('page')
	events = paginator.get_page(page)
	return render(request, 'main/events.html', {'events': events, 'view_past': view_past})

def event_info(request, my_id):
	obj = get_object_or_404(Event, id=my_id)
	context = {"object":obj}
	return render(request, "main/event_info.html", context)

def event_update(request, my_id=None):
	obj = get_object_or_404(Event, id=my_id)

	if not request.user.is_staff:
		messages.info(request, f"You must be logged into a staff account to update events.")
		return redirect('../')
	if not obj.organizer==request.user:
		messages.error(request, f"You must be the organizer of this event to update it.")
		return redirect('../')

	form = EventForm(request.POST or None, request.FILES or None, instance=obj)
	if form.is_valid():
		form.save()
		obj_name = form.cleaned_data.get('name')
		messages.success(request, f"Successfully updates event: {obj_name}")
		obj = get_object_or_404(Event, name=obj_name)
		return redirect(obj)
	form = EventForm(instance=obj)
	context = {
		'object': obj,
		'form': form
	}
	return render(request, "main/event_update.html", context)

