from os import name
from django.contrib import admin
from django.urls import path, include

from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('regex-patterns/', views.list_regex_results, name='regex-form'),
]
