from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.db.models import Count
from .models import User
from .forms import NameForm

@login_required
def edit_account(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect(reverse('account'))
	else:
		form = NameForm()
	return render(request, 'users/edit_account.html', {'form' : form })

@login_required
def account(request, username):
	context = {"username" :username}
	return render(request, 'users/account.html', context)

@login_required
def logout_view(request):
	"""log the user out."""
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def register(request):
	"""register a new user"""
	if request.method != 'POST':
		#Displat blank registration form.
		form = UserCreationForm()
	else: 
		#process completed form.
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			new_user = form.save()
			#Log the user in and then redirect to home page.
			authenticated_user = authenticate(request, username=new_user.username, password=request.POST['password1'])
			login(request, authenticated_user)
			return HttpResponseRedirect(reverse('index'))

	context = {'form': form}
	return render(request,'users/register.html', context)
