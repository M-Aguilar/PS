from django.http.request import HttpRequest
from django.shortcuts import render, reverse, get_object_or_404
from geography.models import Project
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.utils.text import slugify
from django.contrib import messages
from datetime import datetime
from datetime import datetime

def index(request):
	recent_visit = False
	# check for existance of cookie
	if 'last_visit' in request.session.keys():
		last_visit = request.session['last_visit']
		# the cookie is a string - convert back to a datetime type
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		curr_time = datetime.now()
		if (curr_time-last_visit_time).days > 0:
			# if at least one day has gone by then inc the visit count.
			request.session['last_visit'] = str(datetime.now())
		else:
			recent_visit = True
		if 'logout' in request.session.keys():
			if request.session['logout']:
				recent_visit = False
				request.session['logout'] = False
	else: # create cookie keeping track of last visit
		request.session['last_visit'] = str(datetime.now())
	banners = []
	#control max num probably
	projects = Project.objects.filter(public=True)
	for project in projects:
		if project.banner:
			banners.append(project)
	if request.user.is_authenticated:
		messages.success(request, "Welcome {0}".format(request.user))
	context = {'nbar': 'index', 'projects': banners, 'recent_visit': recent_visit}
	return render(request, 'main/index.html', context)

def about(request):
	context = {'nbar': 'about'}
	return render(request, 'main/about.html', context)
