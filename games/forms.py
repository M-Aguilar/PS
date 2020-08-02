from django import forms

from .models import Game, Rating

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name','path','js', 'text']
        labels = {'text':'Description'}

class RatingForm(forms.ModelForm):
	class Meta:
		model = Rating
		fields = ['rating']
		widgets = {'rating':forms.Select()}
		labels = {'rating':'Your Rating'}