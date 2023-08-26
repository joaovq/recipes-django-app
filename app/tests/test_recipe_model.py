import datetime
from django.core.exceptions import ValidationError
from app.models import Recipes
from app.tests.test_recipe_base import RecipeTestBase
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_default(self):
        return Recipes(
            title='title',
            description='description',
            slug='slug',
            num_preparations=5,
            num_servings=5,
            preparation_time=5,
            preparation_time_unit='Minutes',
            preparation_steps='preparation_steps',
            servings_unit='servings_unit',
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            category=self.make_category(name='category default'),
            author=self.make_author(username='joadfsfdguhfg'),
        )
    
    # Test without parameterized
    def test_create_recipe_raises_error_if_name_has_more_than_60_chars(self):
        self.recipe.title = "A" * 61
        with self.assertRaises(ValidationError):
            self.recipe.full_clean() # AQUI A VALIDAÇÃO OCORRE
            
    @parameterized.expand(
        [
            ('title', 60),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ]
    )
    # This repeat test and create sub test's for each parameter
    def test_recipe_fields_max_length(self, field, max_length):
        # Sub testes
        """
        fields = [
            ('title', 60),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ]        
        for field, max_length in fields:
            # Context manager do python, como uma lambda function do kotlin, ou Runnable do Java
            with self.subTest(field=field, max_length=max_length):
                setattr(self.recipe,field, 'A' * (max_length + 1))
                with self.assertRaises(ValidationError):
                        self.recipe.full_clean() # AQUI A VALIDAÇÃO OCORRE
        """
        # parameterized      
        setattr(self.recipe,field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()    
        recipe.full_clean()
        recipe.save()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            'Recipe preparation_steps_is_html is not false'
        )
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()    
        recipe.full_clean()
        recipe.save()
        self.assertFalse(
            recipe.is_published,
            'Recipe preparation_steps_is_html is not false'
        )    