from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os

class Projector(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	admin = models.BooleanField(default=False)

#WHAT IS GOING ON!!! I FOUND THE PROBLEM. This may need to be changed for the regular server
def user_directory_path(instance, filename):
    try:
        return '/user_{0}/{1}/{2}'.format(instance.project.owner.id, instance.project.id, filename)
    except AttributeError:
        print("Attribute Error 1")
        pass
    try:
        return '/user_{0}/{1}/{2}'.format(instance.owner.id, 'banner', filename)
    except AttributeError:
        print("Attribute Error 2")
        pass

def images_path():
    return settings.MEDIA_ROOT
# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=100, blank=True)
    public = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    banner = models.ImageField(upload_to=user_directory_path, blank=True)
    banner_path = models.FilePathField(path=images_path, match=".*\.*jpg$|.*\.*jpeg$|.*\.*png$|.*\.*gif$", recursive=True, blank=True)

    def __str__(self):
        return self.title

    #this is the answer
    def banner_p(self):
        return self.banner_path[self.banner_path.index(settings.MEDIA_URL):]
'''
    def images_path(self):
        if settings.DEBUG:
            return os.path.join(settings.MEDIA_ROOT,settings.MEDIA_URL,'user_',self.owner.id)
        else:
            return os.path.join(settings.MEDIA_ROOT,'user_',self.owner.id)
'''

class Post(models.Model):
    text = models.CharField(max_length=250, blank=True)
    public = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    #TODO I want upload and filepathfields. It looks like the only way I can do it is to 
    #manage it at the views level
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    image_path = models.FilePathField(path=images_path, match=".*\.*jpg$|.*\.*jpeg$|.*\.*png$|.*\.*gif$", recursive=True, blank=True)

    pdf = models.FileField(upload_to=user_directory_path, blank=True)
    pdf_path = models.FilePathField(path=images_path, match=".*\.pdf$", recursive=True, blank=True)

    class Meta:
        verbose_name_plural = 'posts'

    def image_p(self):
        return self.image_path[self.image_path.index(settings.MEDIA_URL):]
    
    def pdf_p(self):
        return self.pdf_path[self.pdf_path.index(settings.MEDIA_URL):]

    def __str__(self):
        return self.text[:50] + "..."
'''
    def images_path(self):
        if settings.DEBUG:
            return os.path.join(settings.MEDIA_ROOT,settings.MEDIA_URL,'user_',self.project.owner.id)
        else:
            return os.path.join(settings.MEDIA_ROOT,'user_',self.project.owner.id)
'''
