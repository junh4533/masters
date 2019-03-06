from scheduling import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

#connect to the url.py in the app
urlpatterns = [
    url(r'', include('scheduling.urls')), #index page
    url(r'^admin/', admin.site.urls), #admin portal
    url(r'^accounts/', include('django.contrib.auth.urls')), #login and logout   
    path('users/', include('scheduling.urls')), 
    path('users/', include('django.contrib.auth.urls')), 
] 