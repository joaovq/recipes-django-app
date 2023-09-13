from django.test import TestCase
from django.urls import resolve,reverse
from app import views
from .test_recipe_base import RecipeTestBase
# from unittest import skip
 

# install pytest watch for run all test's 
# @skip('mensagem') para pular os testes               
class RecipeSearchViewTest(RecipeTestBase):    
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('app:search_recipes')
        resolved = resolve(url)
        self.assertIs(resolved.func.view_class, views.RecipeSearchView)
    def test_recipe_search_loads_correct_template(self):
       response =  self.client.get(reverse('app:search_recipes')+'?search=fsd') 
       self.assertTemplateUsed(response=response,template_name= 'recipes/pages/recipes_search.html')    
    def test_recipe_search_view_returns_404_not_found_term(self):
        response = self.client.get(
            reverse('app:search_recipes')
        )
        self.assertEqual(response.status_code, 404)     
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('app:search_recipes')+ '?search=Teste'
        response = self.client.get(url)   
        self.assertIn(
            'Search Results for &quot;Teste&quot;',
            response.content.decode('utf-8')
        )       
    def test_recipe_search_term_is_filter_is_correct_in_view_template(self):
        title = 'This is recipe one'
        title2 = 'This is recipe two'
        
        recipe1 = self.make_recipe(
            slug = 'this-one',
            title= title,
            author= {'username':'dffds'}            
        )  
        
        recipe2 = self.make_recipe(
            slug = 'this-2',
            title= title2,
            author= {'username':'tof'}            
        )    
        
        url = reverse('app:search_recipes')+ f'?search={title}'
        response = self.client.get(url)
        url2 = reverse('app:search_recipes')+ f'?search={title2}'
        response2 = self.client.get(url2)   
        response_both = self.client.get( reverse('app:search_recipes')+ f'?search=this')
        
        self.assertIn(
            recipe1,
            response.context['recipes']
        )
        self.assertNotIn(
            recipe2,
            response.context['recipes']
        )    
          
        self.assertIn(
            recipe2,
            response2.context['recipes']
        )    
        self.assertNotIn(
            recipe1,
            response2.context['recipes']
        )   
        
        self.assertIn(
            recipe2,
            response_both.context['recipes']
        )    
        self.assertIn(
            recipe1,
            response_both.context['recipes']
        )           
        
                             