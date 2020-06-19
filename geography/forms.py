from django import forms

from .models import Project, Post

class ProjectForm(forms.ModelForm):
    #banner = forms.ImageField(label="Choose your image", help_text="Hope this helps")
    class Meta:
        model = Project
        fields = ['title', 'text', 'public','url','banner','banner_path']
        labels = {'text': 'Description', 'banner_path':'', 'banner':''}


        #currently unused
        def banner_choices():
            return [widgets['banner'], widget['banner_path']]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'public','project', 'image', 'pdf', 'image_path', 'pdf_path']
        labels = {'text':'', 'image_path':'Image','pdf_path':'pdf'}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}
