#!/bin/bash

python3 -m venv $1
source $1/bin/activate
pip install Django
pip install django-bootstrap4
django-admin startproject $2 .
python manage.py startapp $3
python manage.py migrate
python manage.py createsuperuser
cd $3/
echo "from django import forms
from .models import x" > forms.py
echo "from django.urls import path
from . import views

app_name = '$3'
urlpatterns = [
    path('', views.index, name='index'),
]" > urls.py
echo "from django.shortcuts import render, redirect


def index(request):
    return render(request, '$3/index.html')
" > views.py
mkdir templates
cd templates/
mkdir $3
cd $3/
echo '{% load bootstrap4 %}

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>Titulo</title>
  {% bootstrap_css %}
  {% bootstrap_javascript jquery="full" %}
</head>
<body>
  <nav class="navbar navbar-expand-md navbar-light bg-light mb-4 border">
    <a class="navbar-brand" href="{% url "XXXX:index" %}">XXXX</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse"
      data-target="#navbarCollapse" aria-controls="navbarCollapse"
      aria-expanded="false" aria-laber="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarCollapse">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <a class="nav-link" href="{% url "XXXX:index" %}">YYYYY</a></li>
        <li class="nav-item">
          <a class="nav-link" href="{% url "XXXX:index" %}">YYYYY</a></li>
        <li class="nav-item">
          <a class="nav-link" href="{% url "XXXX:index" %}">YYYYY</a></li>
      </ul>
    </div>
  </nav>
  <main role="main" class="container">
    <div class="pb-2 mb-2 border-bottom">
      {% block page_header %}{% endblock page_header %}
    </div>
    <div>
      {% block content %}{% endblock content %}
    </div>
  </main>

</body>

</html>' > base.html
echo '{% extends "XXXX/base.html" %}

{% block page_header %}
  <div class="jumbotron">
    <h1 class="display-3">XXXX.</h1>
    <p class="lead">XXXXX sirve para ...</p>
      <a class="btn btn-lg btn-primeary" href="{% url "XXXX:index" %}"
        role="button">Mis XXXX &raquo;</a>
  </div>
{% endblock page_header %}
' > index.html
