from django import forms
from .models import Profile

class creationProfile(forms.ModelForm):
    name = forms.CharField(max_length=30, label="Nombre del perfil")

    class Meta:
        model = Profile
        fields = ["name"]
        exclude = ["user"]