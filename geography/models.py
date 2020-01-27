from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#change project text to textarea and move text to title
class Project(models.Model):
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=100, blank=True)
    public = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.CharField(max_length=250)
    public = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.text[:50] + "..."
