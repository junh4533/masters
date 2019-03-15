# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Appointment, User

#form to create a new patient
class DoctorCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('first_name','last_name','username','email','phone','id','specialty','appointments_per_day',)

#allows the admin to change patient credentials
class DoctorChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','phone','id','specialty','appointments_per_day',)

#form to create a new patient
class PatientCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('first_name','last_name','username','email','phone','id',)

#allows the admin to change patient credentials
class PatientChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','phone','id',)



