import re
from django import forms
from django.contrib.auth.models import User


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, new_placeholder):
    add_attr(field, 'placeholder', new_placeholder)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise forms.ValidationError(
            ('Password must have at least one uppercase letter, '
             'one lowercase letter and one number. The length should be '
             'at least 8 characters.'),
            code='invalid',
        )


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['password'], 'Coloque sua senha')
        # require is equal True for default
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'John e.'}
        ),
        error_messages={
            'required': 'This field is required'
        },
        label='First Name',
        help_text='Required. 30 characters or fewer.'
    )
    username = forms.CharField(
        min_length=4,
        max_length=150,
        label='Username',
        help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={
            'required': 'This field is required',
            'unique': 'This username has already been taken.',
            'max_length': "Your username must be at least %(limit_value)d character long.",
            'invalid': 'This field is invalid',
            'min_length': 'Username must have at least 4 characters'
        },
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'johndoe54'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Doe'}
        ),
        error_messages={
            'required': 'This field is required'
        },
        label='Last Name',
        help_text='Required. 30 characters or fewer.'
    )
    email = forms.EmailField(
        required=True,
        label='E-mail',
        error_messages={
            'required': 'Email is required'
        },
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'example@host.com'}),
        help_text='Required. A valid email address.'
    )

    # A mesma coisa de utilizar a Meta, aqui sobrescrevemos
    # Se fizer isso, melhor sobrescrever tudo
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '**********'}
        ),
        error_messages={
            'required': 'This field is required'
        },
        help_text='',
        label='Password',
        # Lista de validadores
        validators=[strong_password]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '**********'}
        ),
        error_messages={
            'required': 'This field is required'
        },
        help_text='',
        label='Confirm Password',
        # Lista de validadores
        validators=[strong_password]
    )

    class Meta:
        model = User
        # Passa todos os atributos da classe '__all__'
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # exclude = ['first_name']
        # labels = {
        #     'username': 'Username',
        # }
        # help_texts = {
        #     'username': 'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.',
        #     'first_name': 'Required. 30 characters or fewer.',
        #     'last_name': 'Required. 30 characters or fewer.',
        # }
        # error_messages = {
        #     'username': {
        #         'required':'This field is required',
        #         'unique': 'This username has already been taken.',
        #         'max_length': "Your username must be at least %(limit_value)d character long.",
        #         'invalid': 'This field is invalid'
        #     }
        # }
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'johndoe54'}),
        # }

    # def clean_password(self):
    #     data = self.cleaned_data.get('password')

    #     if 'atenção' in data:
    #         raise forms.ValidationError(
    #             'Formulário inválido. Não digite %(value)s no campo',
    #             code='invalid',
    #             params={'value': ''}
    #         )

    #     return data

    # def clean_first_name(self):
    #     data = self.cleaned_data.get('first_name')

    #     if 'atenção' in data:
    #         raise forms.ValidationError(
    #             'Formulário inválido. Não digite %(value)s no campo',
    #             code='invalid',
    #             params={'value': ''}
    #         )

    #     return data

    # Caso não sobreescreva, podemos usar esses metodos
    def clean_username(self):
        data = self.cleaned_data.get('username')

        if len(data) < 4:
            raise forms.ValidationError(
                'Forms invalid. Username have %(value)s chars and should be upper than 4 chars',
                code='min_length',
                params={'value': len(data)}
            )

        return data

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if User.objects.filter(username=username).exists():
            self.add_error('username', 'This username has already been taken.')
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email', 'This email address has already been taken.')
        
        if password != password2:
            password_confirmation_error = forms.ValidationError(
                'Password and password2 must be equal',
                code='invalid'
            )
            raise forms.ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
