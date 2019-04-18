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


#################### generic views ####################
def user_login(request):
    if request.method =="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
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

def all_appointments(request):
    if request.user.user_type == "assistant":
        all_appointments = Appointment.objects.all().order_by('date','timeslot')
        user = request.user.first_name + " " + request.user.last_name
    elif request.user.user_type == "doctor":
        all_appointments = Appointment.objects.filter(doctor = request.user.doctor.upin).order_by('date').order_by('timeslot')
        user = "Dr. " + request.user.first_name + " " + request.user.last_name
    
    return render(request, 'scheduling/appointments.html', {"all_appointments" : all_appointments})

def patients(request):
    if request.user.user_type == "assistant":
        patients = Patient.objects.all()
        user = request.user.first_name + " " + request.user.last_name
    else:
        patients = Patient.objects.filter(doctor = request.user.doctor)
        user = "Dr. " + request.user.first_name + " " + request.user.last_name

    return render(request, 'scheduling/view_patients.html', {"patients" : patients, "user" : user})

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
class SignUp(generic.CreateView):
    form_class = CustomCreationForm
    success_url = reverse_lazy('add_user')
    template_name = 'registration/add_user.html'

def assistant_portal(request):
    appointments = Appointment.objects.all().order_by('date','timeslot')[:5]
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
    return TemplateResponse(request, 'scheduling/assistant.html', 
    {"appointments" : appointments,
    "categories":json.dumps(categories),
    "appointment_count":json.dumps(appointment_count)})
    
def doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'scheduling/view_doctors.html', {"doctors" : doctors})

def make_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../appointments/')
    else:
        form = AppointmentForm(request.POST)
        return render(request, 'scheduling/assistant.html', {"form" : form})

def assistant_report(request):
    appointments = Appointment.objects.all().order_by('date').order_by('timeslot')
    user_filter = UserFilter(request.GET, queryset=appointments)
    return render(request,'scheduling/reports.html',
    {'filter': user_filter,
    'appointments':appointments}
    )


#################### doctors' views ####################
def doctor_portal(request):
    appointments = Appointment.objects.filter(doctor=request.user.doctor.upin).order_by('date','timeslot')[:5]
    return TemplateResponse(request, 'scheduling/doctor.html', {"appointments" : appointments})

# for doctors to add additional information like specialty/appointments per hour
def add_info(request):
    form = AddSpecialtyForm(request.POST, instance=request.user.doctor)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('../../profile/')
    else:   
        heading = "Add your specialty"
        return render(request, 'registration/profile.html', {'form':form,'heading':heading})


#################### patients' views ####################
def patient_portal(request):
    data_input = request.GET.get('date')
    # datetimeobject = datetime.strptime(data_input,'%m/%d/%Y')
    # newformat = datetimeobject.strftime('%Y-%m-%d')
    # print(newformat)
    print(data_input)
    #imported datetime to show only upcoming appointment
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
            "doctor_pic":doctor_pic
        }
        return render(request, 'scheduling/patient.html', args)