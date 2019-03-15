from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserCreationForm, DoctorCreationForm, DoctorChangeForm, PatientCreationForm, PatientChangeForm

class DoctorSignUp(generic.CreateView):
    form_class = DoctorCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class PatientSignUp(generic.CreateView):
    form_class = PatientCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def index(request):
    return render(request, 'scheduling/index.html')

def appointments(request):
    return render(request, 'scheduling/appointments.html')

def patients(request):
    return render(request, 'scheduling/patients.html')

def reports(request):
    return render(request, 'scheduling/reports.html')

def settings(request):
    return render(request, 'scheduling/settings.html')


