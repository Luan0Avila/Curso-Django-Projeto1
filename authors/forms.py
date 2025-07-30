from django import forms
from django.contrib.auth.models import User

def add_placeholder(field, placeolder_val):
    field.widget.attrs['placeholder'] = placeolder_val


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your email')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')


    password = forms.CharField(
        required=True,
        widget= forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one 1 uppercase letter'
            'one lowercase letter and one number'
            'at least 8 characters'
        )
        )
    
    password2 = forms.CharField(
        required=True,
        widget= forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
    )

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
