from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('', TemplateView.as_view(template_name='main/home.html'), name='home'),
]
