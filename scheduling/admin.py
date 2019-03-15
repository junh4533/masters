from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from scheduling.models import Appointment, User
from .forms import DoctorCreationForm, DoctorChangeForm, PatientCreationForm, PatientChangeForm

# Register the models so that they appear as tables in Django admin

class CustomDoctorAdmin(UserAdmin):
    model = User
    add_form = DoctorCreationForm
    form = DoctorChangeForm

class CustomPatientAdmin(UserAdmin):
    model = User
    add_form = PatientCreationForm
    form = PatientChangeForm

admin.site.register(Appointment)
# admin.site.register(User,CustomDoctorAdmin)
# admin.site.register(User,CustomPatientAdmin)
admin.site.register(User)
