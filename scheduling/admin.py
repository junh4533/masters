from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from scheduling.models import Doctor, Patient, Appointment, User
from .forms import UserCreationForm, UserChangeForm

# Register the models so that they appear as tables in Django admin

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = UserCreationForm
    form = UserChangeForm

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(User,CustomUserAdmin)