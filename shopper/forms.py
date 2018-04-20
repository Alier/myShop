from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    zipcode = forms.CharField(min_length=5, max_length=5, help_text='Required. Input your zipcode.')

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email', 'zipcode', 'birth_date', 'password1', 'password2', )
