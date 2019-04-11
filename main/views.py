# Django imports:
# django.db
# Python imports:
import re

# django.contrib
from django.contrib import messages
# django.urls and django.views
# django.core:
from django.core.paginator import Paginator
from django.db import IntegrityError
# django shortcuts
from django.shortcuts import render, redirect, reverse, get_object_or_404
# djano.utils
from django.utils import timezone
# Django-newsletter:
from newsletter.models import Newsletter, Subscription, Submission

from .forms import (
    RegistrationForm,
    EditUserForm,
    EventForm,
    MessagingForm,
    ArticleForm,
    SubscribeNewsletterForm
)
# Local project imports
from .models import Event, Attendee

# ENUMS
SITE_NEWSLETTER = "Eventify"
SITE_EMAIL = 'eventify.site@gmail.com'


# Create your views here.
def homepage(request):
    try:
        '''newsletter = Newsletter.objects.get(title=SITE_NEWSLETTER)'''
    except Newsletter.DoesNotExist:
        Newsletter.objects.create(title=SITE_NEWSLETTER, email=SITE_EMAIL, sender=SITE_NEWSLETTER,
                                  slug=SITE_NEWSLETTER.lower())

    return render(request=request,
                  template_name="main/home.html",
                  context={"events": Event.objects.all})


"""
class SignUp(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
"""


def SignUp(request):
    ''' A view for anonymous users to sign up to Eventify. '''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        sub_form = SubscribeNewsletterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if sub_form.is_valid():
                try:
                    sub = sub_form.save(commit=False)
                    sub.user = user
                    sub.newsletter = Newsletter.objects.get(title=SITE_NEWSLETTER)
                    sub.save()
                except Newsletter.DoesNotExist:
                    messages.error(request,
                                   "No newsletter named {}, please contact costumer services."
                                   .format(SITE_NEWSLETTER))
                messages.success(request, "User successfully created!")
                return redirect('login')
            else:
                messages.error(request, "Error in newsletter-form")
        else:
            messages.error(request, "Error in signup-form")
            print(form.errors)

    form = RegistrationForm()
    sub_form = SubscribeNewsletterForm()
    context = {
        'form': form,
        'sub_form': sub_form
    }
    return render(request=request, template_name='registration/signup.html', context=context)


def profile(request):
    ''' A profile page with a simple overview of contact detail. '''
    try:
        newsletter = Newsletter.objects.get(title=SITE_NEWSLETTER)
        subscription = Subscription.objects.get(newsletter=newsletter, user=request.user).subscribed
    except (Newsletter.DoesNotExist):
        messages.error(request, "NewsletterError")
        subscription = False
    context = {
        "subscribed": subscription
    }
    return render(request=request,
                  template_name="main/profile.html", context=context)


def terms(request):
    return render(request=request,
                  template_name="main/terms.html",
                  context={"events": Event.objects.all})


def edit_profile(request):
    ''' Check if the user is subscribed and pass that instance into the subscription form. '''

    try:
        newsletter = Newsletter.objects.get(title=SITE_NEWSLETTER)
        subscription = Subscription.objects.get(newsletter=newsletter, user=request.user)
    except (Newsletter.DoesNotExist):
        messages.error(request, "NewsletterError")
        subscription = None

    if request.method == 'POST':
        form = EditUserForm(request.POST or None, instance=request.user)
        sub_form = SubscribeNewsletterForm(request.POST or None, instance=subscription)
        if form.is_valid():
            form.save()
            if sub_form.is_valid():
                try:
                    sub_form.save()
                except Newsletter.DoesNotExist:
                    messages.error(request, "No newsletter called Eventify")
                finally:
                    messages.success(request,
                                     "Successfully updated your profile")
                    return redirect('profile')
            messages.success(request, f"Successfully edited profile")
            return redirect(reverse('profile'))

    else:
        form = EditUserForm(instance=request.user)
        sub_form = SubscribeNewsletterForm(instance=subscription)
        context = {
            'form': form,
            'sub_form': sub_form
        }
        return render(request, 'registration/edit_profile.html', context)


def create_event(request):
    ''' A view where staff and superuser can create new events '''
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
        new_slug = event_name.lower()
        new_slug = re.sub(r'[\s]', '-', new_slug)  # Replace all spaces with dash.
        new_slug = re.sub(r'[^\w|-]', '', new_slug)  # Remove all non alphabetic characters except dash.
        newsletter = Newsletter(title=event_name, slug=new_slug, email="eventify.site@gmail.com", sender="Eventify")
        newsletter.save()
        return redirect(event)

    form = EventForm()
    context = {
        'form': form
    }
    return render(request, "main/create_event.html", context)


def events(request):
    ''' A view of all events '''
    now = timezone.now()
    view_past = request.GET.get('view_past', False) == 'True'
    organizer = request.GET.get('organizer', False)
    my_events = request.GET.get('my_events', False)

    if organizer is not False:
        events_list = Event.objects.filter(organizer=request.user).order_by('date')
    elif my_events is not False:
        events_list = Event.objects.filter(attendee__user=request.user).order_by('date')
    elif view_past:
        events_list = Event.objects.all().order_by('-date')
    else:
        events_list = Event.objects.filter(date__gte=now).order_by('date')

    paginator = Paginator(events_list, 4)  # Show 4 events per page
    page = request.GET.get('page')
    events = paginator.get_page(page)
    context = {
        'events': events,
        'view_past': view_past
    }
    return render(request, 'main/events.html', context)


