from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),    
    path('about/', views.about, name='about'),
    path('fetch-data', views.fetch_data, name='fetch_data'),
]