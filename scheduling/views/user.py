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
                    return redirect('home/admin') 
    else:
        form = LoginForm()
        return render(request,'registration/login.html',{'form':form})

def index(request):
    if request.user.is_authenticated:
        if request.user.user_type=="doctor":
            return redirect('doctor_portal')
        elif request.user.user_type=="patient":
            return redirect('patient_portal')
        elif request.user.user_type=="assistant":
            return redirect('assistant_portal')
        else:
            return redirect('home/admin') 
    else:
        return redirect('home/login')

def all_appointments(request):
    if request.method == 'GET':
        if request.user.user_type == "doctor":
            all_appointments = Appointment.objects.filter(doctor = request.user.doctor.upin)
        else:
            all_appointments = Appointment.objects.all().order_by('date','timeslot')
        return render(request, 'scheduling/appointments.html', {"all_appointments" : all_appointments})
    elif request.method == 'POST':
        Appointment.objects.filter(id=request.POST.get('appointment_id')).delete()
        all_appointments = Appointment.objects.all().order_by('date','timeslot')
        return render(request, 'scheduling/appointments.html', {"all_appointments" : all_appointments})

# def delete_appointment(request):
    

def patients(request):
    heading = "Edit Profile"
    success = "Profile successfully updated."
    if request.method == 'POST':
        edit_user = User.objects.get(username = request.session['edit_user_session'])
        form = EditProfile(request.POST, instance=edit_user)
        if form.is_valid():
            request.session['edit_user_session'] = form.cleaned_data['username']
            form.save()
            args = {'form':form,'heading':heading,'success':success}
            return render(request, 'registration/profile.html', args)  
    elif 'edit_profile' in request.GET:
        edit_user = User.objects.get(username = request.GET.get('edit_profile'))
        request.session['edit_user_session'] = request.GET.get('edit_profile')
        form = EditProfile(instance=edit_user)
        args = {'form':form,'heading':heading}
        return render(request, 'registration/profile.html', args) 
    else:
        if request.user.user_type == "doctor":
            patients = Patient.objects.filter(doctor = request.user.doctor)
        else:
            patients = Patient.objects.all()
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
        # if ('edit_user_session' in request.session) and (request.user.username != request.session['edit_user_session']):
        #     print("1")
        #     # print(request.user.username)
        #     # print(request.session['edit_user_session'])
        #     form = EditProfile(request.POST, instance=request.session['edit_user_session'])
        # else:
        #     print("2")
            # print(request.user.username)
            # print(request.session['edit_user_session'])
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            args = {'form':form,'heading':heading,'success':success}
            if request.user.user_type == "patient":
                print("patient profile")
                return render(request, 'registration/patient_profile.html', args)
            else:
                return render(request, 'registration/profile.html', args)
    else:
        form = EditProfile(instance=request.user)
        args = {'form':form,'heading':heading}
        if request.user.user_type == "patient":
            return render(request, 'registration/patient_profile.html', args)
        else:
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
            if request.user.user_type == "patient":
                return render(request, 'registration/patient_profile.html', args)
            else:
                return render(request, 'registration/profile.html', args)
        else:
            args = {'form':form, 'heading':heading}
            if request.user.user_type == "patient":
                return render(request, 'registration/patient_profile.html', args)
            else:
                return render(request, 'registration/profile.html', args)
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form, 'heading':heading}
        if request.user.user_type == "patient":
                return render(request, 'registration/patient_profile.html', args)
        else:
            return render(request, 'registration/profile.html', args)

def our_team(request):
    doctors = Doctor.objects.all()
    print(doctors)
    args = {"doctors" : doctors}
    return render(request, 'scheduling/our_team.html', args)


