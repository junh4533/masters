# app urls
from django.conf.urls import url, include
from django.urls import path
from scheduling.views import *
from django.contrib import admin

#load methods from views.py
urlpatterns = [
    path('', user.index, name='index'),
    path('home/', include(([
        path('our_team/',user.our_team,name='our_team'),
        path('admin/', admin.site.urls), #admin portal
    ]))),
    path('doctor/', include(([
        path('home/', doctor.doctor_portal,name='doctor_portal'),
        path('appointments/', user.all_appointments, name='all_appointments'),
        path('patients/', user.patients, name='patients'),
        path('reports/', user.reports, name='reports'),
        path('settings/', user.settings, name='doctor_settings'),
        path('profile/', user.edit_profile, name='edit_profile'),
        path('password/', user.change_password, name='change_password'),
    ]))),
    path('patient/', include(([
        path('home/',patient.patient_portal, name='patient_portal'),
        path('profile/', user.edit_profile, name='edit_profile'),
        path('password/', user.change_password, name='change_password'),
    ]))),
    path('assistant/', include(([
        path('home/', assistant.assistant_portal, name='assistant_portal'),
        path('appointments/', user.all_appointments, name='all_appointments'),
        path('make_appointments/', assistant.make_appointments, name='make_appointments'),
        # path('delete_appointment/', user.delete_appointment, name='delete_appointment'),
        path('patients/', user.patients, name='patients'),
        path('doctors/', assistant.doctors, name='all_doctors'),
        path('reports/', user.reports, name='reports'),
        path('add_user/', assistant.add_user, name='add_user'), 
        path('add_doctor_info/', assistant.add_doctor_info, name='add_doctor_info'), 
        path('add_patient_info/', assistant.add_patient_info, name='add_patient_info'),
        path('profile/', user.edit_profile, name='edit_profile'),
        path('password/', user.change_password, name='change_password'),
    ]))),
]

