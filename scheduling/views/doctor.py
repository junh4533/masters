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

#################### doctors' views ####################
def doctor_portal(request):
    appointments = Appointment.objects.filter(doctor=request.user.doctor.upin).order_by('date','timeslot')[:4]
    appointments_today = Appointment.objects.filter(doctor=request.user.doctor.upin).filter(date=date.today()).count()
    # print()
    print(appointments_today)
    args = {"appointments" : appointments, "appointments_today":appointments_today}
    return render(request, 'scheduling/doctor.html', args)