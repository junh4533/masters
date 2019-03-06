from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# from scheduling.models import Doctor, Appointment
from scheduling.models import Doctor, Patient, Appointment
from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import Patient

# Register the models so that they appear as tables in Django admin

class CustomUserAdmin(UserAdmin):
    model = Patient
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)