from django import forms

from utils.django_forms import add_placeholder


class LoginAuthorForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'johndoe54')
        add_placeholder(self.fields['password'], '********')

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        label='Username',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        label='Password',
    )
