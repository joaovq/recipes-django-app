from django.urls import resolve, reverse
from app import views
from app.models import Recipes
from app.tests.test_recipe_base import RecipeTestBase
from utils.recipes import constants
from parameterized import parameterized


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse('app:home')
        ) 
        self.assertIs(view.func, views.home_view)
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
        
        self.assertEqual(response_recipes[0].title, 'My name Recipe')
        self.assertIn('My name Recipe',content_recipes_home)   
        self.assertIn('My Description',content_recipes_home)     
        self.assertEqual(len(response_recipes),1)  
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
    def test_recipe_home_view_is_displayed_items_per_page_is_correct(self):
        """Test recipes is_published False don't show"""
        Recipes.objects.filter(pk=1).delete()
        for i in range(1,11):
            needed_title = 'My new recipe in page'    
            self.make_recipe(
                title=needed_title,
                author={'username':f'joaovq{i}'},
                slug=f'{needed_title}{i}',
                is_published=True
            )
        response = self.client.get(
            reverse('app:home')
        )
        recipes_in_page = response.context['recipes']
        self.assertEqual(len(recipes_in_page), 10)
        
    @parameterized.expand(
        [
            'g',
            'f',
            '',
            '^',
            '     ',
        ]
    )    
    def test_recipe_home_view_page_parameter_is_not_valid_value_int_returns_initial_page(self, invalid_argument_page):        
        response = self.client.get(
            reverse('app:home')+f'?page={invalid_argument_page}'
        )
        pagination_range = response.context['pagination_range']
        self.assertEqual(pagination_range['current_page'], 1)
        