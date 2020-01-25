from django import forms

from .models import Project, Post

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['text', 'public']
        lables = {'text': ''}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels = {'text':''}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}
