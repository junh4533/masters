# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Patient, Doctor, Appointment, User

#form to create a new patient
class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('first_name','last_name','email','username')

#allows the admin to change patient credentials
class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')
