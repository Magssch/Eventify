from django.contrib import admin
from django.urls import path, include
from main.views import event_info, events

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('account/', include('django.contrib.auth.urls')),
]
