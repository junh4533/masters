from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from scheduling.models import User, Doctor, Patient, Appointment
from .forms import DoctorForm, LoginForm, CustomCreationForm

#show all fields in the doctor table
class CustomDoctorAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Doctor._meta.fields]

#show all fields in the patient table
class CustomPatientAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Patient._meta.fields]

admin.site.register(User, UserAdmin)
admin.site.register(Patient, CustomPatientAdmin)
admin.site.register(Doctor, CustomDoctorAdmin)
admin.site.register(Appointment)



