from .base import AuthorBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AuthorFunctionalRegisterTest(AuthorBaseTest):
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            'html/body/div[2]/form'
        )    
        
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(
            By.TAG_NAME, 
            'input'
        )
        for field in fields:
            if field.is_displayed():    
                field.send_keys(' '*20)
        email = form.find_element(value='id_email')
        email.send_keys('dummy@email.com')
        
    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url+'/author/register/')
        form = self.get_form()        
        self.fill_form_dummy_data(form)
        
        callback(form)
        return form
    
    def test_empty_first_name_show_error_message(self):
        def first_name_field_callback(form):
            first_name_field = self.get_by_placeholder(
                form, 'John e.'
            )
            first_name_field.send_keys('  ')
            first_name_field.send_keys(Keys.ENTER)
            # Quando manda o form, a pagina recarrega e os elementos que estão na pagina são novos
            # Então é preciso reselecionar os elementos para fazer asserts  

            form = self.get_form()
                    
            self.assertIn('This field is required', form.text)
            
        self.form_field_test_with_callback(callback=first_name_field_callback)
        
    def test_empty_last_name_show_error_message(self):
        def last_name_field_callback(form):
            last_name_field = self.get_by_placeholder(
                form, 'Doe'
            )
            last_name_field.send_keys('  ')
            last_name_field.send_keys(Keys.ENTER)
            # Quando manda o form, a pagina recarrega e os elementos que estão na pagina são novos
            # Então é preciso reselecionar os elementos para fazer asserts  

            form = self.get_form()
                    
            self.assertIn('This field is required', form.text)
            
        self.form_field_test_with_callback(callback=last_name_field_callback)
    def test_empty_username_show_error_message(self):
        def username_field_callback(form):
            username_field = self.get_by_placeholder(
                form, 'johndoe54'
            )
            username_field.send_keys('  ')
            username_field.send_keys(Keys.ENTER)
            # Quando manda o form, a pagina recarrega e os elementos que estão na pagina são novos
            # Então é preciso reselecionar os elementos para fazer asserts  

            form = self.get_form()
                    
            self.assertIn('This field is required', form.text)
            
        self.form_field_test_with_callback(callback=username_field_callback)
        
    def test_invalid_email_show_error_message(self):
        def email_field_callback(form):
            email_field = self.get_by_placeholder(
                form, 'example@host.com'
            )
            email_field.clear()
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            # Quando manda o form, a pagina recarrega e os elementos que estão na pagina são novos
            # Então é preciso reselecionar os elementos para fazer asserts  

            form = self.get_form()
                    
            self.assertIn('Informe um endereço de email válido', form.text)
            
        self.form_field_test_with_callback(callback=email_field_callback)
        
    def test_invalid_confirmation_password_show_error_message(self):
        def password_callback(form):
            password = self.get_by_placeholder(
                form, '********** Coloque sua senha'
            )
            password2 = self.get_by_placeholder(
                form, '**********'
            )
            password.clear()
            password2.clear()
            password.send_keys('Pad@dshfg5454')
            password2.send_keys('Pad@dshfgdasdsa1454')
            password.send_keys(Keys.ENTER)
            # Quando manda o form, a pagina recarrega e os elementos que estão na pagina são novos
            # Então é preciso reselecionar os elementos para fazer asserts  

            form = self.get_form()
            
            self.assertIn('Password and password2 must be equal', form.text)
            
        self.form_field_test_with_callback(callback=password_callback)
        
    def test_valid_data_user_succesfully_response(self):
        self.browser.get(self.live_server_url+'/author/register/')
        form = self.get_form()        
        
        self.get_by_placeholder(form, 'John e.').send_keys('First Name')
        self.get_by_placeholder(form, 'Doe').send_keys('Last Name')
        self.get_by_placeholder(form, 'johndoe54').send_keys('myusername')
        self.get_by_placeholder(form, 'example@host.com').send_keys('youremail@valid.com')
        self.get_by_placeholder(form, '********** Coloque sua senha').send_keys('P@sswordValid123')
        self.get_by_placeholder(form, '**********').send_keys('P@sswordValid123')
        
        form.submit()
        
        self.sleep()
        
        self.assertIn(
            'Your user is created, please log in',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )