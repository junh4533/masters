# models
from scheduling.models import *
from django.contrib.auth.models import User

# forms
from scheduling.forms import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

#URL
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse

#Chart
from django.db.models import Count
import json

#Reports
from scheduling.filter import UserFilter

#etc
from django.utils.dateparse import parse_date
from django.core.mail import send_mail
from datetime import datetime, timedelta

#################### assistants' views ####################
def assistant_portal(request):
    appointments = Appointment.objects.all().order_by('date','timeslot').filter(date=date.today())[:5]
        #generate chart
    dataset = Appointment.objects\
        .filter(date__gte=datetime.now())\
        .values('doctor',
        'doctor__user__first_name',
        'doctor__user__last_name',
        )\
        .annotate(appointment_count=Count('date'))\
        .order_by('doctor')
    print(dataset)
    categories = list()
    appointment_count = list()

    # for entry in dataset:
    #     categories.append('Dr.')
    #     categories.append(entry['doctor__user__first_name'])
    #     categories.append(entry['doctor__user__last_name'])
    #     # categories = " ".join(categories)
    #     appointment_count.append(entry['appointment_count'])
    #     print(json.dumps(categories))
        
    return render(request, 'scheduling/assistant.html', 
    {"appointments" : appointments,
    # "categories":json.dumps(categories),
    "appointment_count":json.dumps(appointment_count),
    "dataset": dataset,
    })

def add_user(request):
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user_type = form.cleaned_data['user_type']
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            if user_type == "doctor":
                return redirect('../add_doctor_info/')
            elif user_type == "patient":
                return redirect('../add_patient_info/')
            elif user_type == "assistant":
                success = "Assistant added!"
                appointments = Appointment.objects.all().order_by('date','timeslot').filter(date__gte=datetime.now())[:5]
                args = {'success':success, "appointments":appointments}
                return render(request, 'scheduling/assistant.html', args)
        else:
            return render(request, 'registration/add_user.html', {'form':form})
    else:
        heading = "Add User"
        form = CustomCreationForm
        args = {'form':form,'heading':heading}
        return render(request, 'registration/add_user.html', args)

# to add additional information for doctors like specialty/picture
def add_doctor_info(request):
    fn = request.session['first_name'] 
    ln = request.session['last_name']
    doctor = User.objects.get(first_name=fn, last_name=ln).doctor
    if request.method == 'POST':
        form = AddDoctorInfo(request.POST, request.FILES, instance=doctor)
        print(form.errors)
        if form.is_valid():
            form.save()
            success = "Doctor successfully added"
            # return render(request, 'scheduling/assistant.html', {'success':success})
            return redirect('assistant_portal')
        else:
            return render(request, 'registration/add_user.html', {'form':form})
    else:
        heading = "Please provide additional information for " + fn + " " + ln 
        form = AddDoctorInfo(instance=doctor)
        args = {'form':form,'heading':heading}
        return render(request, 'registration/add_user.html', args)

# to add additional information for paitents like doctor/picture
def add_patient_info(request):
    fn = request.session['first_name'] 
    ln = request.session['last_name']
    patient = User.objects.get(first_name=fn, last_name=ln).patient
    if request.method == 'POST':
        form = AddPatientInfo(request.POST, request.FILES, instance=patient)
        print(form.errors)
        if form.is_valid():
            form.save()
            success = "Patient successfully added"
            # return render(request, 'scheduling/assistant.html', {'success':success})
            return redirect('assistant_portal')
        else:
            return render(request, 'registration/add_user.html', {'form':form})
    else:
        heading = "Please provide additional information for " + fn + " " + ln
        form = AddPatientInfo(instance=patient)
        args = {'form':form,'heading':heading}
        return render(request, 'registration/add_user.html', args)
    
def doctors(request):
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
        doctors = Doctor.objects.all()
        args = {"doctors" : doctors}
        return render(request, 'scheduling/view_doctors.html', args)
    
def make_appointments(request):
    data_input = request.GET.get('date')
    if not data_input:
        data_input = str(date.today())
        date_object = date.today()
        print(data_input, date_object)
    else:
        date_object = parse_date(data_input)
    
    # doctors = Doctor.objects.all()
    selected_date = Appointment.objects.filter(date = data_input).values_list('timeslot', flat=True)
    # available_doctor = Appointment.objects.filter(date = data_input)
    # print(available_doctor)
    # available_appointments = [((value, time) for value, time in Appointment.TIMESLOT_LIST if value not in selected_date and if doctor not in available_doctor)]
    available_appointments = [(value, time) for value, time in Appointment.TIMESLOT_LIST if value not in selected_date]
    print(available_appointments)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            success = "Appointment created!"
            email = str(form.instance.patient.user.email)
            message = 'Appointment scheduled for ' + str(form.cleaned_data['date']) + " " + str(form.instance.get_timeslot_display())
            send_mail('EZDoct Appointment', message, 'EZDoctPortal@gmail.com', [email])
            print(email)
            print(message)
            form = AppointmentForm
            return render(request, 'scheduling/make_appointments.html', {"success" : success,"form":form})
        else:
            print("invalid")
    else:
        form = AppointmentForm
        args = {
            "form" : form, 
            "available_appointments" : available_appointments, 
            "data_input": data_input,
            "date_object": date_object,
        }
        return render(request, 'scheduling/make_appointments.html', args)