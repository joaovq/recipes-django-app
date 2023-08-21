from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
