from django import forms

from .models import Project, Post

class ProjectForm(forms.ModelForm):
    #banner = forms.ImageField(label="Choose your image", help_text="Hope this helps")
    class Meta:
        model = Project
        fields = ['title', 'text', 'public','url','banner']
        labels = {'text': 'Description', 'banner':''}

        widgets = {
            'title': forms.TextInput(attrs={'autofocus':'autofocus','class':'form-control','rows':1,'placeholder':'Title'}),
            'text': forms.Textarea(attrs={'class':'form-control','rows':2,'placeholder':'Description'}),
            'public': forms.CheckboxInput(attrs={'class':'form-check'}),
            'url': forms.URLInput(attrs={'class':'form-control','placeholder':'https://...'}),
            'banner':forms.ClearableFileInput(),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'public','project', 'image', 'pdf']
        labels = {'text':'', 'image':''}
        widgets = {
            'text': forms.Textarea(attrs={'cols':80,'autofocus':'autofocus','class':'form-control'}),
            'public': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'project': forms.Select(attrs={'class': 'form-control custom-select'}),
            'image': forms.ClearableFileInput(),
            'pdf': forms.ClearableFileInput(),
        }