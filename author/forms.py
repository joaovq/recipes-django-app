import re
from django import forms
from django.contrib.auth.models import User

def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name,'')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()
    
def add_placeholder(field, new_placeholder):
    add_attr(field,'placeholder', new_placeholder)
    
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
        add_placeholder(self.fields['password'],'Coloque sua senha')
    
    # A mesma coisa de utilizar a Meta, aqui sobrescrevemos 
    # Se fizer isso, melhor sobrescrever tudo
    password = forms.CharField(
        required= True,
        widget= forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':'**********'}
        ),
        error_messages = {
            
        },
        help_text = '',
        label='Password',
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
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
            
        }
        help_texts = {
            'username': 'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.',
            'first_name': 'Required. 30 characters or fewer.',
            'last_name': 'Required. 30 characters or fewer.',
            'email': 'Required. A valid email address.',
            
        }
        error_messages = {
            'username': {
                'required':'This field is required',
                'unique': 'This username has already been taken.',
                'max_length': "Your username must be at least %(limit_value)d character long.",
                'invalid': 'This field is invalid'
            },
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'johndoe54'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'John e.'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'example@host.com'}),
        }
        
    def clean_password(self):
        data = self.cleaned_data.get('password')
        
        if 'atenção' in data:
            raise forms.ValidationError(
                'Formulário inválido. Não digite %(value)s no campo',
                code='invalid',
                params={'value': ''} 
            )
        
        return data    
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        
        if 'atenção' in data:
            raise forms.ValidationError(
                'Formulário inválido. Não digite %(value)s no campo',
                code='invalid',
                params={'value': ''} 
            )
        
        return data
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'This username has already been taken.')
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'This email address has already been taken.')
        # if first_name and last_name:
        #     if first_name[0].isupper() and last_name[0].isupper():
        #         self.add_error('first_name', 'First Name must be lowercase')
        #         self.add_error('last_name', 'Last Name must be lowercase')
        return cleaned_data