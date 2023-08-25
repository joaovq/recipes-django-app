from django.test import TestCase
from django.urls import resolve,reverse
from app import views
from app.models import Category, Recipes
from django.contrib.auth.models import User

from .test_recipe_base import RecipeTestBase
 

# install pytest watch for run all test's                 
class RecipeViewsTest(RecipeTestBase):
    def tearDown(self) -> None:
        return super().tearDown()    
    
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse('app:home')
        ) 
        self.assertIs(view.func, views.home_view)
        
    def test_recipe_details_view_function_is_correct(self):
        view = resolve(
            reverse('app:recipe_details',kwargs= {'recipe_id':1})
        ) 
        self.assertIs(view.func, views.recipe_details_view) 
        
    def test_recipe_home_view_get_status_200_OK(self):
        home_path = reverse('app:home')
        response = self.client.get(path = home_path)  
        self.assertEqual(response.status_code, 200)    
         
    def test_recipe_home_view_loads_correct_template(self):  
        response = self.client.get(reverse('app:home')) 
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
        
    def test_not_found_recipes_state(self):
        Recipes.objects.filter(pk=1).delete()
        response = self.client.get(reverse('app:home'))   
        content_string =  response.content.decode('utf-8')
        self.assertIn('No Recipe Found here',content_string) 
        
    def test_recipe_home_template_shows_recipes_found_assert_title(self):    
        response = self.client.get(reverse('app:home'))
        response_recipes = response.context['recipes']  
        content_recipes_home = response.content.decode('utf-8')
        
        self.assertEqual(response_recipes.first().name, 'My name Recipe')
        self.assertIn('My name Recipe',content_recipes_home)   
        self.assertIn('My Description',content_recipes_home)     
        self.assertEqual(len(response_recipes),1)                                  
                
    def test_recipe_category_recipe_view_function_is_correct(self):
        Recipes.objects.filter(pk=1).delete()    
        view = resolve(
            reverse('app:category_recipes',kwargs= {'category_id':1})
        ) 
        self.assertIs(view.func, views.categories_recipes_view)  
        
    def test_recipe_category_returns_404_not_found_category(self):
        response = self.client.get(
            reverse('app:category_recipes',kwargs= {'category_id':2000})
        )
        self.assertEqual(response.status_code, 404)  
          
    def test_recipe_details_view_returns_404_not_found_category(self):
        response = self.client.get(
            reverse('app:recipe_details',kwargs= {'recipe_id':2000})
        )
        self.assertEqual(response.status_code, 404)    
        
    def test_force_fail_for_remember(self):
        self.fail('Induzindo a falha por que não fiz esse teste')                  