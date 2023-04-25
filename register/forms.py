from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML, ButtonHolder, Row, Column
from .models import CURRENCY_CHOICES


class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    currency = forms.CharField(max_length=3, widget=forms.Select(choices=CURRENCY_CHOICES))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Column(Field('username', placeholder="Username", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Column(Field('email', placeholder="Email", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Column(Field('password1', placeholder="Password", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Column(Field('password2', placeholder="Re-Enter Password", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Column(Field('first_name', placeholder="First Name", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Column(Field('last_name', placeholder="Last Name", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Row(
                Column(HTML('<p>Select Currency:</p>'), css_class='col-md-4 mx-auto'),
                Column('currency', css_class='col-md-5 mx-auto'),
                css_class='col-md-4 mx-auto'
            ),
            ButtonHolder(
                Submit('submit', 'Register', css_class='btn-primary'),
                css_class="text-center"
            ),
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
    username = forms.CharField(label='Username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Column(Field('username', placeholder="Username", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Column(Field('password', placeholder="Password", css_class="text-center"), css_class='col-md-4 mx-auto'),
            ButtonHolder(
                Submit('submit', 'Login', css_class="btn-primary"),
                css_class="text-center"
            ),
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