def event_info(request, my_id):
    ''' Detailed info about a specific event where users can click attend and subscribe to the event. '''
    event = get_object_or_404(Event, id=my_id)
    newsletter = Newsletter.objects.get(title=event.name)
    attendees = Attendee.objects.filter(event=event)
    now = timezone.now()

    is_upcoming = Event.objects.filter(id=my_id, date__gte=now).exists()
    registration_open = Event.objects.filter(id=my_id, registration_starts__lte=now).exists()

    ''' A logical test if the current user is already attending or/and subscribing to the event. '''
    if not request.user.is_anonymous:
        am_I_attending = Attendee.objects.filter(event=event, user=request.user).exists()
        am_I_subscribed = Subscription.objects.filter(newsletter=newsletter, user=request.user).exists()
    else:
        am_I_attending = False
        am_I_subscribed = False

    # If a user wants to attend we must check if he/she is logged in.
    # Also we want to check if the number of attendees does not preceed the capacity.
    if request.method == "POST":
        try:
            if request.user.is_anonymous:
                messages.info(request, "Please login or register to attend or subscribe event.")
                return redirect('event_info', my_id)
            if request.POST.get('attend') == 'Attend' or request.POST.get('unattend') == 'Unattend':
                if attendees.count() < event.capacity and not am_I_attending:
                    # attend the event
                    attendee = Attendee.objects.create(user=request.user, event=event)
                    attendee.save()
                    messages.success(request, f"Successfully signed up for {event.name}")
                    return redirect('event_info', my_id)
                elif am_I_attending:
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
        except IntegrityError:
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
    ''' An update view for specific events, allowed for organizer and superuser. '''
    event = get_object_or_404(Event, id=my_id)
    old_event_name = event.name
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You must be logged into a staff account to update events.")
        return redirect('../')
    if not (event.organizer == request.user or request.user.is_superuser):
        messages.error(request, "You must be the organizer of this event to update it.")
        return redirect('../')

    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        try:
            new_event = form.save(commit=False)
            newsletter = Newsletter.objects.get(title=old_event_name)
            newsletter.title = new_event.name
            newsletter.save()
            new_event.save()
            event_name = form.cleaned_data.get('name')
            messages.success(request, f"Successfully updates event: {event_name}")
            event = get_object_or_404(Event, name=event_name)
        except Newsletter.DoesNotExist:
            messages.error(request, "An error has occured with the database, please contact costumer service.")
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
    ''' A confirmation view to delete an event, allowed for organizer and superuser. '''
    event = get_object_or_404(Event, id=my_id)
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You do not have this privilege.")
        return redirect('../')
    if not (event.organizer == request.user or request.user.is_superuser):
        messages.error(request, "You must be the organizer of this event to delete it.")
        return redirect('../')

    if request.method == "POST":
        # Confirming delete
        event.delete()
        return redirect('../../')
    context = {
        "event": event
    }
    return render(request, "main/event_delete.html", context)


def event_attendees(request, my_id):
    ''' A view with a list of all attendees for a specific event, allowed for organizer and superuser. '''
    event = get_object_or_404(Event, id=my_id)
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You do not have the privilege to see this page.")
        return redirect('../')
    if not (event.organizer == request.user or request.user.is_superuser):
        messages.error(request, "You must be the organizer of this event to look at this page")
        return redirect('../')

    attendees = Attendee.objects.filter(event=event)
    context = {
        "event": event,
        "attendees": attendees
    }
    return render(request, "main/event_attendees.html", context)


def event_newsletter(request, my_id):
    ''' Newsletter function specific event, allowed for staff and superuser. '''
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('/')

    event = get_object_or_404(Event, id=my_id)

    messagingForm = MessagingForm(request.POST or None)
    articleForm = ArticleForm(request.POST or None)
    if messagingForm.is_valid():
        message = messagingForm.save(commit=False)
        slug = message.title.lower()
        slug = re.sub(r'[\s]', '-', slug)  # Replace all spaces with dash.
        slug = re.sub(r'[^\w|-]', '', slug)  # Remove all non alphabetic characters except dash.
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


def site_newsletter(request):
    ''' A view for superuser to send out site-wide newsletter to subscribed users.  '''
    if not request.user.is_superuser:
        return redirect('/')

    messagingForm = MessagingForm(request.POST or None)
    articleForm = ArticleForm(request.POST or None)

    if messagingForm.is_valid():
        message = messagingForm.save(commit=False)
        slug = message.title.lower()
        slug = re.sub(r'[\s]', '-', slug)  # Replace all spaces with dash.
        slug = re.sub(r'[^\w|-]', '', slug)  # Remove all non alphabetic characters except dash.
        message.slug = slug
        newsletter_name = SITE_NEWSLETTER
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
                return redirect('site_newsletter')

    MessagingForm()
    ArticleForm()
    context = {
        'messagingForm': messagingForm,
        'articleForm': articleForm
    }
    return render(request, "main/site_newsletter.html", context)
