from django import forms
from register.models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, ButtonHolder, Column


class PaymentForm(forms.Form):
    username = forms.CharField(max_length=32)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Column(Field('username', placeholder="Username", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Column(Field('amount', placeholder="Amount to transfer", css_class="text-center"), css_class='col-md-4 mx-auto'),
            ButtonHolder(
                Submit('submit', 'Transfer', css_class="btn-primary"),
                css_class="text-center"
            ),
        )

    # returns an error in the form if the entered user does not exist
    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError('User does not exist')
        return username


class RequestForm(forms.Form):
    username = forms.CharField(max_length=32)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Column(Field('username', placeholder="Username", css_class="text-center"), css_class='col-md-4 mx-auto'),
            Column(Field('amount', placeholder="Requested amount", css_class="text-center"), css_class='col-md-4 mx-auto'),
            ButtonHolder(
                Submit('submit', 'Request', css_class="btn-primary"),
                css_class="text-center"
            ),
        )

    # returns an error in the form if the entered user does not exist
    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError('User does not exist')
        return username
