from django.urls import path
from . import admin
from . import views

app_name = 'author'

urlpatterns = [
    path('register/', views.register_view, name= 'register_author'),
    path('create/', views.register_create, name= 'register_success'),
]
