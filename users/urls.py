"""Defines URL patterns for users"""
from django.urls import path, include
from . import views


app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
    path('profile/<int:profile_id>/', views.viewIndex, name='loginProfile'),
    path('newprofile/', views.newProfile, name='newProfile'),
]