# Django imports:
# django.db
from django.db import IntegrityError
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
from django.contrib.auth import login, authenticate

# Local project imports
from .models import Event, Attendee
from .forms import (
    RegistrationForm,
    EditUserForm,
    EventForm,
    ProfileForm,
    EditProfileForm,
    MessagingForm,
    ArticleForm
)

# Django-newsletter:
from newsletter.models import Newsletter, Subscription, Submission


# Create your views here.

def homepage(request):
    return render(request = request,
                  template_name = "main/home.html",
                  context = {"events":Event.objects.all})

"""
class SignUp(generic.CreateView):
	form_class = RegistrationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/signup.html'
"""
def SignUp(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		profile_form = ProfileForm(request.POST)
		if form.is_valid() and profile_form.is_valid():
			user = form.save()
			user.refresh_from_db()  # load the profile instance created by the signal
			user.profile.subscribed = form.cleaned_data.get('subscribed')
			user.save()
			return redirect(reverse_lazy('login'))
	else:
		form = RegistrationForm()
		profile_form = ProfileForm()
	return render(request, 'registration/signup.html', {'form': form, 'profile_form': profile_form})


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
		form = EditUserForm(request.POST, instance=request.user)
		profile_form = EditProfileForm(request.POST, instance=request.user.profile)

		if form.is_valid() and profile_form.is_valid():
			form.save()
			profile_form.save()
			messages.success(request, f"Successfully edited profile")
			return redirect(reverse('profile'))
	else:
		form = EditUserForm(instance=request.user)
		profile_form = EditProfileForm(instance=request.user.profile)
		args = {'form': form, 'profile_form': profile_form}
		return render(request, 'registration/edit_profile.html', args)

def create_event(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('/')

    form = EventForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.save()
        messages.success(request, f"New event created: {form.cleaned_data.get('name')}")
        event_name = form.cleaned_data.get('name')
        event = get_object_or_404(Event, name=event_name)
        newsletter = Newsletter(title=event_name, slug=event_name.lower(), email="eventify.site@gmail.com", sender="Eventify")
        newsletter.save()
        return redirect(event)
    else:
        print(form.errors)

    form = EventForm()
    context = {
        'form': form
    }
    return render(request, "main/create_event.html", context)

def events(request):
    now = timezone.now()
    view_past = request.GET.get('view_past', False) == 'True'
    organizer = request.GET.get('organizer', False)
    my_events = request.GET.get('my_events', False)

    if organizer != False:
        events_list = Event.objects.filter(organizer = request.user)
    elif my_events != False:
        events_list = Event.objects.filter(attendee__user = request.user)
    elif view_past:
        events_list = Event.objects.all()
    else:
        events_list = Event.objects.filter(date__gte=now).order_by('date')

    paginator = Paginator(events_list, 4)  # Show 25 contacts per page
    page = request.GET.get('page')
    events = paginator.get_page(page)
    context = {
        'events': events,
        'view_past': view_past
    }
    return render(request, 'main/events.html', context)

def event_info(request, my_id):
    event = get_object_or_404(Event, id=my_id)
    newsletter = Newsletter.objects.get(title=event.name)
    attendees = Attendee.objects.filter(event=event)
    now = timezone.now()

    is_upcoming = Event.objects.filter(id=my_id, date__gte=now).exists()

    registration_open = Event.objects.filter(id=my_id, registration_starts__lte=now).exists()


    if not request.user.is_anonymous:
        am_I_attending = Attendee.objects.filter(event=event, user=request.user).exists()
        am_I_subscribed = Subscription.objects.filter(newsletter=newsletter, user=request.user).exists()
    else:
        am_I_attending = False
        am_I_subscribed = False

    # If a user wants to attend we must check if he/she is logged in.
    # Also we want to check if the number of attendees does not preceed the capacity.
    if request.method=="POST":
        try:
            if request.user.is_anonymous:
                messages.info(request, "Please login or register to attend or subscribe event.")

            if  request.POST.get('attend') == 'Attend' or request.POST.get('unattend') == 'Unattend':
                if attendees.count() < event.capacity and am_I_attending==False:
                    # attend the event
                    attendee = Attendee.objects.create(user=request.user, event=event)
                    attendee.save()
                    messages.success(request, f"Successfully signed up for {event.name}")
                    return redirect('event_info', my_id)
                elif am_I_attending==True:
                    # unattend the event
                    attendee = Attendee.objects.filter(event=event, user=request.user)
                    attendee.delete()
                    messages.success(request, f"Successfully unattended {event.name}")
                    return redirect('event_info', my_id)
                else:
                    # base-case: capacity reached maximum, do not allow more attendees
                    messages.error(request, "Sorry, you were too late. The event is full")
                    return redirect('event_info', my_id)
            elif request.POST.get('subscribe') == 'Subscribe':
                # add subscription
                subscription = Subscription.objects.create(user=request.user, newsletter=newsletter, subscribed=True)
                subscription.save()
                messages.success(request, f"Successfully subscribed to newsletter: {event.name}")
                return redirect('event_info', my_id)
            elif request.POST.get('unsubscribe') == 'Unsubscribe':
                # remove subscription.
                subscription = Subscription.objects.filter(user=request.user, newsletter=newsletter)
                subscription.delete()
                messages.success(request, "Successfully unsubscribed to newsletter.")
                return redirect('event_info', my_id)
        except IntegrityError as e:
            messages.error(request, "You have already signed up for this event")
            return redirect('event_info', my_id)

    context = {
        "event": event,
        "attendees": attendees,
        "am_I_attending": am_I_attending,
        "am_I_subscribed": am_I_subscribed,
        "is_upcoming": is_upcoming,
        "registration_open": registration_open,

    }

    return render(request, "main/event_info.html", context)


def event_update(request, my_id=None):
	event = get_object_or_404(Event, id=my_id)

	if not (request.user.is_staff or request.user.is_superuser):
		messages.error(request, "You must be logged into a staff account to update events.")
		return redirect('../')
	if not (event.organizer==request.user or request.user.is_superuser):
		messages.error(request, "You must be the organizer of this event to update it.")
		return redirect('../')

	form = EventForm(request.POST or None, request.FILES or None, instance=event)
	if form.is_valid():
		form.save()
		event_name = form.cleaned_data.get('name')
		messages.success(request, f"Successfully updates event: {event_name}")
		event = get_object_or_404(Event, name=event_name)
		return redirect(event)
	form = EventForm(instance=event)
	context = {
		'event': event,
		'form': form
	}
	return render(request, "main/event_update.html", context)

# An option to delete existing event.
# Has to be admin or the staff user that created the event.
def event_delete(request, my_id):
	event = get_object_or_404(Event, id=my_id)

	if not (request.user.is_staff or request.user.is_superuser):
		messages.error(request, "You do not have this privilege.")
		return redirect('../')
	if not (event.organizer==request.user or request.user.is_superuser):
		messages.error(request, "You must be the organizer of this event to delete it.")
		return redirect('../')

	if request.method =="POST":
		# Confirming delete
		event.delete()
		return redirect('../../')
	context = {
		"event": event
	}
	return render(request, "main/event_delete.html", context)

def event_attendees(request, my_id):
	event = get_object_or_404(Event, id=my_id)

	if not (request.user.is_staff or request.user.is_superuser):
		messages.error(request, "You do not have the privilege to see this page.")
		return redirect('../')
	if not (event.organizer==request.user or request.user.is_superuser):
		messages.error(request, "You must be the organizer of this event to look at this page")
		return redirect('../')

	attendees = Attendee.objects.filter(event=event)
	context = {
		"event": event,
		"attendees": attendees
	}
	return render(request, "main/event_attendees.html", context)


def event_newsletter(request, my_id):

    if not (request.user.is_staff or request.user.is_admin):
        return redirect('/')

    event = get_object_or_404(Event, id=my_id)

    messagingForm = MessagingForm(request.POST or None)
    articleForm = ArticleForm(request.POST or None)
    if messagingForm.is_valid():
        message = messagingForm.save(commit=False)
        slug = message.title.lower()
        slug = slug.replace(' ', '_')
        print(slug)
        message.slug = slug
        newsletter_name = event.name
        newsletter = Newsletter.objects.get(title=newsletter_name)
        message.newsletter = newsletter
        message.save()

        if articleForm.is_valid():
            article = articleForm.save(commit=False)
            article.title = ' '
            article.post = message
            article.save()

            if not (article is None or message is None):
                submission = Submission.objects.create(message=message, newsletter=newsletter)
                subs = Subscription.objects.filter(newsletter=newsletter)
                submission.subscriptions.set(subs)
                submission.prepared = True
                submission.save()
                messages.success(request, "Successfully submitted newsletter!")
                return redirect(event)

    MessagingForm()
    ArticleForm()
    context = {
        'messagingForm': messagingForm,
        'articleForm': articleForm
    }
    return render(request, "main/newsletter.html", context)
