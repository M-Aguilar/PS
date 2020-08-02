from django.shortcuts import render, get_object_or_404
from .models import Game, Score, Rating
from .forms import GameForm, RatingForm
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
import csv
import os
from django.conf import settings
from django.urls import reverse
# Create your views here.

def rate(game):
	ratings = Rating.objects.filter(game=game)
	total = 0
	if ratings.count() > 0:
		rate_count = len(ratings)
		for rating in ratings:
			total += rating.rating
		return {'total':total, 'rate_count':rate_count}
	return None

#IN THE WORKS
def index(request):
	games = Game.objects.all()
	for game in games:
		game.rating = rate(game)
	context = {'nbar': 'games', 'games' : games}
	return render(request, 'games/index.html', context)

#a lot going on in one form it may be worth delegating actions but will see
@login_required
def rating(request, path):
	game = get_object_or_404(Game, path=path)
	rating = rate(game)
	check = Rating.objects.filter(user=request.user,game=game)
	if request.method!= 'POST':
		if check.count() > 0:
			form = RatingForm(instance=check.get(user=request.user))
		else:
			form = RatingForm()
	else:
		form = RatingForm(data=request.POST)
		if check.count()>0:
			original = check.get(user=request.user)
			if form.is_valid():
				original.rating = request.POST['rating']
				original.save()
				return HttpResponseRedirect(reverse('game', args=[path]))
		else:
			if form.is_valid():
				new_rating = form.save(commit=False)
				new_rating.user = request.user
				new_rating.game = game
				new_rating.save()
				return HttpResponseRedirect(reverse('game', args=[path]))
	context = {'nbar':'games','game':game, 'form':form,'rating':rating}
	return render(request,'games/rating.html',context)

#When creating other games this may need to be chnged. 
#this probabl needs to be changed
def game(request, path):
	ojs = {}
	game = get_object_or_404(Game, path=path)
	rating = rate(game)
	#may need to add a try except for none js games
	try:
		with open(os.path.join(settings.STATIC_ROOT, 'games', (path + '.csv')), newline='') as c:
			f = csv.reader(c)
			for i in f:
				ojs[i[2]] = list(i[:2])
	except FileNotFoundError:
		pass
	context = {'nbar': 'games', 'game': game, 'gps': ojs, 'rating':rating}
	return render(request, 'games/game.html', context)

@login_required
def edit_game(request, path):
	g = get_object_or_404(Game, path=path)
	if g.creator != request.user:
		raise Http404
	if request.method != 'POST':
		form = GameForm(instance=g)
	else:
		form = GameForm(instance=g, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('games'))
	context = {'game':g, 'form': form, 'nbar': 'games'}
	return render(request, 'games/edit_game.html', context)

@login_required
def new_game(request):
	if not request.user.projector.admin:
		raise Http404
	if request.method != 'POST':
		form = GameForm()
	else:
		form = GameForm(data=request.POST)
		if form.is_valid():
			new_g = form.save(commit=False)
			new_g.creator = request.user
			new_g.save()
			return HttpResponseRedirect(reverse('games'))
	context = {'form': form,'nbar':'games'}
	return render(request, 'games/new_game.html', context)
