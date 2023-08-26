from django.test import TestCase
from django.urls import resolve,reverse
from app import views
from app.models import Category, Recipes
from django.contrib.auth.models import User
from .test_recipe_base import RecipeTestBase
from utils.recipes import constants
# from unittest import skip
 

# install pytest watch for run all test's 
# @skip('mensagem') para pular os testes               
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
        self.assertIn(constants.RECIPES_NOT_FOUND_MESSAGE,content_string) 
        
    def test_recipe_home_template_shows_recipes_found_assert_title(self):  
        self.make_recipe(title='My name Recipe')  
        response = self.client.get(reverse('app:home'))
        response_recipes = response.context['recipes']  
        content_recipes_home = response.content.decode('utf-8')
        
        self.assertEqual(response_recipes.first().title, 'My name Recipe')
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
        
    def test_recipe_category_returns_404_not_found_recipes(self):
        Recipes.objects.filter(pk=1).delete()
        recipe = self.make_recipe(author={'username':'joaovq'}, is_published=False)
        response = self.client.get(
            reverse('app:category_recipes',kwargs= {'category_id':recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)  
          
    def test_recipe_details_view_returns_404_not_found_recipe(self):
        response = self.client.get(
            reverse('app:recipe_details',kwargs= {'recipe_id':2000})
        )
        self.assertEqual(response.status_code, 404) 
        
    def test_recipe_details_view_returns_404_not_found_recipe(self):
        Recipes.objects.filter(pk=1).delete()
        recipe = self.make_recipe(author={'username':'joaovq'}, is_published=False)
        response = self.client.get(
            reverse('app:recipe_details',kwargs= {'recipe_id':recipe.id})
        )
        self.assertEqual(response.status_code, 404) 
          
    def test_category_recipes_view_returns_recipe_with_title_is_correct(self):
        needed_title = 'My Test category recipe'
        self.make_recipe(category={'name': needed_title}, author={'username':'joaovq'})
        response = self.client.get(
            reverse('app:category_recipes',kwargs= {'category_id':1})
        )
        content_recipes_page = response.content.decode('utf-8')
        self.assertIn(needed_title,content_recipes_page)
        
    def test_recipe_details_view_returns_recipe_with_title_is_correct(self):
        self.make_recipe()
        needed_title = 'My recipe details test'
        self.make_recipe(title=needed_title,author={'username':'joaovq'})
        response = self.client.get(
            reverse('app:recipe_details',kwargs= {'recipe_id':2})
        )
        content_recipes_page = response.content.decode('utf-8')
        self.assertIn(needed_title,content_recipes_page)  
        
    def test_recipe_details_view_returns_recipe_with_title_is_correct(self):
        needed_first_name = 'Cardoso'
        self.make_recipe(author={'username':'joaovq', 'first_name': needed_first_name})
        response = self.client.get(
            reverse('app:recipe_details',kwargs= {'recipe_id':1})
        )
        content_recipes_page = response.content.decode('utf-8')
        self.assertIn(needed_first_name,content_recipes_page)
        
    def test_recipe_home_view_is_displayed_recipes_is_published_correct(self):
        """Test recipes is_published False don't show"""
        needed_title = 'My new recipe is not published'
        Recipes.objects.filter(pk=1).delete()
        self.make_recipe(title=needed_title,author={'username':'joaovq'}, is_published=False)
        response = self.client.get(
            reverse('app:home')
        )
        template_content_home = response.content.decode('utf-8')
        self.assertIn(constants.RECIPES_NOT_FOUND_MESSAGE,template_content_home)                    