from django.shortcuts import render, reverse, get_object_or_404
from geography.models import Project
from main.models import Page
from main.forms import PageForm
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

def page(request, slug_url):
	page = get_object_or_404(Page, slug_url=slug_url)
	context = {'page': page}
	return render(request, 'main/page.html', context)

@login_required
def new_page(request):
	if not request.user.is_authenticated and not request.user.projector.admin:
		raise Http404
	if request.method != 'POST':
		form = PageForm()
	else:
		form = PageForm(request.POST)
		if form.is_valid():
			new_p = form.save(commit=False)
			new_p.owner = request.user
			name_check = Page.objects.filter(name__icontains=new_p.name)
			if len(name_check) > 0:
				new_p.slug_url = "{0}-{1}".format(slugify(new_p.name), str(len(name_check)))
			else:
				new_p.slug_url = slugify(new_p.name)
				new_p.save()
			return HttpResponseRedirect(reverse('page', args=[new_p.slug_url]))
	context = {'form': form}
	return render(request, 'main/new_page.html', context)

@login_required
def edit_page(request, page_id):
	if not request.user.is_authenticated and not request.user.projector.admin:
		raise Http404
	page = get_object_or_404(Page, id=page_id)
	if request.method != 'POST':
		form = PageForm(instance=page)
	else:
		form = PageForm(instance=page, data=request.POST)
		if form.is_valid():
			f = form.save()
		return HttpResponseRedirect(reverse('page', args=[f.slug_url]))
	context = {'page': page, 'form':form}
	return render(request, 'main/edit_page.html', context)

@login_required
def delete_page(request, page_id):
	if not request.user.is_authenticated and not request.user.projector.admin:
		messages.error(request, "You don't have the permissions to perform this request.")
		return HttpResponseRedirect(request.META.HTTP_REFERER)
	page = get_object_or_404(Page, id=page_id)
	page_name = page.name
	page.delete()
	messages.success(request, 'You have successfully deleted: {0}'.format(page_name))
	return HttpResponseRedirect(reverse('account', args=[request.user]))

def about(request):
	context = {'nbar': 'about'}
	return render(request, 'main/about.html', context)
