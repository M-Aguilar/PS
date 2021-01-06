from django.shortcuts import render
from geography.models import Project
# Create your views here.
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
