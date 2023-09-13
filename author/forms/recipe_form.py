from django import forms

from app.models import Recipes
from utils.django_forms import add_attr
from collections import defaultdict
from django.core.exceptions import ValidationError

from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._form_errors = defaultdict(list)
        add_attr(field = self.fields.get('title'), attr_name = 'class',attr_new_val = 'span-2')
        
    def validate_positive_number_field(
        self,
        field_name,
        message_error = 'The field must be greater than 0'
    ):
        field = self.cleaned_data.get(field_name)
        
        if not is_positive_number(field):
                self._form_errors[field_name].append(message_error)
        return field
    
    class Meta:
        model = Recipes
        exclude = (
            'is_published',
            'slug',
            'created_at',
            'updated_at',
            'preparation_steps_is_html',
            'author'
        )
        widgets = {
            'cover_image': forms.FileInput(
                attrs = {
                    'class': 'span-2'
                }   
            ),
            'servings_unit': forms.Select(
                choices = (
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )                 
            ),        
        }
    def clean(self, *args, **kwargs):
            super_clean = super().clean(*args, **kwargs)
            cleaned_data = self.cleaned_data
            title = cleaned_data.get('title')
            description = cleaned_data.get('description')                    
                
            if title == description:
                self._form_errors['description'].append(f'Cannot be equal description "{description}"')
                
            if self._form_errors:
                raise ValidationError(self._form_errors)
                
            return super_clean
        
    def clean_title(self):
        title = self.cleaned_data.get('title')    
        if len(title) < 4:
                self._form_errors['title'].append('Title must have more than 4 characters')             
        return title
    
    def clean_preparation_time(self):
        field_name = 'preparation_time'            
        return self.validate_positive_number_field(field_name, 'Preparation time must be greater than 0')
    
    def clean_num_servings(self):
        field_name = 'num_servings'
        return self.validate_positive_number_field(field_name, 'Number of servings must be greater than 0')
    
    def clean_num_preparations(self):
        field_name = 'num_preparations'               
        return self.validate_positive_number_field(field_name, 'Number preparations must be greater than 0')