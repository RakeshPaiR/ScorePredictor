from django.contrib import admin
from django.urls import path
from . import views

app_name = 'football'

urlpatterns = [
    path('',views.index,name='index'),
]