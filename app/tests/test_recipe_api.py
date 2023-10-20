from unittest.mock import patch
from django.urls import reverse
from rest_framework import test
from app.tests.test_recipe_base import RecipeMixin


class RecipeAPIv2TestMixin(RecipeMixin):
    def get_recipe_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('app:recipes-api-list')
        return api_url
    
    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_reverse_url(reverse_result)
        response = self.client.get(api_url)
        return response
    
    def get_auth_data(self, username='user', password='pass'):
        userdata = {
            'username': username,
            'password': password,
        }
        user = self.make_author(
            username=userdata.get('username'),
            password=userdata.get('password')
        )
        response = self.client.post(
            reverse('app:token_obtain_pair'), data={**userdata}
        )
        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user,
        }
    
    def get_recipe_raw_data(self):
        return {
            "title": "Torta de morango",
            "description": "My Description",
            "preparation": "5 Minutes",
            "num_preparations": 5,
            "num_servings": 5,
            "preparation_time": 5,
            "preparation_time_unit": "Minutes",
            "servings_unit": "dd",
            "preparation_steps": "dasdfdds"
        }

class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2TestMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(
            response.status_code,
            200
        )
    @patch('app.views.api.RecipeAPIV2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(qtd=wanted_number_of_recipes)

        response = self.client.get(
            reverse('app:recipes-api-list') + '?page=1'
        )
        qtd_of_loaded_recipes = len(response.data.get('results'))

        self.assertEqual(
            wanted_number_of_recipes,
            qtd_of_loaded_recipes
        )
    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(
            len(response.data.get('results')),
            1
        )
        
    @patch('app.views.api.RecipeAPIV2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        # Creates categories
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')

        # Creates 10 recipes
        recipes = self.make_recipe_in_batch(qtd=10)

        # Change all recipes to the wanted category
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        # Change one recipe to the NOT wanted category
        # As a result, this recipe should NOT show in the page
        recipes[0].category = category_not_wanted
        recipes[0].save()

        # Action: get recipes by wanted category_id
        api_url = reverse('app:recipes-api-list') + \
            f'?category_id={category_wanted.id}'
        response = self.get_recipe_api_list(reverse_result=api_url)

        # We should only see recipes from the wanted category
        self.assertEqual(
            len(response.data.get('results')),
            9
        )

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code,
            401
        )
    # def test_jwt_login(self):
    #     print(self.get_jwt_access_token())
        
    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        data = self.get_recipe_raw_data()
        response = self.client.post(
            self.get_recipe_reverse_url(),
            data=data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_auth_data().get('jwt_access_token')}"
        )
        self.assertEqual(
            response.status_code,
            201
        )
        
    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        # Arrange (config do test)
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')
        jwt_access_token = access_data.get('jwt_access_token')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()

        wanted_new_title = f'The new title updated by {author.username}'

        # Action (Ação)
        response = self.client.patch(
            reverse('app:recipes-api-detail', args=(recipe.id,)),
            data={
                'title': wanted_new_title
            },
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )

        # Assertion (Afirmação)
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            response.data.get('title'),
            wanted_new_title,
        )

    def test_recipe_api_list_logged_user_cant_update_a_recipe_owned_by_another_user(self):  # noqa
        # Arrange (config do test)
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')

        # This user cannot update the recipe because it is owned by another
        # user.
        another_user = self.get_auth_data(username='cant_update')
        jwt_access_token_from_another_user = another_user.get(
            'jwt_access_token'
        )

        # This is the actual owner of the recipe
        author = access_data.get('user')
        recipe.author = author
        recipe.save()

        # Action (Ação)
        response = self.client.patch(
            reverse('app:recipes-api-detail', args=(recipe.id,)),
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token_from_another_user}'
        )

        # Assertion (Afirmação)
        # Another user cannot update the recipe, so the status code
        # must be 403 Forbidden
        self.assertEqual(
            response.status_code,
            403,
        )