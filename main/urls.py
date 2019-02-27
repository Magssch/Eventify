from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# To reference the app, e.g. in django.shortcuts.redirect('main:homepage')

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('account/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='main/home.html'), name='home'),
    path('create_event/', views.create_event, name='create_event'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('terms', views.terms, name='terms'),


    path('events/', views.events, name="events"),
    path('events/<int:my_id>/', views.event_info, name="event_info"),
    # path('events/<int:id>/update/', views.event_update.as_view(), name="event_update"),
    path('events/<int:my_id>/update/', views.event_update, name="event_update"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
