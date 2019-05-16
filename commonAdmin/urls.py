from django.contrib import admin
from django.urls import path
from . import views

app_name = 'commonAdmin'

urlpatterns = [
    path('',views.index,name='index'),
    path('abc/',views.getMatches,name='getMatches'),
    path('def/',views.storeMatches,name='storeMatches'),
]