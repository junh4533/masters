#contains all the models and database structure
from django.db import models
from datetime import *
from django.contrib.auth.models import Group, User, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.is_patient = True
    username = models.CharField(max_length=50)
    pid = models.AutoField(unique=True, primary_key=True) #patient identification
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=70, unique=True)
    active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ('username')
    USERNAME_FIELD = 'username'
    #gives the patient object his/her name
    def __str__(self):
        return self.first_name  + " " + self.last_name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.is_doctor = True
    upin = models.AutoField(unique=True, primary_key=True) #unique physician identification number
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    expertise = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=70, unique=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    days_available = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ('username')
    USERNAME_FIELD = 'username'

    # gives the doctor object his/her name
    def __str__(self):
        return self.first_name  + " " + self.last_name
        # doctor_group = Group.objects.get(name='Doctors') 
        # doctor_group.user_set.add(self)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, related_name='patient_appointment', on_delete="DO_NOTHING")
    doctor = models.ForeignKey(Doctor, related_name='doctor_appointment', on_delete="DO_NOTHING")
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.timeslot) + " - " + str(self.patient) + "- Dr. " + str(self.doctor)
        



