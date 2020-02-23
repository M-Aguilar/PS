from django import forms

from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name','path','js', 'text']
        labels = {'text':'Description'}