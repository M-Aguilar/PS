from django.http.request import HttpRequest
from django.shortcuts import render, reverse, get_object_or_404
from geography.models import Project
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.utils.text import slugify
from django.contrib import messages
from datetime import datetime
from django.utils import timezone

def index(request):
	recent_visit = False
	if 'last_visit' in request.session.keys():
		last_visit = request.session['last_visit']
		# the cookie is a string - convert back to a datetime type
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		curr_time = datetime.now()
		if (curr_time-last_visit_time).days > 0:
			# if at least one day has gone by then inc the visit count.
			request.session['last_visit'] = datetime.now()
		else:
			recent_visit = True
	else:
		request.session['last_visit'] = datetime.now()
	banners = []
	#control max num probably
	projects = Project.objects.filter(public=True)
	for project in projects:
		if project.banner:
			banners.append(project)
	context = {'nbar': 'index', 'projects': banners, 'recent_visit': recent_visit}
	return render(request, 'main/index.html', context)

def about(request):
	context = {'nbar': 'about'}
	return render(request, 'main/about.html', context)
