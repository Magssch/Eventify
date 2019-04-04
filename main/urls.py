from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views

# To reference the app, e.g. in django.shortcuts.redirect('main:homepage')

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('account/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='main/home.html'), name='home'),
    path('create_event/', views.create_event, name='create_event'),
    path('signup/', views.SignUp, name='signup'),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('terms', views.terms, name='terms'),


    path('events/', views.events, name="events"),
    path('events/<int:my_id>/', views.event_info, name="event_info"),
    # path('events/<int:id>/update/', views.event_update.as_view(), name="event_update"),
    path('events/<int:my_id>/update/', views.event_update, name="event_update"),
    path('events/<int:my_id>/delete/', views.event_delete, name="event_delete"),
    path('events/<int:my_id>/attendees/', views.event_attendees, name="event_attendees"),
    # URL-path for Newletter (import (un)subscription and archive)
    path('newsletter/', include('newsletter.urls')),
    path('events/<int:my_id>/event_newsletter/', views.event_newsletter, name="event_newsletter"),

    path('site_newsletter/', views.site_newsletter, name='site_newsletter'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
