from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

app_name = 'author'

author_api_router = SimpleRouter()
author_api_router.register('api', views.AuthorViewSet, basename='author-api')

urlpatterns = [
    path('register/', views.register_view, name= 'register_author'),
    path('create/', views.register_create, name= 'register_success'),
    path('login/',view=views.login_view, name='login'),
    path("login/success", view=views.login_create, name="login_success"),
    path("login/logout", view=views.logout_view, name="logout"),
    path("dashboard", view=views.dashboard_view, name="dashboard"),
    path("dashboard/create", view=views.DashboardRecipeView.as_view(), name="dashboard_create"),
    path("dashboard/<int:id>/delete", view=views.DashboardDeleteView.as_view(), name="dashboard_delete"),
    path(
        "dashboard/<int:id>/edit",
        view=views.DashboardRecipeView.as_view(),
        name="dashboard_recipe_edit"
    ),
    path(
        "profile/<int:id>/",
        view=views.ProfileView.as_view(),
        name="profile"
    ),
]

urlpatterns += author_api_router.urls
