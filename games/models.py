from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

#wondering if it would be wise to allow for uploading a js file
class Game(models.Model):
	name = models.CharField(max_length=50)
	text = models.TextField(max_length=500, blank=True)
	path = models.SlugField(max_length=50, unique=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	js = models.FilePathField(path=os.path.join(settings.STATIC_ROOT,'games'), recursive=True, blank=True, match=".*js")

	def js_p(self):
		return self.js[self.js.index(settings.STATIC_URL):]

	def __str__(self):
		return self.name

class Score(models.Model):
	initial = models.CharField(max_length=3)
	player = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	score = models.IntegerField()
	total = models.IntegerField()

class Rating(models.Model):
	ZERO = 0
	ONE = 1
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	choices = [
		(ZERO,'0'),
		(ONE,'1'),
		(TWO,'2'),
		(THREE,'3'),
		(FOUR,'4'),
		(FIVE,'5'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	rating = models.IntegerField(choices=choices, blank=True, validators=[MaxValueValidator(5),MinValueValidator(0)])