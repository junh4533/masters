# users/forms.py
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Appointment, User, Doctor, Patient

#form to create a new patient
class CustomCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('first_name','last_name','username','email','user_type',)
        
#allows the user to change their information
class CustomChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        # fields = ('specialty','start_time','end_time','days_available','appointments_per_hour',)
        fields = ('user','specialty','appointments_per_hour','picture')

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('doctor','patient','timeslot',)