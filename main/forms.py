from django import forms
from .models import Page

class PageForm(forms.ModelForm):
        class Meta:
            model = Page
            fields = ['name', 'navbar','html']
            labels = {'name': '', 'navbar':'Show in navbar'}

            widgets = {
                'html': forms.Textarea(attrs={'autofocus':'autofocus','class':'form-control','rows':20}),
                'name': forms.TextInput(attrs={'class':'form-control','rows':1,'placeholder':'Page Name'}),
                'navbar': forms.CheckboxInput(attrs={'class':'form-check'}),
            }
