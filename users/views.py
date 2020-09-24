from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from geography.models import Projector, Project, Post
from django.db.models import Count
from .models import User
from .forms import NameForm

@login_required
def edit_account(request, username):
	if request.user == username:
		user = User.objects.get(username=username)
	message=''
	if request.method == 'POST':
		form = NameForm(data=request.POST)
		if form.is_valid():
			user.username = form.cleaned_data['your_name']
			user.save()
		else:
			return HttpResponseRedirect(reverse('account', args=[user.username]))
	else:
		form = NameForm(initial={'your_name':username})
	return render(request, 'users/edit_account.html', {'form' : form})

def account(request, username):
	p_tot = len(Project.objects.filter(owner__username=username))
	po_tot = len(Post.objects.filter(project__owner__username=username))
	date_joined = User.objects.get(username=username).date_joined
	context = {"project_tot": p_tot, "post_tot": po_tot, 'date_joined': date_joined, 'username':username}
	return render(request, 'users/account.html', context)

@login_required
def password_change(request):
	if request.method == 'POST':
		form = PasswordChangeForm(user=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			message = "Your password has been updated."
		else:
			message = "Something went wrong."
		return HttpResponseRedirect(reverse('account', args=[request.user.username]))
	else:
		form = PasswordChangeForm()
	return render(request, 'users/password_change.html', {'form': form})


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
			p = Projector(user=new_user)
			p.save()
			login(request, authenticated_user)
			return HttpResponseRedirect(reverse('index'))
	context = {'form': form, 'nbar': 'register'}
	return render(request,'users/register.html', context)
