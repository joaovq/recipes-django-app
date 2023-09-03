from unittest import TestCase
from author.forms import RegisterForm 
from parameterized import parameterized

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            ('first_name','John e.'),
            ('last_name','Doe'),
            ('email','example@host.com'),
            ('username', 'johndoe54'),
            ('password','********** Coloque sua senha'),
        ]
    )
    def test_author_register_placeholder_is_correct(self, field_name, placeholder_value):
        form = RegisterForm()
        placeholder = form[field_name].field.widget.attrs['placeholder']
        self.assertEqual(placeholder_value, placeholder)
    
    @parameterized.expand(
        [
            ('first_name','Required. 30 characters or fewer.'),
            ('last_name','Required. 30 characters or fewer.'),
            ('email','Required. A valid email address.'),
            ('username', 'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        ]
    )    
    def test_author_register_help_text_is_correct(self, field_name, help_text_value):
        form = RegisterForm()
        help_text = form[field_name].field.help_text
        self.assertEqual(help_text_value, help_text)
        
    @parameterized.expand(
        [
            ('first_name','First Name'),
            ('last_name','Last Name'),
            ('email','E-mail'),
            ('username', 'Username'),
            ('password', 'Password'),
        ]
    )    
    def test_author_register_label_is_correct(self, field_name, label_value):
        form = RegisterForm()
        label = form[field_name].field.label
        self.assertEqual(label_value, label)    