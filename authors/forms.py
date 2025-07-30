from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name',
                    'last_name',
                    'username', 
                    'email', 
                    'password'
                ]
        # exclue = ['first_name']
        labels = {
            'username': 'Username',
            'first_name': 'Fist name',
            'last_name': 'Last name',
            'email': 'Email', 
            'password': 'Password'
        }
        help_texts = {
            'email': 'The email must be valid.',
        }
        error_messsages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here',
            'class': 'input text-input',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }
