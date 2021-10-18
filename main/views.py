from django.shortcuts import render, reverse, get_object_or_404
from geography.models import Project
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.utils.text import slugify
from django.contrib import messages

def index(request):
	banners = []
	#control max num probably
	projects = Project.objects.filter(public=True)
	for project in projects:
		if project.banner:
			banners.append(project)
	context = {'nbar': 'index', 'projects': banners}
	return render(request, 'main/index.html', context)

def about(request):
	context = {'nbar': 'about'}
	return render(request, 'main/about.html', context)
