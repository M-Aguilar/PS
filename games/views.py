from django.shortcuts import render
from .models import Game, Score
# Create your views here.

def index(request):
	games = Game.objects.all()
	context = {'nbar': 'games', 'games' : games}
	return render(request, 'games/index.html', context)

def game(request, game_id):
	game = Game.objects.get(id=game_id)
	scores = Score.objects.all().filter(game=game)
	context ={'nbar': 'games', 'game': game, 'scores': scores}
	return render(request, 'games/game.html', context)