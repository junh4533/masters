from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import DoctorForm, LoginForm, CustomCreationForm, CustomChangeForm, AppointmentForm
from django.http import HttpResponse
from django.template.response import TemplateResponse
from scheduling.models import User, Doctor, Patient, Appointment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class SignUp(generic.CreateView):
    form_class = CustomCreationForm
    success_url = reverse_lazy('add_doctor')
    template_name = 'registration/add_user.html'

class AddDoctor(generic.CreateView):
    form_class = DoctorForm
    success_url = reverse_lazy('index')
    template_name = 'registration/add_doctor.html'

# class ChangeInfo(generic.CreateView):
#     form_class = CustomChangeForm
#     success_url = reverse_lazy('index')
#     template_name = 'registration/edit.html'

class AppointmentForm(generic.CreateView):
    form_class = AppointmentForm
    success_url = reverse_lazy('appointments')
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

def index(request):
    if request.user.is_authenticated:
        if request.user.user_type=="doctor":
            return redirect('doctor_portal')
        elif request.user.user_type=="patient":
            return redirect('patient_portal')
        else:
            return redirect('assistant_portal')
    return render(request, 'scheduling/index.html')

def doctor_portal(request):
    return render(request, 'scheduling/doctor.html')

def patient_portal(request):
    return render(request, 'scheduling/patient.html')

def assistant_portal(request):
    return render(request, 'scheduling/assistant.html')

def appointments(request):
    # data = Appointment.objects.get(patient=request.user)
    data = Appointment.objects.all()
    print(data)
    return TemplateResponse(request, 'scheduling/appointments.html', {"data" : data})

def patients(request):
    return render(request, 'scheduling/view_patients.html')

def reports(request):
    return render(request, 'scheduling/reports.html')

def settings(request):
    return render(request, 'scheduling/settings.html')

# def AddDoctor(request):
#     if request.method == 'POST':
#         form = UserChangeForm(request.POST, instance=request.user)

#         if form.is_valid():
#             form.save()
#             return redirect('scheduling/index.html')
#     else:   
#         form = UserChangeForm(request.POST, instance=request.user)
#         args = {'form':form}
#         return render(request, 'scheduling/index.html', args)


# #for users to edit personal information
# def EditInfo(request):
#     if request.method == 'POST':
#         form = UserChangeForm(request.POST, instance=request.user)

#         if form.is_valid():
#             form.save()
#             return redirect('scheduling/index.html')
#     else:   
#         form = ChangeInfoForm(request.POST, instance=request.user)
#         args = {'form':form}
#         return render(request, 'scheduling/index.html', args)


