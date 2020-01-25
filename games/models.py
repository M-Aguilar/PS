from django.db import models

# Create your models here.

class Game(models.Model):
    text = models.CharField(max_length=50)

    def __str__(self):
       return self.text

    class Score(models.Model):
        name = models.CharField(max_length=3)
        score = models.DecimalField(max_digits = 5, decimal_places=2)
