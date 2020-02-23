from django.shortcuts import render
from .models import Project, Post
from .forms import ProjectForm, PostForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
'''
possible inputs
as registered user and projector
    public -- other user -- own projects

as registered non owner
    public other - other user 

as non registered
    public -- specific user's public
TODO adjust urls to show username instead of user id
'''
def projects(request, user_id='public'):
    #public = True
    #user_id either equals public or it doesnt
    if user_id != 'public':
        #this is for user looking at their own files
        try:
            public = int(user_id)
        except ValueError:
            raise Http404
        if request.user.is_authenticated and request.user.id == public:
            projects = Project.objects.filter(owner=request.user).order_by('-date_edited')
        else: #for all other viewing of no owners projects 
            try:
                projects = Project.objects.filter(owner=user_id, public=True).order_by('-date_added')
            except NameError:
                raise Http404
        try:
            public = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise Http404
    else:
        projects = Project.objects.filter(public=True).order_by('date_added')
        public = user_id
    context = {'projects':projects, 'public': public, 'nbar': 'project'}
    return render(request, 'geography/projects.html', context)

def project(request, project_id):
    project = Project.objects.get(id=project_id)
    if project.owner != request.user and not project.public:
        raise Http404
    posts = project.post_set.order_by('-date_added')
    context = {'project': project, 'posts': posts, 'nbar': 'project'}
    return render(request, 'geography/project.html', context)


@login_required
def new_project(request):
    if request.method != 'POST':
        form = ProjectForm()
    else:
        form = ProjectForm(request.POST)
        if form.is_valid():
            new_p = form.save(commit=False)
            new_p.owner = request.user
            new_p.save()
            return HttpResponseRedirect(reverse('projects'))
    context = {'form': form, 'nbar': 'project'}
    return render(request, 'geography/new_project.html', context)

@login_required
def new_post(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.project = project
            new_post.save()
            new_post.project.save()
            return HttpResponseRedirect(reverse('project', args=[project_id]))
    context = {'project':project,'form': form, 'nbar': 'project'}
    return render(request, 'geography/new_post.html', context)

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    project = post.project
    if project.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project', args=[project.id]))
    context = {'post': post, 'project':project, 'form':form, 'nbar': 'project'}
    return render(request, 'geography/edit_post.html', context)

@login_required
def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if project.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = ProjectForm(instance=project)
    else:
        form = ProjectForm(instance=project, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('projects'))
    context = {'project':project, 'form':form, 'nbar': 'project'}
    return render(request, 'geography/edit_project.html', context)

