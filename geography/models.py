from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os

class Projector(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	admin = models.BooleanField(default=False)

def user_directory_path(instance, filename):
    try:
        return 'user_{0}/{1}/{2}'.format(instance.project.owner.id, instance.project.id, filename)
    except AttributeError:
        print("Attribute Error: user_directory_path 1")
        pass
    try:
        return 'user_{0}/{1}/{2}/{3}'.format(instance.owner.id, instance.id, 'banner', filename)
    except AttributeError:
        print("Attribute Error: user_directory_path 2")
        pass

def images_path():
    return settings.MEDIA_ROOT

class Project(models.Model):
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=100, blank=True)
    public = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    banner = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.CharField(max_length=250, blank=True)
    public = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    pdf = models.FileField(upload_to=user_directory_path, blank=True)

    class Meta:
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.text[:50] + "..."

