from django.contrib.auth.models import User
from scheduling.models import *
import django_filters
from django import template

class UserFilter(django_filters.FilterSet):
    date = django_filters.DateFilter 

    class Meta:
        model = Appointment
        fields = ['doctor','patient','date']

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})