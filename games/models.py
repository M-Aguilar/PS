from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

#wondering if it would be wise to allow for uploading a js file
class Game(models.Model):
	name = models.CharField(max_length=50)
	text = models.TextField(max_length=500, blank=True)
	path = models.SlugField(max_length=50, unique=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	js = models.FilePathField(path='static/games', recursive=True, blank=True, match=".*js")

	def __str__(self):
		return self.name

class Score(models.Model):
	initial = models.CharField(max_length=3)
	player = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	score = models.IntegerField()
	total = models.IntegerField()
