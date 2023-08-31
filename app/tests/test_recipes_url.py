from django.test import TestCase
from django.urls import reverse

# install pytest watch for run all test's 
class RecipesURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        home_url = reverse('app:home')
        self.assertEqual(home_url,'/', 'url not equals in view')     
        
    def test_recipes_details_url_is_correct(self):
        recipes_url = reverse('app:recipe_details', kwargs= {'recipe_id':1})
        self.assertEqual(recipes_url,'/recipes/1/', 'url not equals in view') 
        
    def test_recipes_category_url_is_correct(self):
        recipes_url = reverse('app:category_recipes', kwargs= {'category_id':1})
        self.assertEqual(recipes_url,'/recipes/category/1/', 'url not equals in view')
        
    def test_search_recipes_url_is_correct(self):
        search_recipes_url = reverse('app:search_recipes')
        self.assertEqual(search_recipes_url,'/recipes/search/', 'url not equals in view')        