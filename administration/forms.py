from django.contrib.auth.forms import UserCreationForm
from django import forms
from register.models import CustomUser


class AdminRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
