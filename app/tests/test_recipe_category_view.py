from django.urls import resolve, reverse
from app import views
from app.models import Recipes
from app.tests.test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
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
    def test_category_recipes_view_returns_recipe_with_title_is_correct(self):
        needed_title = 'My Test category recipe'
        self.make_recipe(category={'name': needed_title}, author={'username':'joaovq'})
        response = self.client.get(
            reverse('app:category_recipes',kwargs= {'category_id':1})
        )
        content_recipes_page = response.content.decode('utf-8')
        self.assertIn(needed_title,content_recipes_page)
                