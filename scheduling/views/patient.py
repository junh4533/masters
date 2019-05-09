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

# #Chart
# from django.db.models import Count
# import json

# #Reports
# from scheduling.filter import UserFilter

#etc
from django.utils.dateparse import parse_date
from django.core.mail import send_mail
from datetime import datetime, timedelta

#################### patients' views ####################
def patient_portal(request):
    data_input = request.GET.get('date')
    if not data_input:
        data_input = str(date.today())
        date_object = date.today()
        print(data_input, date_object)
    else:
        date_object = parse_date(data_input)
    doctor = request.user.patient.doctor
    appointments = Appointment.objects.filter(patient=request.user.patient.pid).filter(date__gte=datetime.now()-timedelta(days=1)).order_by('date','timeslot')
    selected_date = Appointment.objects.filter(date = data_input).values_list('timeslot', flat=True)
    available_appointments = [(value, time) for value, time in Appointment.TIMESLOT_LIST if value not in selected_date]

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            success = "Appointment Scheduled"
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
            send_mail('EZDoct Appointment', message, 'EZDoctPortal@gmail.com', [email])
            print(email)
            print(message)
            return render(request, 'scheduling/patient.html', args)
        else:
            print(form.errors)
    else:
        if 'appointment_id' in request.GET:
            delete = Appointment.objects.get(id=request.GET.get('appointment_id'))
            Appointment.objects.filter(id=request.GET.get('appointment_id')).delete()
            email = str(request.user.email)
            message = "The appointment for "  + str(delete.date) + " " + str(delete.get_timeslot_display()) + " has been cancelled."
            send_mail('EZDoct Appointment', message, 'EZDoctPortal@gmail.com', [email])
            print("appointment deleted", email, message)
        form = AppointmentForm(request.POST)
        args = {
            "form" : form, 
            "appointments" : appointments, 
            "available_appointments" : available_appointments, 
            "data_input": data_input, 
            "date_object": date_object,
            "doctor": doctor, 
        }
        return render(request, 'scheduling/patient.html', args)