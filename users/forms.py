from django import forms

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=20)

	def __init__(self, *args, **kwargs):
		super(NameForm, self).__init__(*args, **kwargs)
		if len(args) > 0:
			self.fields['your_name'].widget.attrs['placeholder'] = args[0]['username']
