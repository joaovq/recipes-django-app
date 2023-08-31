from django.urls import path

from app import views

app_name = 'app'

urlpatterns = [
    path('',views.home_view, name='home'),
    path('recipes/search/',view=views.search_recipes_view, name='search_recipes'),
    path('recipes/<int:recipe_id>/',views.recipe_details_view, name='recipe_details'),
    path('recipes/category/<int:category_id>/',views.categories_recipes_view, name='category_recipes'),
]
