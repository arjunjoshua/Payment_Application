from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, ButtonHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

CURRENCY_CHOICES = (
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('GBP', 'GBP'),
)


class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    currency = forms.CharField(max_length=3, widget=forms.Select(choices=CURRENCY_CHOICES, attrs={'class': 'form-select', 'placeholder': 'Select Currency'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-12 col-md-6'),
                Column('email', css_class='col-12 col-md-6'),
                css_class='mb-3'
            ),
            Row(
                Column('password1', css_class='col-12 col-md-6'),
                Column('password2', css_class='col-12 col-md-6'),
                css_class='mb-3'
            ),
            Row(
                Column('first_name', css_class='col-12 col-md-6'),
                Column('last_name', css_class='col-12 col-md-6'),
                css_class='mb-3'
            ),
            Row(
                Column('currency', css_class='col-12 col-md-6'),
                css_class='mb-3'
            ),
            Submit('submit', 'Register', css_class='btn btn-primary'),
        )

    class Meta:
        model = CustomUser
        fields = ['username',
                  'email',
                  'password1',
                  'password2',
                  'first_name',
                  'last_name',
                  'currency']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_show_labels = False

        # Code to set the layout of the form
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-md-4 mx-auto mb-3'),
                css_class='justify-content-center'
            ),
            Row(
                Column('password', css_class='col-md-4 mx-auto mb-3'),
                css_class='justify-content-center'
            ),
            ButtonHolder(
                Submit('submit', 'Login', css_class='btn-primary'),
                css_class='d-flex justify-content-center mt-3'
            ),
        )
