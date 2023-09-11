from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthorLogoutTest(TestCase):
    def make_user_login(self):
        user = User.objects.create_user(username='my_user', password='mypass')
        self.client.login(username=user.username, password='mypass')
    def test_user_tries_to_logout_using_get_method(self):
        self.make_user_login()
        response = self.client.get(reverse('author:logout'), follow=True)
        self.assertIn('Invalid logout request',
                      response.content.decode('utf-8'))

    def test_user_tries_to_logout_using_post_method_with_user_invalid(self):
        self.make_user_login()
        response = self.client.post(
            path= reverse('author:logout'),
            data= {
                'username': 'userinvalid' 
            },
            follow=True
        )
        self.assertIn('Invalid user request', response.content.decode('utf-8'))
        
    def test_user_tries_to_logout_can_is_successfully(self):
        self.make_user_login()    
        response = self.client.post(
            path= reverse('author:logout'),
            data= {
                'username': 'my_user' 
            },
            follow=True
        )
        self.assertIn('You session was terminated', response.content.decode('utf-8'))    
