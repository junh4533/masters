# app urls
from django.conf.urls import url, include
from django.urls import path
from . import views

#load methods from views.py
urlpatterns = [
    path('', views.index, name='index'),
    path('doctor/', include(([
        path('home/', views.doctor_portal,name='doctor_portal'),
        path('appointments/', views.all_appointments, name='all_appointments'),
        path('patients/', views.patients, name='patients'),
        path('reports/', views.reports, name='reports'),
        path('settings/', views.settings, name='doctor_settings'),
        path('profile/', views.edit_profile, name='edit_profile'),
        path('password/', views.change_password, name='change_password'),
    ]))),
    path('patient/', include(([
        path('home/',views.patient_portal, name='patient_portal'),
        path('profile/', views.edit_profile, name='edit_profile'),
        path('password/', views.change_password, name='change_password'),
    ]))),
    path('assistant/', include(([
        path('home/', views.assistant_portal, name='assistant_portal'),
        path('appointments/', views.all_appointments, name='all_appointments'),
        path('make_appointments/', views.make_appointments, name='make_appointments'),
        path('patients/', views.patients, name='patients'),
        path('doctors/', views.doctors, name='all_doctors'),
        path('reports/', views.assistant_report, name='reports'),
        path('add_user/', views.add_user, name='add_user'), 
        path('add_doctor_info/', views.add_doctor_info, name='add_doctor_info'), 
        path('add_patient_info/', views.add_patient_info, name='add_patient_info'),
        path('profile/', views.edit_profile, name='edit_profile'),
        path('password/', views.change_password, name='change_password'),
    ]))),
]

