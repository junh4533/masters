from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import *
from scheduling.models import *
# from django.db.models import F
# from django.views.generic.edit import UpdateView

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

class AppointmentForm(generic.CreateView):
    form_class = AppointmentForm
    success_url = reverse_lazy('index')
    template_name = 'scheduling/make_appointment.html'

def reports(request):
    return render(request, 'scheduling/reports.html')

def settings(request):
    return render(request, 'scheduling/settings.html')

#################### assistants' views ####################
class SignUp(generic.CreateView):
    form_class = CustomCreationForm
    success_url = reverse_lazy('add_user')
    template_name = 'registration/add_user.html'

def assistant_portal(request):
    appointments = Appointment.objects.all().order_by('date').order_by('timeslot')[:5]
    print(appointments)
    return TemplateResponse(request, 'scheduling/assistant.html', {"appointments" : appointments})

def all_appointments(request):
    all_appointments = Appointment.objects.all().order_by('date').order_by('timeslot')
    print(all_appointments)
    return TemplateResponse(request, 'scheduling/appointments.html', {"all_appointments" : all_appointments})

def all_patients(request):
    patients = Patient.objects.all()
    return render(request, 'scheduling/view_patients.html', {"patients" : patients})

def doctors(request):
    doctors = Doctor.objects.all()
    print(doctors)
    return TemplateResponse(request, 'scheduling/view_doctors.html', {"doctors" : doctors})

#################### doctors' views ####################
def doctor_portal(request):
    appointments = Appointment.objects.filter(doctor=request.user.doctor.upin).order_by('date').order_by('timeslot')[:5]
    print(request.user.doctor.upin)
    print(appointments)
    return TemplateResponse(request, 'scheduling/doctor.html', {"appointments" : appointments})

def doctor_appointments(request):
    appointments = Appointment.objects.filter(doctor = request.user.doctor.upin).order_by('date').order_by('timeslot')
    return TemplateResponse(request, 'scheduling/appointments.html', {"appointments" : appointments})

def doctor_patients(request):
    patients = Patient.objects.filter(doctor = request.user.doctor)
    return render(request, 'scheduling/view_patients.html')

def doctor_profile(request):
    profile = Doctor.objects.filter(upin=request.user.doctor.upin)
    return render(request, 'registration/profile.html', {'profile': profile})

# for doctors to add additional information like specialty/appointments per hour
def add_info(request):
    if request.method == 'POST':
        form = EditDoctorForm(request.POST, instance=request.user.doctor)

        if form.is_valid():
            form.save()
            return redirect('../../profile/')
    else:   
        form = EditDoctorForm(request.POST, instance=request.user.doctor)
        return render(request, 'registration/profile.html', {'form':form})

#################### patients' views ####################
def patient_portal(request):
    appointments = Appointment.objects.filter(patient=request.user.patient.pid)
    data_input = request.GET.get('date')
    selected_date = Appointment.objects.filter(date = data_input).values_list('timeslot', flat=True)
    available_appointments = [(value, time) for value, time in Appointment.TIMESLOT_LIST if value not in selected_date]
    return TemplateResponse(request, 'scheduling/patient.html', {"appointments" : appointments, "available_appointments" : available_appointments, "data_input": data_input})

def patient_profile(request):
    profile = Patient.objects.filter(pid=request.user.patient.pid)
    return render(request, 'registration/profile.html', {'profile': profile})



