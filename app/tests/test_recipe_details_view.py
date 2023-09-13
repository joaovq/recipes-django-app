from django.urls import resolve, reverse
from app import views
from app.models import Recipes
from app.tests.test_recipe_base import RecipeTestBase


class RecipeDetailsViewTest(RecipeTestBase):
    def test_recipe_details_view_function_is_correct(self):
        view = resolve(
            reverse('app:recipe_details',kwargs= {'recipe_id':1})
        ) 
        self.assertIs(view.func.view_class, views.RecipeDetailsView) 
        
                                    
                
   
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
        
   