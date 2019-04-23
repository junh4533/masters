# users/forms.py
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

#form to create a new user
class CustomCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('first_name','last_name','username','email','user_type',)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ('user','specialty','picture')

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('doctor','patient','date','timeslot') 

class EditProfile(UserChangeForm):
    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            "email",
        }

class AddDoctorInfo(UserChangeForm):
    class Meta:
        model = Doctor
        fields = {
            # "user",
            "specialty",
            "picture"
        }

class AddPatientInfo(UserChangeForm):
    class Meta:
        model = Patient
        fields = {
            # 'user',
            'doctor',
            'picture'
        }

class searchAppointment(forms.Form):
     date = models.DateField(default=date.today)