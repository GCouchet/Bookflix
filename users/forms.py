from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
import datetime

# Extendemos del original
class UCFWithExtends(UserCreationForm):
    # Ahora el campo username es de tipo email y cambiamos su texto
    email = forms.EmailField(label="Correo electrónico")
    first_name = forms.CharField(max_length=30, label="Nombre")
    last_name = forms.CharField(max_length=30, label="Apellido")
    age = forms.IntegerField(label="Edad")

    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    credit_Card = forms.IntegerField(label="N° de tarjeta")
    expired_Card = forms.DateField(label="Fecha de vencimiento (aaaa-mm-dd)", initial=datetime.date.today)
    secCode_Card = forms.CharField(widget=forms.PasswordInput, label="Código de seguridad")

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "age", "password1", "password2", "credit_Card", "expired_Card", "secCode_Card"]