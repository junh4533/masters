# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Patient

#form to create a new patient
class PatientCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Patient
        fields = ('pid','patient_fn','patient_ln','phone','email',)

#allows the admin to change patient credentials
class PatientChangeForm(UserChangeForm):
    class Meta:
        model = Patient
        fields = UserChangeForm.Meta.fields