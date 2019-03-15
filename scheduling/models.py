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
    active = models.BooleanField(default=True)
    phone = models.CharField(max_length=10)
    id = models.IntegerField(unique=True, primary_key=True)
    phone = models.CharField(max_length=10)
    specialty = models.CharField(max_length=20)
    # start_time = models.TimeField(null=True)
    # end_time = models.TimeField(null=True)
    # days_available = models.DateTimeField(null=True)
    appointments_per_day = models.IntegerField(null=True,max_length=1)

    def __str__(self):
        return self.first_name  + " " + self.last_name

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

    user = models.ManyToManyField(User, related_name='appointment')
    timeslot = models.IntegerField(choices=TIMESLOT_LIST, null=True)

    def __str__(self):
        return str(self.timeslot)



