from django.urls import path
from rest_framework.routers import SimpleRouter
from app import views
from .views import api
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'app'

recipe_api_v2_route = SimpleRouter()
recipe_api_v2_route.register(
    prefix='recipes/api/v2',
    viewset=api.RecipeApiv2ViewSet,
    basename='recipes-api'
)

# Se não tivesse nenhuma outra url
# urlpatterns  =  recipe_api_v2_route.urls

urlpatterns = [
    path('',views.RecipeHomeView.as_view(), name='home'),
    path('recipes/search/',view=views.RecipeSearchView.as_view(), name='search_recipes'),
    path('recipes/tags/<slug:slug>',view=views.RecipeTagView.as_view(), name='tag_recipes'),
    path('recipes/api/v1/',view=views.RecipeHomeViewApi.as_view(), name='recipes_api_v1'),
    path('recipes/api/v1/<int:recipe_id>/',views.RecipeDetailsViewApi.as_view(), name='recipe_details_api'),
    path('recipes/<int:recipe_id>/',views.RecipeDetailsView.as_view(), name='recipe_details'),
    path('recipes/category/<int:category_id>/',views.RecipeCategoryRecipeView.as_view(), name='category_recipes'),
    # path('recipes/api/v2/', api.RecipeApiv2ViewSet.as_view({
    #     'get':'list',
    #     'post': 'create'
    # })),
    # path('recipes/api/v2/<pk>/', api.RecipeApiv2ViewSet.as_view({
    #     'get':'retrieve',
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # })),
    path('recipes/api/v2/tag/<pk>/', api.tag_api_details, name='tag_api_detail'),
    # Pode fazer assim para incluir
    # path('recipes/api/v2', include(recipe_api_v2_route.urls))
    path('recipes/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('recipes/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('recipes/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# Pode fazer assim para incluir
urlpatterns += recipe_api_v2_route.urls