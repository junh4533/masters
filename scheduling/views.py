# models
from scheduling.models import *
from django.contrib.auth.models import User

# forms
from .forms import *
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
from .filter import UserFilter
from datetime import datetime

#################### generic views ####################
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        print("wrong")
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            # if user is not None:
            if request.user.is_authenticated:
                print("wrong")
                if user_type=="patient":
                    login(request, user)
                    return redirect('patient_portal')
                elif user_type=="doctor":
                    login(request, user)
                    return redirect('doctor_portal')
                else:
                    login(request, user)
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
        all_appointments = Appointment.objects.filter(doctor = request.user.doctor.upin).order_by('date').order_by('timeslot')
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
    return render(request, 'scheduling/reports.html')

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

#################### assistants' views ####################
def assistant_portal(request):
    appointments = Appointment.objects.all().order_by('date','timeslot').filter(date__gte=datetime.now())[:5]
    #generate chart
    dataset = Appointment.objects\
        .values('doctor',
        'doctor__user__last_name',
        )\
        .annotate(appointment_count=Count('date'))\
        .order_by('doctor')
    
    categories = list()
    appointment_count = list()

    for entry in dataset:
        categories.append('%s Doctor' % entry['doctor__user__last_name'])
        appointment_count.append(entry['appointment_count'])
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
            form = CustomCreationForm
            return render(request, 'registration/add_user.html', {'form':form})
    else:
        form = CustomCreationForm
        return render(request, 'registration/add_user.html', {'form':form})

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
        heading = "Please provide additional information for the doctor"
        form = AddDoctorInfo(instance=doctor)
        return render(request, 'registration/add_user.html', {'form':form,'heading':heading})

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
        heading = "Please provide additional information for " +fn + " " + ln
        form = AddPatientInfo(instance=patient)
        return render(request, 'registration/add_user.html', {'form':form,'heading':heading})
    
def doctors(request):
    doctors = Doctor.objects.all()
    args = {"doctors" : doctors}
    return render(request, 'scheduling/view_doctors.html', args)

def assistant_report(request):
    appointments = Appointment.objects.all().order_by('date').order_by('timeslot')
    user_filter = UserFilter(request.GET, queryset=appointments)
    return render(request,'scheduling/reports.html',
    {'filter': user_filter,
    'appointments':appointments}
    )

def make_appointments(request):
    data_input = request.GET.get('date')
    if not data_input:
        data_input = date.today()
        print(data_input)
    selected_date = Appointment.objects.filter(date = data_input).values_list('timeslot', flat=True)
    print(selected_date)
    available_appointments = [(value, time) for value, time in Appointment.TIMESLOT_LIST if value not in selected_date]

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            success = "Appointment created!"
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
        }
        return render(request, 'scheduling/make_appointments.html', args)

#################### doctors' views ####################
def doctor_portal(request):
    appointments = Appointment.objects.filter(doctor=request.user.doctor.upin).order_by('date','timeslot')[:4]
    appointments_today = Appointment.objects.filter(doctor=request.user.doctor.upin).filter(date=datetime.now().date()).count()
    print(appointments_today)
    args = {"appointments" : appointments}
    return render(request, 'scheduling/doctor.html', args)

#################### patients' views ####################
def patient_portal(request):
    data_input = request.GET.get('date')
    print(data_input)
    patient = User.objects.get(patient=request.user.patient)
    appointments = Appointment.objects.filter(patient=request.user.patient.pid).filter(date__gte=datetime.now()-timedelta(days=1)).order_by('date','timeslot')
    selected_date = Appointment.objects.filter(date = data_input).values_list('timeslot', flat=True)
    available_appointments = [(value, time) for value, time in Appointment.TIMESLOT_LIST if value not in selected_date]
    doctor =  Patient.objects.get(doctor=request.user.patient.doctor).doctor
    doctor_pic = Doctor.objects.get(upin=request.user.patient.doctor.upin)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../home/')
    else:
        form = AppointmentForm(request.POST)
        args = {
            "form" : form, 
            "appointments" : appointments, 
            "available_appointments" : available_appointments, 
            "data_input": data_input, 
            "doctor": doctor, 
            "doctor_pic": doctor_pic,
        }
        return render(request, 'scheduling/patient.html', args)