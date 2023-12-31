import time
from utils.browser import make_chrome_browser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from app.tests.test_recipe_base import RecipeMixin


class RecipeBaseFunctionalTest(RecipeMixin,StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp() 
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self, seconds = 2):
        time.sleep(seconds)  