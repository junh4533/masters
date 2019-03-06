# app url
from django.conf.urls import url, include
from django.urls import path
from . import views

#load methods from views.py
urlpatterns = [
    path('', views.index, name='index'), 
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('appointments/', views.appointments, name='appointments'),
    path('patients/', views.patients, name='patients'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),
]