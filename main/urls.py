from django.contrib import admin
from django.urls import path, include
from . import views

# To reference the app, e.g. in django.shortcuts.redirect('main:homepage')
app_name = 'main'

urlpatterns = [
    path('', views.homepage, name="homepage")
]
