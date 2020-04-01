from django import forms
from .models import Comment, Calification


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'spoiler']
        labels = {'text': '', 'spoiler': 'Check if yor comment has any spoiler'}


class CalificationForm(forms.ModelForm):
    class Meta:
        model = Calification
        CHOICES = (
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (6, '6'),
            (7, '7'),
            (8, '8'),
            (9, '9'),
            (10, '10'),
        )
        fields = ['value']
        widgets = {'value': forms.Select(choices=CHOICES)}
