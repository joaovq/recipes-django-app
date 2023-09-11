from django.urls import reverse
from tests.functional_tests.author.base import AuthorBaseTest
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.mark.functional_test
class AuthorLoginFunctionalTest(AuthorBaseTest):
    def test_user_validate_data_login_completed(self):
        pass_not_encrypt = 'pass'
        user = User.objects.create_user(username='my_user',password= pass_not_encrypt)
        
        # Usuario abre a página
        self.browser.get(self.live_server_url + reverse('author:login'))
        
        # Usuario vê o formulário de login
        form = self.browser.find_element(by=By.ID,value='register-form-author')
        username_field = self.get_by_placeholder(form, 'johndoe54')
        password_field = self.get_by_placeholder(form, '********')
        
        # Usuario preenche o formulário
        username_field.send_keys(user.username)
        password_field.send_keys(pass_not_encrypt)
        # Envia o formulário
        form.submit()
        self.sleep()
        
        self.assertIn(        
            f'Dashboard ({user.username})',
            self.browser.find_element(by=By.TAG_NAME,value='body').text
        )    
        
    def test_login_if_not_POST_method_raise_404_not_found(self): 
        self.browser.get(self.live_server_url + reverse('author:login_success'))
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
    def test_login_form_is_invalid(self):
        # Usuário acessa a página de login
        self.browser.get(self.live_server_url + reverse('author:login'))
        #  Tenta enviar valores vazio
        form = self.browser.find_element(by=By.ID,value='register-form-author')
        username_field = self.get_by_placeholder(form, 'johndoe54')
        password_field = self.get_by_placeholder(form, '********')
        # Usuario preenche o formulário com valores vazios
        username_field.send_keys('       ')
        password_field.send_keys('   ')
        # Usuario envia o forms
        form.submit()
        # Espera a mensagem aparecer 
        self.sleep()
        self.assertIn(
            'Error to validate form data',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        
    def test_login_user_data_is_invalid_credentials(self):
        # Usuário acessa a página de login
        self.browser.get(self.live_server_url + reverse('author:login'))
        #  Tenta enviar valores vazio
        form = self.browser.find_element(by=By.ID,value='register-form-author')
        username_field = self.get_by_placeholder(form, 'johndoe54')
        password_field = self.get_by_placeholder(form, '********')
        # Usuario preenche o formulário com valores vazios
        username_field.send_keys('invaliduser')
        password_field.send_keys('invalidpasswordS4S@')
        # Usuario envia o forms
        form.submit()
        # Espera a mensagem aparecer 
        self.sleep()
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )    