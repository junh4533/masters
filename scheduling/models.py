#contains all the models and database structure
from django.db import models
from datetime import *
from django.contrib.auth.models import Group, User, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager
from datetime import date, datetime

class User(AbstractUser):
    users = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('assistant', 'Assistant'),
    )

    user_type = models.CharField(choices=users, max_length=9, default='patient')

    #return the users' name
    def __str__(self):
        return self.first_name  + " " + self.last_name

class Doctor(models.Model):
    upin = models.AutoField(primary_key=True) #unique physician identification number
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.user_type = "doctor"
    specialty = models.CharField(max_length=20)
    appointments_per_hour = models.IntegerField(null=True)
    picture = models.ImageField(upload_to = 'doctors', default = '')

    #return the doctors' name
    def __str__(self):
        return str(self.user)

class Patient(models.Model):
    pid = models.AutoField(unique=True, primary_key=True) #patient identification
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, related_name='patient_doctor', null=True)
    user.user_type = "patient"
    picture = models.ImageField(upload_to = 'patients', default = '')

    #return the patients' name
    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "doctor":
            Doctor.objects.create(user=instance)
        elif instance.user_type == "patient":
            Patient.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == "doctor":
        instance.doctor.save()
    elif instance.user_type == "patient":
        instance.patient.save()

class Appointment(models.Model):
    TIMESLOT_LIST = (
        (1, '10:00 – 11:00'),
        (2, '11:00 – 12:00'),
        (3, '12:00 – 13:00'),
        (4, '13:00 – 14:00'),
        (5, '14:00 – 15:00'),
        (6, '15:00 – 16:00'),
        (7, '16:00 – 17:00'),
        (8, '17:00 – 18:00'),
        (8, '18:00 – 19:00'),
    )

    date = models.DateField(default=date.today)
    timeslot = models.IntegerField(choices=TIMESLOT_LIST, null=True)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, related_name='appointment_doctor')
    # doctor =  models.OneToOneField(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE, related_name='appointment_patient')
    # patient =  models.OneToOneField(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.doctor) + " " + str(self.patient) + " - " + str(self.get_timeslot_display()) 



