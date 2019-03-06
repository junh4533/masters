# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Patient

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Patient
        fields = ('username','email','pid','patient_fn','patient_ln')

#allow the admin to change patient credentials
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Patient
        fields = UserChangeForm.Meta.fields