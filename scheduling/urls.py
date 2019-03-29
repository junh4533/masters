# app url
from django.conf.urls import url, include
from django.urls import path
from . import views

#load methods from views.py
urlpatterns = [
    path('', views.index, name='index'), 
    path('add_user/', views.SignUp.as_view(), name='add_user'), 
    path('add_user/add_doctor/', views.AddDoctor.as_view(), name='add_doctor'), 
    path('doctor/', include(([
        path('appointments/', views.appointments, name='appointments'),
        path('patients/', views.patients, name='patients'),
        path('reports/', views.reports, name='reports'),
        path('settings/', views.settings, name='settings'),
        path('login/', views.user_login, name='login'),
        path('home/', views.doctor_portal,name='doctor_portal'),
        # path('edit/', views.EditInfo.as_view(), name='edit'),
    ]))),
    path('patient/', include(([
        path('appointments/', views.appointments, name='appointments'),
        path('appointments/make_appointment', views.AppointmentForm.as_view(), name='make_appointments'),
        path('login/', views.user_login, name='login'),
        path('home/',views.patient_portal, name='patient_portal'),
        # path('edit/', views.EditInfo.as_view(), name='edit'),
    ]))),
    path('assistant/', include(([
        path('appointments/', views.appointments, name='appointments'),
        path('appointments/make_appointment', views.AppointmentForm.as_view(), name='make_appointments'),
        path('patients/', views.patients, name='patients'),
        path('reports/', views.reports, name='reports'),
        path('settings/', views.settings, name='settings'),
        path('login/', views.user_login, name='login'),
        path('home/', views.assistant_portal,name='assistant_portal'),
        # path('edit/', views.EditInfo.as_view(), name='edit'),
        path('add_user/', views.SignUp.as_view(), name='add_user'), 
        # path('add_info/', views.EditInfo.as_view(), name='add_info'),
    ]))),
]