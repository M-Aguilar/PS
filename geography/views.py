from django.shortcuts import render
from .models import Project, Post
from .forms import ProjectForm, PostForm
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

# Create your views here.
def projects(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(owner=request.user).order_by('date_added')
    else:
        projects = Project.objects.filter(public=True).order_by('date_added')
    context = {'projects':projects}
    return render(request, 'geography/projects.html', context)

def project(request, project_id):
    project = Project.objects.get(id=project_id)
    if project.owner != request.user and not project.public:
        raise Http404
    posts = project.post_set.order_by('-date_added')
    context = {'project': project, 'posts': posts}
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
    context = {'form': form}
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
            return HttpResponseRedirect(reverse('project', args=[project_id]))
    context = {'project':project,'form': form}
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
        form = PostForm(instance=post, data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project', args=[project.id]))
    context = {'post': post, 'project':project, 'form':form}
    return render(request, 'geography/edit_post.html', context)
