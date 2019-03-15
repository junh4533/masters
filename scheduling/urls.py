# app url
from django.conf.urls import url, include
from django.urls import path
from . import views

#load methods from views.py
urlpatterns = [
    path('', views.index, name='index'), 
    path('signup/doctor/', views.DoctorSignUp.as_view(), name='doc_signup'),
    path('signup/patient/', views.PatientSignUp.as_view(), name='pn_signup'),
    path('appointments/', views.appointments, name='appointments'),
    path('patients/', views.patients, name='patients'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),
]