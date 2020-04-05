"""Defines URL patterns for users"""
from django.urls import path, include
from . import views


app_name = 'profiles'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('select/', views.selectProfile, name='selectProfile'),
    path('<int:profile_id>/', views.viewIndex, name='loginProfile'),
    path('new/', views.newProfile, name='newProfile'),
    path('delete/<int:profile_id>/', views.deleteProfile, name='deleteProfile'),
]