from django.contrib.auth.models import User
from scheduling.models import *
import django_filters
from django import template
from django import forms

class UserFilter(django_filters.FilterSet):

    class Meta:
        model = Appointment
        fields = ['doctor','patient','date']
        filter_overrides = {
            models.CharField:{
                'filter_class':django_filters.CharFilter,
                'extra': lambda f:{
                    'lookup_expr':'icontain',
                }
            },
            models.DateField:{
                'filter_class':django_filters.DateFilter,
                'extra': lambda f:{
                    'widget': forms.TextInput(
                        attrs={'type': 'date'}
                    )
                }
            }
        }

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})