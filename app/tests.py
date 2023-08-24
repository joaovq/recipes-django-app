from django.test import TestCase
from django.urls import resolve, reverse 
from app import views

# install pytest watch for run all test's

# Create your tests here.
class RecipesURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        home_url = reverse('app:home_recipes')
        self.assertEqual(home_url,'/', 'url not equals in view')     
        
    def test_recipes_details_url_is_correct(self):
        recipes_url = reverse('app:recipe_details', kwargs= {'recipe_id':1})
        self.assertEqual(recipes_url,'/recipes/1/', 'url not equals in view') 
        
    def test_recipes_category_url_is_correct(self):
        recipes_url = reverse('app:category_recipes', kwargs= {'category_id':1})
        self.assertEqual(recipes_url,'/recipes/category/1/', 'url not equals in view')     
            
      
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