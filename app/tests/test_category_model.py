from django.core.exceptions import ValidationError

from app.tests.test_recipe_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name= 'Category Testing'
        )        
        return super().setUp()
    def test_recipe_category_model_string_representation_is_correct_return(self):
        self.assertEqual(
            str(self.category),
            self.category.categoryName      
        )
        
    def test_recipe_category_model_name_max_length_upper_65_char(self):
        self.category.categoryName = 'A' * 70
        with self.assertRaises(ValidationError):    
            self.category.full_clean() 