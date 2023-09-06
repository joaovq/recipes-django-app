from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from author.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            ('first_name', 'John e.'),
            ('last_name', 'Doe'),
            ('email', 'example@host.com'),
            ('username', 'johndoe54'),
            ('password', '********** Coloque sua senha'),
        ]
    )
    def test_author_register_placeholder_is_correct(self, field_name, placeholder_value):
        form = RegisterForm()
        placeholder = form[field_name].field.widget.attrs['placeholder']
        self.assertEqual(placeholder_value, placeholder)

    @parameterized.expand(
        [
            ('first_name', 'Required. 30 characters or fewer.'),
            ('last_name', 'Required. 30 characters or fewer.'),
            ('email', 'Required. A valid email address.'),
            ('username', 'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        ]
    )
    def test_author_register_help_text_is_correct(self, field_name, help_text_value):
        form = RegisterForm()
        help_text = form[field_name].field.help_text
        self.assertEqual(help_text_value, help_text)

    @parameterized.expand(
        [
            ('first_name', 'First Name'),
            ('last_name', 'Last Name'),
            ('email', 'E-mail'),
            ('username', 'Username'),
            ('password', 'Password'),
        ]
    )
    def test_author_register_label_is_correct(self, field_name, label_value):
        form = RegisterForm()
        label = form[field_name].field.label
        self.assertEqual(label_value, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'email@gmail.com',
            'password': 'Strongpassword123456',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand(
        [
            ('username', 'This field is required'),
            ('first_name', 'This field is required'),
            ('last_name', 'This field is required'),
            ('password', 'This field is required'),
            ('email', 'Email is required'),
        ]
    )
    def test_cannot_be_empty(self, field, message_error):
        self.form_data[field] = ''
        url = reverse('author:register_success')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(message_error, response.content.decode('utf-8'))

    def test_username_min_length_should_be_least_4_chars(self):
        self.form_data['username'] = 'u'
        url = reverse('author:register_success')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have at least 4 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_length_should_be_less_150_chars(self):
        self.form_data['username'] = 'u'*151
        url = reverse('author:register_success')
        # O atributo follow segue a  página se ela for redirecionada
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = "Your username must be at least 150 character long."
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'ufds7Ffdds'
        url = reverse('author:register_success')
        # O atributo follow segue a  página se ela for redirecionada
        response = self.client.post(url, data=self.form_data, follow=True)
        msg =('Password must have at least one uppercase letter, '
        'one lowercase letter and one number. The length should be '
        'at least 8 characters.')
        self.assertNotIn(msg, response.content.decode('utf-8'))
        
    def test_password_not_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'ufdsfdds'
        url = reverse('author:register_success')
        # O atributo follow segue a  página se ela for redirecionada
        response = self.client.post(url, data=self.form_data, follow=True)
        msg =('Password must have at least one uppercase letter, '
        'one lowercase letter and one number. The length should be '
        'at least 8 characters.')
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
         
    def test_password_not_equal_password2(self):
        self.form_data['password'] = 'ufdSfdds@4445'
        self.form_data['password2'] = 'ufdSfdds@4442'
        url = reverse('author:register_success')
        # O atributo follow segue a  página se ela for redirecionada
        response = self.client.post(url, data=self.form_data, follow=True)
        msg ='Password and password2 must be equal'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password')) 
          
    def test_password_equals_and_corrects_password2(self):
        self.form_data['password'] = 'ufdSfdds@4445'
        self.form_data['password2'] = 'ufdSfdds@4445'
        url = reverse('author:register_success')
        # O atributo follow segue a  página se ela for redirecionada
        response = self.client.post(url, data=self.form_data, follow=True)
        msg ='Password and password2 must be equal'
        self.assertNotIn(msg, response.content.decode('utf-8'))         
