from django.urls import path

from app import views

app_name = 'app'

urlpatterns = [
    path('',views.RecipeHomeView.as_view(), name='home'),
    path('recipes/search/',view=views.RecipeSearchView.as_view(), name='search_recipes'),
    path('recipes/api/v1/',view=views.RecipeHomeViewApi.as_view(), name='recipes_api_v1'),
    path('recipes/api/v1/<int:recipe_id>/',views.RecipeDetailsViewApi.as_view(), name='recipe_details_api'),
    path('recipes/<int:recipe_id>/',views.RecipeDetailsView.as_view(), name='recipe_details'),
    path('recipes/category/<int:category_id>/',views.RecipeCategoryRecipeView.as_view(), name='category_recipes'),
]
