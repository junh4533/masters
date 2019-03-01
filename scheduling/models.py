#contains all the models and database structure
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

# class Patient(models.Model):
#     pid = models.AutoField(primary_key=True) #patient identification
#     patient_fn = models.CharField(max_length=30)
#     patient_ln = models.CharField(max_length=30)
#     phone = PhoneNumberField(unique=True)
#     email = models.EmailField(max_length=70,unique=True)
    
#     # gives the patient object his/her name
#     def __str__(self):
#         return self.patient_fn  + " " + self.patient_ln

class Patient(AbstractUser):
    pid = models.AutoField(primary_key=True) #patient identification
    patient_fn = models.CharField(max_length=30)
    patient_ln = models.CharField(max_length=30)
    phone = PhoneNumberField(unique=True)

    #gives the patient object his/her name
    def __str__(self):
        return self.patient_fn  + " " + self.patient_ln

class Doctor(models.Model):
    upin = models.AutoField(primary_key=True) #unique physician identification number
    doctor_fn = models.CharField(max_length=30)
    doctor_ln = models.CharField(max_length=30)
    expertise = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, unique=True)
    # availability = 

    # gives the doctor object his/her name
    def __str__(self):
        return self.doctor_fn + " " + self.doctor_ln

class Appointment(models.Model):
    # patient = models.ForeignKey(Patient,on_delete="DO_NOTHING")
    doctor = models.ForeignKey(Doctor,on_delete="DO_NOTHING")
    timeslot = models.DateTimeField()

    def __str__(self):
        return str(self.timeslot) + " - " + str(self.patient) + "- Dr. " + str(self.doctor)
        



