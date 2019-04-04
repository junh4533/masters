from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import DoctorForm, LoginForm, CustomCreationForm, CustomChangeForm, AppointmentForm
from django.http import HttpResponse
from django.template.response import TemplateResponse
from scheduling.models import User, Doctor, Patient, Appointment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import F
from django.views.generic.edit import UpdateView

class SignUp(generic.CreateView):
    form_class = CustomCreationForm
    success_url = reverse_lazy('add_doctor')
    template_name = 'registration/add_user.html'

class AddDoctor(UpdateView):
    form_class = DoctorForm
    success_url = reverse_lazy('index')
    template_name = 'registration/add_doctor.html'

# class ChangeInfo(generic.CreateView):
#     form_class = CustomChangeForm
#     success_url = reverse_lazy('index')
#     template_name = 'registration/edit.html'

class AppointmentForm(generic.CreateView):
    form_class = AppointmentForm
    success_url = reverse_lazy('index')
    template_name = 'scheduling/make_appointment.html'

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

def doctorupdate(request):
    if request.method =='POST':
        form = DoctorForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('assistant_portal')
    
    else:
        form = UserChangeForm(instance=request.user)
        args = {'form': form}
        return render(request,'scheduling/index.html')

def index(request):
    if request.user.is_authenticated:
        if request.user.user_type=="doctor":
            return redirect('doctor_portal')
        elif request.user.user_type=="patient":
            return redirect('patient_portal')
        else:
            return redirect('assistant_portal')

#################### assistants' views ####################
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
    appointments = Appointment.objects.get(doctor=request.user.doctor.upin).order_by('date').order_by('timeslot')[:5]
    print(request.user.doctor.upin)
    print(appointments)
    return TemplateResponse(request, 'scheduling/doctor.html', {"appointments" : appointments})

def doctor_appointments(request):
    appointments = Appointment.objects.get(doctor=request.user.doctor.upin).order_by('date').order_by('timeslot')
    return TemplateResponse(request, 'scheduling/appointments.html', {"appointments" : appointments})

def doctor_patients(request):
    patients = Patient.objects.get(doctor = request.user.doctor)
    return render(request, 'scheduling/view_patients.html')

#################### patients' views ####################
def patient_portal(request):
    appointments = Appointment.objects.get(patient=request.user)
    return TemplateResponse(request, 'scheduling/patient.html', {"appointments" : appointments})

#################### etc ####################
def reports(request):
    return render(request, 'scheduling/reports.html')

def settings(request):
    return render(request, 'scheduling/settings.html')


