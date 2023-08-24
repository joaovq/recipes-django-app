from django.test import TestCase
from django.urls import resolve,reverse
from app import views

# install pytest watch for run all test's                 
class RecipeViewsTest(TestCase):
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
    def test_recipe_category_recipe_view_function_is_correct(self):
        view = resolve(
            reverse('app:category_recipes',kwargs= {'category_id':1})
        ) 
        self.assertIs(view.func, views.categories_recipes_view)
        
    def test_recipe_home_view_get_status_200_OK(self):
        home_path = reverse('app:home')
        response = self.client.get(path = home_path)  
        self.assertEqual(response.status_code, 200)    
         
    def test_recipe_home_view_loads_correct_template(self):  
        response = self.client.get(reverse('app:home')) 
        self.assertTemplateUsed(response, 'recipes/pages/home.html')      