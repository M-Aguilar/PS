from django.db import models
from django.conf import settings
from django.contrib.auth.models import User 

def user_directory_path(instance, filename):
    return settings.MEDIA_ROOT + '/user_{0}/{1}'.format(instance.user.id, filename)

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
    #banner = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.CharField(max_length=250)
    public = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    #image = models.ImageField(upload_to=user_directory_path)

    class Meta:
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.text[:50] + "..."
