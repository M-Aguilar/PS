from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Page(models.Model):
    name = models.CharField(max_length=75)
    slug_url = models.SlugField(max_length=75, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_edited = models.DateTimeField(auto_now=True)
    navbar = models.BooleanField(default=False)
    html = models.TextField()

    def __str__(self):
        return self.name

def validate_page(value):
    return None