# Para importar os arquivos staticos no live server utilizamos o StaticLiverServerTestCase
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest
# Importando o LiveServerTestCase, você não vai subir o css (static files)  
# from django.test import LiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from unittest.mock import patch

@pytest.mark.functional_test
# pytest -m 'functional_test' -rP para executar os tests com essa marker
# pytest -m 'not functional_test' -rP para executar os tests que não tem essa marker (coloca o not na frente)
# pytest -k "test_recipe_home_page_not_recipes_found_message_is_present" para executar um test especifico
class RecipeHomePageFunctionalTestCase(RecipeBaseFunctionalTest):
    def test_recipe_home_page_not_recipes_found_message_is_present(self):
        self.browser.get(self.live_server_url)    
        body = self.browser.find_element(by=By.TAG_NAME, value='body')
        self.assertIn('No Recipe Found here!', body.text)
        self.browser.quit()
    @patch('app.views.PER_PAGE', new=2)
    def test_recipe_search_can_recipe_found_recipes_is_correct(self):
        recipes = self.make_recipe_in_batch(qtd=15)
        self.browser.get(self.live_server_url)
        
        title_needed = 'This is title needed'
        recipes[0].title = title_needed
        recipes[0].save()
        
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search recipes"]'
        )     
        
        search_input.send_keys(title_needed)   
        search_input.send_keys(Keys.ENTER)
        
        self.assertIn(title_needed, self.browser.find_element(By.CLASS_NAME, 'main-content').text)   
                
    @patch('app.views.PER_PAGE', new=2)
    def test_recipe_pagination_click_on_page(self):
        self.make_recipe_in_batch()
        
        self.browser.get(self.live_server_url)
        
        pagination = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        
        pagination.click()
        
        self.assertEqual(len(self.browser.find_elements(By.CLASS_NAME, 'card-recipe-container')),2)            