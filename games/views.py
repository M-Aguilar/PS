from django.shortcuts import render
from .models import Game, Score
from .forms import GameForm
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
import csv
import os
from django.urls import reverse
# Create your views here.

def index(request):
	games = Game.objects.all()
	context = {'nbar': 'games', 'games' : games}
	return render(request, 'games/index.html', context)

def game(request, path):
	ojs = {}
	game = Game.objects.get(path=path)
	#may need to add a try except for none js games
	with open('/home/pi/site/games/static/games/'+str(game.path)+'.csv', newline='') as c:
		f = csv.reader(c)
		for i in f:
			ojs[i[2]] = list(i[:2])
	scores = Score.objects.all().filter(game=game)
	context ={'nbar': 'games', 'game': game, 'scores': scores, 'gps': ojs}
	return render(request, 'games/game.html', context)

def new_game(request):
	if not request.user.projector.admin:
		raise Http404
	if request.method != 'POST':
		form = GameForm()
	else:
		form = GameForm(data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('games'))
	context = {'game': game,'form': form,'nbar':'games'}
	return render(request, 'games/new_game.html', context)

@login_required
def edit_game(request, path):
	game = Game.objects.get(path=path)
	if game.creator != request.user:
		raise Http404
	if request.method != 'POST':
		form = GameForm(instance=game)
	else:
		form = GameForm(instance=game, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('games'))
	context = {'game':game, 'form': form, 'nbar': 'games'}
	return render(request, 'games/edit_game.html', context)