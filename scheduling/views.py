from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import *
from scheduling.models import *
from django.contrib.auth.models import User

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

# class AppointmentForm(generic.CreateView):
#     form_class = AppointmentForm
#     success_url = reverse_lazy('index')
#     template_name = 'scheduling/make_appointment.html'

def all_appointments(request):
    if request.user.user_type == "assistant":
        all_appointments = Appointment.objects.all().order_by('date','timeslot')
        user = request.user.first_name + " " + request.user.last_name
    elif request.user.user_type == "doctor":
        all_appointments = Appointment.objects.filter(doctor = request.user.doctor.upin).order_by('date').order_by('timeslot')
        user = "Dr. " + request.user.first_name + " " + request.user.last_name
    
    return TemplateResponse(request, 'scheduling/appointments.html', {"all_appointments" : all_appointments})

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
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('../profile/')
    else:
        form = EditProfile(request.POST, instance=request.user)
        heading = "Edit Your Profile"
        return render(request, 'registration/profile.html', {'form':form,'heading':heading})

#################### assistants' views ####################
class SignUp(generic.CreateView):
    form_class = CustomCreationForm
    success_url = reverse_lazy('add_user')
    template_name = 'registration/add_user.html'

def assistant_portal(request):
    appointments = Appointment.objects.all().order_by('date','timeslot')[:5]
    return TemplateResponse(request, 'scheduling/assistant.html', {"appointments" : appointments})

def doctors(request):
    doctors = Doctor.objects.all()
    return TemplateResponse(request, 'scheduling/view_doctors.html', {"doctors" : doctors})

def make_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../appointments/')
    else:
        form = AppointmentForm(request.POST)
        return render(request, 'scheduling/assistant.html', {"form" : form})

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
    print(data_input)
    appointments = Appointment.objects.filter(patient=request.user.patient.pid).order_by('date','timeslot')
    selected_date = Appointment.objects.filter(date = data_input).values_list('timeslot', flat=True)
    available_appointments = [(value, time) for value, time in Appointment.TIMESLOT_LIST if value not in selected_date]
    doctor =  Patient.objects.get(doctor=request.user.patient.doctor).doctor

    if request.method == 'POST':
        print(request.POST)
        
        form = AppointmentForm(request.POST)
        # ,initial={'doctor': doctor,'patient': request.user.patient,'date':data_input}
        if form.is_valid():
            form.save()
            return redirect('../home/')
        else:
            print(form.errors)
    else:
        form = AppointmentForm(request.POST)
    return render(request, 'scheduling/patient.html', {"form" : form, "appointments" : appointments, "available_appointments" : available_appointments, "data_input": data_input, "doctor": doctor})