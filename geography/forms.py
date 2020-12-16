from django import forms

from .models import Project, Post

class ProjectForm(forms.ModelForm):
    #banner = forms.ImageField(label="Choose your image", help_text="Hope this helps")
    class Meta:
        model = Project
        fields = ['title', 'text', 'public','url','banner','banner_path']
        labels = {'text': 'Description', 'banner_path':'', 'banner':''}

        widgets = {
            'title': forms.TextInput(attrs={'autofocus':'autofocus','class':'form-control','rows':1,'placeholder':'Title'}),
            'text': forms.Textarea(attrs={'class':'form-control','rows':2,'placeholder':'Description'}),
            'public': forms.CheckboxInput(attrs={'class':'form-check'}),
            'url': forms.URLInput(attrs={'class':'form-control','placeholder':'https://...'}),
            'banner':forms.FileInput(attrs={'class':'custom-file-input'}),
            'banner_path':forms.Select(attrs={'class':'form-control custom-select'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'public','project', 'image', 'pdf', 'image_path', 'pdf_path']
        labels = {'text':'', 'image_path':'', 'image':'','pdf_path':'pdf'}
        widgets = {
            'text': forms.Textarea(attrs={'cols':80,'autofocus':'autofocus','class':'form-control'}),
            'public': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'project': forms.Select(attrs={'class': 'form-control custom-select'}),
            'image': forms.ClearableFileInput(attrs={'class':'custom-file-input'}),
            'pdf': forms.FileInput(attrs={'class':'custom-file-input'}),
            'image_path': forms.Select(attrs={'class': 'form-control custom-select'}),
            'pdf_path': forms.Select(attrs={'class': 'form-control custom-select'}),
        }