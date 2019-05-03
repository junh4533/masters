# models
from scheduling.models import *
from django.contrib.auth.models import User

# forms
from scheduling.forms import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from django.urls import reverse_lazy
from django.views import generic

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse

#for chart
from django.db.models import Count
from datetime import datetime, timedelta
import json

#for reports
from scheduling.filter import UserFilter
from datetime import datetime

from django.core.mail import send_mail

#################### generic views ####################
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if request.user.is_authenticated:
                if user_type=="patient":
                    login(request, user)
                    return redirect('patient_portal')
                elif user_type=="doctor":
                    login(request, user)
                    return redirect('doctor_portal')
                elif user_type=="assistant":
                    return redirect('assistant_portal')    
    else:
        form = LoginForm()
        return render(request,'registration/login.html',{'form':form})

def index(request):
    if request.user.is_authenticated:
        if request.user.user_type=="doctor":
            return redirect('doctor_portal')
        elif request.user.user_type=="patient":
            return redirect('patient_portal')
        else:
            return redirect('assistant_portal')
    else:
        return redirect('home/login')

def all_appointments(request):
    if request.user.user_type == "doctor":
        all_appointments = Appointment.objects.filter(doctor = request.user.doctor.upin)
    else:
        all_appointments = Appointment.objects.all().order_by('date','timeslot')
    return render(request, 'scheduling/appointments.html', {"all_appointments" : all_appointments})

def delete_appointment(request):
    Appointment.objects.filter(id=request.POST.get('appointment_id')).delete()
    if request.user.user_type == "doctor":
        all_appointments = Appointment.objects.filter(doctor = request.user.doctor.upin)
    else:
        all_appointments = Appointment.objects.all().order_by('date','timeslot')
    return render(request, 'scheduling/appointments.html', {"all_appointments" : all_appointments})

def patients(request):
    if request.user.user_type == "doctor":
        patients = Patient.objects.filter(doctor = request.user.doctor)
        # user = request.user
    else:
        patients = Patient.objects.all()
        # user = request.user
    
    args = {"patients" : patients}
    return render(request, 'scheduling/view_patients.html', args)

def reports(request):
    appointments = Appointment.objects.all().order_by('date').order_by('timeslot')
    user_filter = UserFilter(request.GET, queryset=appointments)
    return render(request,'scheduling/reports.html',
    {'filter': user_filter,
    'appointments':appointments}
    )

def settings(request):
    return render(request, 'scheduling/settings.html')

def edit_profile(request):
    heading = "Edit Your Profile"
    success = "Profile successfully updated."
    
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            args = {'form':form,'heading':heading,'success':success}
            return render(request, 'registration/profile.html', args)
    else:
        form = EditProfile(instance=request.user)
        args = {'form':form,'heading':heading}
        return render(request, 'registration/profile.html', args)

def change_password(request):
    heading = "Change Your Password"
    success = "Password successfully changed."

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            args = {'form':form, 'heading':heading,'success':success}
            return render(request, 'registration/profile.html', args)
        else:
            args = {'form':form, 'heading':heading}
            return render(request, 'registration/profile.html', args)
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form, 'heading':heading}
        return render(request, 'registration/profile.html', args)



