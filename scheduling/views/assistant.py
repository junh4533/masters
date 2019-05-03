# models
from scheduling.models import *
from django.contrib.auth.models import User

# forms
# from forms import *
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

#################### assistants' views ####################
def assistant_portal(request):
    appointments = Appointment.objects.all().order_by('date','timeslot').filter(date__gte=datetime.now())[:5]
        #generate chart
    dataset = Appointment.objects\
        .values('doctor',
        'doctor__user__first_name',
        'doctor__user__last_name',
        )\
        .annotate(appointment_count=Count('date'))\
        .order_by('doctor')
    
    categories = list()
    appointment_count = list()

    for entry in dataset:
        categories.append('Dr.')
        categories.append(entry['doctor__user__first_name'])
        categories.append(entry['doctor__user__last_name'])
        categories = ' '.join(categories)
        appointment_count.append(entry['appointment_count'])
    print(json.dumps(categories))
    return render(request, 'scheduling/assistant.html', 
    {"appointments" : appointments,
    "categories":json.dumps(categories),
    "appointment_count":json.dumps(appointment_count),
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
        heading = "Add a User"
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
            return render(request, 'scheduling/assistant.html', {'success':success})
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
            return render(request, 'scheduling/assistant.html', {'success':success})
        else:
            return render(request, 'registration/add_user.html', {'form':form})
    else:
        heading = "Please provide additional information for " + fn + " " + ln
        form = AddPatientInfo(instance=patient)
        args = {'form':form,'heading':heading}
        return render(request, 'registration/add_user.html', args)
    
def doctors(request):
    doctors = Doctor.objects.all()
    args = {"doctors" : doctors}
    return render(request, 'scheduling/view_doctors.html', args)


def make_appointments(request):
    # date_session = request.session['data_input']
    data_input = request.GET.get('date')
    print(data_input)
    if data_input == None:
        data_input = date.today()
        print(data_input)

    selected_date = Appointment.objects.filter(date = data_input).values_list('timeslot', flat=True)
    available_appointments = [(value, time) for value, time in Appointment.TIMESLOT_LIST if value not in selected_date]
    print(available_appointments)
    # request.session['data_input'] = data_input
    # date_session = data_input
    # print("Input2: ", data_input)
    form = AppointmentForm(request.POST)
    args = {
        "form" : form, 
        "available_appointments" : available_appointments, 
        "data_input": data_input, 
        # "date_session": date_session,
    }

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            success = "Appointment created!"
            email = str(form.instance.patient.user.email)
            message = 'Appointment scheduled for ' + str(form.cleaned_data['date']) + " " + str(form.instance.get_timeslot_display())
            send_mail('EzDoc Appointment', message, 'EZDoctPortal@gmail.com', [email])
            print(email)
            print(message)
            form = AppointmentForm
            return render(request, 'scheduling/make_appointments.html', {"success" : success,"form":form})
        else:
            print("invalid form")
            return render(request, 'scheduling/make_appointments.html', {"form":form})
    # elif request.method == 'GET':
        
    print("dsas")
    return render(request, 'scheduling/make_appointments.html', args)
    # elif request.method == 'GET':