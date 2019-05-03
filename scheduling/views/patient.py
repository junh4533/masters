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

#################### patients' views ####################
def patient_portal(request):
    data_input = request.GET.get('date')
    if not data_input:
        data_input = date.today()
        print(data_input)
    doctor = request.user.patient.doctor
    appointments = Appointment.objects.filter(patient=request.user.patient.pid).filter(date__gte=datetime.now()-timedelta(days=1)).order_by('date','timeslot')
    selected_date = Appointment.objects.filter(date = data_input).values_list('timeslot', flat=True)
    available_appointments = [(value, time) for value, time in Appointment.TIMESLOT_LIST if value not in selected_date]

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            success = "Appointment Created!"
            args = {
                "success":success,
                "form" : form,
                "appointments" : appointments, 
                "available_appointments" : available_appointments, 
                "data_input": data_input, 
                "doctor": doctor, 
            }
            email = str(request.user.email)
            message = 'Appointment scheduled for ' + str(form.cleaned_data['date']) + " " + str(form.instance.get_timeslot_display())
            send_mail('KungFuMD Appointment', message, 'EZDoctPortal@gmail.com', [email])
            print(email)
            print(message)
            return render(request, 'scheduling/patient.html', args)
    else:
        form = AppointmentForm(request.POST)
        args = {
            "form" : form, 
            "appointments" : appointments, 
            "available_appointments" : available_appointments, 
            "data_input": data_input, 
            "doctor": doctor, 
        }
        return render(request, 'scheduling/patient.html', args)