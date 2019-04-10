# app urls
from django.conf.urls import url, include
from django.urls import path
from . import views

#load methods from views.py
urlpatterns = [
    path('', views.index, name='index'), 
    path('doctor/', include(([
        path('home/', views.doctor_portal,name='doctor_portal'),
        path('appointments/', views.doctor_appointments, name='doctor_appointments'),
        path('patients/', views.doctor_patients, name='doctor_patients'),
        path('reports/', views.reports, name='doctor_reports'),
        path('settings/', views.settings, name='doctor_settings'),
        path('profile/', views.doctor_profile, name='doctor_profile'),
        path('profile/edit/', views.add_info, name='add_info'),
    ]))),
    path('patient/', include(([
        path('home/',views.patient_portal, name='patient_portal'),
        path('make_appointment', views.AppointmentForm.as_view(), name='make_appointments'),
        # path('edit/', views.EditInfo.as_view(), name='edit'),
    ]))),
    path('assistant/', include(([
        path('home/', views.assistant_portal,name='assistant_portal'),
        path('appointments/', views.all_appointments, name='all_appointments'),
        path('appointments/make_appointment', views.AppointmentForm.as_view(), name='make_appointments'),
        path('patients/', views.all_patients, name='all_patients'),
        path('doctors/', views.doctors, name='all_doctors'),
        path('reports/', views.reports, name='assistant_reports'),
        path('settings/', views.settings, name='assistant_settings'),
        path('add_user/', views.SignUp.as_view(), name='add_user'), 
        # path('change/',views.doctorupdate, name='drupdate'),
        # path('add_user/', views.SignUp.as_view(), name='add_user'), 
        # path('add_user/add_doctor/', views.AddDoctor.as_view(), name='add_doctor'), 
        # path('edit/', views.EditInfo.as_view(), name='edit'),
    ]))),
]