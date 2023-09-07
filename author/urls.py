from django.urls import path
from . import views

app_name = 'author'

urlpatterns = [
    path('register/', views.register_view, name= 'register_author'),
    path('create/', views.register_create, name= 'register_success'),
    path('login/',view=views.login_view, name='login_author'),
    path("login/success", view=views.login_create, name="login_success"),
    path("login/logout", view=views.logout_view, name="logout"),
]
