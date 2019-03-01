from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from scheduling.models import Doctor, Patient, Appointment

# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm

# admin.site.register(CustomUser, CustomUserAdmin)
# Register the models so that they appear as tables in Django admin

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)