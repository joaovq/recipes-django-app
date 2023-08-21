from django.urls import path

from app import views


urlpatterns = [
    path('',views.home_view),
    path('about/',views.about_view),
    path('contact/',views.contact_view),
]
