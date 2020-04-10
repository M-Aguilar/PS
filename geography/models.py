from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os

#this needs to be cleaned up
#Currently we have user/project/<images>
#               and user/

class Projector(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	admin = models.BooleanField(default=False)

#WHAT IS GOING ON!!! I FOUND THE PROBLEM. This may need to be changed for the regular server
def user_directory_path(instance, filename):
    try:
        return settings.MEDIA_ROOT + '/user_{0}/{1}/{2}'.format(instance.project.owner.id, instance.project.id, filename)
    except AttributeError:
        print("Attribute Error 1")
        pass
    try: #settings.MEDIA_ROOT +
        return settings.MEDIA_ROOT + '/user_{0}/{1}/{2}'.format(instance.owner.id, 'banner', filename)
    except AttributeError:
        print("Attribute Error 2")
        pass

def images_path():
    return os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,'media/user_2')

# Create your models here.
#change project text to textarea and move text to title
class Project(models.Model):
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=100, blank=True)
    public = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    banner = models.ImageField(upload_to=user_directory_path, blank=True)
    banner_path = models.FilePathField(path=images_path, match=".*\.*g$", recursive=True, blank=True)

    def __str__(self):
        return self.title

    def banner_p(self):
        return self.banner_path[len('/home/pi/site'):]

class Post(models.Model):
    text = models.CharField(max_length=250)
    public = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    #TODO I want upload and filepathfields. It looks like the only way I can do it is to 
    #manage it at the views level
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    image_path = models.FilePathField(path=images_path, match=".*\.*g$", recursive=True, blank=True)

    pdf = models.FileField(upload_to=user_directory_path, blank=True)
    pdf_path = models.FilePathField(path=images_path, match=".*\.pdf$", recursive=True, blank=True)


    class Meta:
        verbose_name_plural = 'posts'

    def image_p(self):
        return self.image_path[len('/home/pi/site'):]

    def pdf_p(self):
        return self.pdf_path[len('/home/pi/site'):]

    def __str__(self):
        return self.text[:50] + "..."
