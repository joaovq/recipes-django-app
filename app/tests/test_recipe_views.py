from django.test import TestCase
from django.urls import resolve, reverse 
from app import views

# install pytest watch for run all test's                 
class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse('app:home_recipes')
        ) 
        self.assertIs(view.func, views.home_view)
    def test_recipe_details_view_function_is_correct(self):
        view = resolve(
            reverse('app:recipe_details',kwargs= {'recipe_id':1})
        ) 
        self.assertIs(view.func, views.recipe_details_view)  
    def test_recipe_category_recipe_view_function_is_correct(self):
        view = resolve(
            reverse('app:category_recipes',kwargs= {'category_id':1})
        ) 
        self.assertIs(view.func, views.categories_recipes_view)  