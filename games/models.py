from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#wondering if it would be wise to allow for uploading a js file
class Game(models.Model): 
    text = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
       return self.text

class Score(models.Model):
    initial = models.CharField(max_length=3)
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits = 5, decimal_places=2)
