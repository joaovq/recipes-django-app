import datetime
from django.test import TestCase
from app.models import Category, Recipes
from django.contrib.auth.models import User

class RecipeMixin:
    def make_recipe(
        self,
        title='My name Recipe',
        description='My Description',
        slug='my-name-recipe',
        num_preparations=5,
        num_servings=4,
        preparation_time=5,
        preparation_steps='dasdfdds',
        preparation_steps_is_html=False,
        is_published=True,
        preparation_time_unit = 'Minutes',
        servings_unit ='dd',
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        category=None,
        author=None,
    ) -> Recipes:
        if category is None:
            category = {}
        if author is None:
            author = {}
        return Recipes.objects.create(
            title=title,
            description=description,
            slug=slug,
            num_preparations=num_preparations,
            num_servings=num_servings,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            servings_unit=servings_unit,
            created_at=created_at,
            updated_at=updated_at,
            category=self.make_category(**category),
            author=self.make_author(**author),
        )

    def make_category(self, name='Category') -> Category:
        return Category.objects.create(categoryName=name)

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@gmail.com'
    ) -> User:
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )
        
    def make_recipe_in_batch(self, qtd = 10):
        recipes = []
        for i in range(qtd):
            needed_title = 'My new recipe in page'    
            recipe = self.make_recipe(
                title=needed_title,
                author={'username':f'joaovq{i}'},
                slug=f'{needed_title}{i}',
                is_published=True
            )
            recipes.append(recipe)
        return recipes

class RecipeTestBase(RecipeMixin,TestCase):
    ...