from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView

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
]
