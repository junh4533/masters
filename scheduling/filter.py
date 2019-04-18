from django.contrib.auth.models import User
from scheduling.models import *
import django_filters

class UserFilter(django_filters.FilterSet):
    date = django_filters.DateFilter 

    class Meta:
        model = Appointment
        fields = ['doctor','patient','date']