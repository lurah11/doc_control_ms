from django import forms
from .models import Accounts,Department
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import *

class RegisterForm(forms.Form): 
    username = forms.CharField(max_length=100,required=True)
    first_name = forms.CharField(max_length=100,required=True)
    last_name = forms.CharField(max_length=100,required=True)
    dept = forms.ChoiceField(choices=Department.DEPT_CHOICES)
    email = forms.EmailField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))
        self.helper.form_id = 'registration-form'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')

class CustomPWChangeForm(PasswordChangeForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'pw-change-form'        
        self.helper.add_input(Submit('submit', 'Change Password'))

class CustomPWResetForm(PasswordResetForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'pw-reset-form'        
        self.helper.add_input(Submit('submit', 'Send to My EMail',css_class="btn btn-warning"))

class CustomPWResetConfirmForm(SetPasswordForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'new-pw-form'        
        self.helper.add_input(Submit('submit', 'Submit',css_class="btn btn-success"))

        
    

