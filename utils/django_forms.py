import re
from django import forms

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