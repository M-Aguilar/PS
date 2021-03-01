from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist

from itertools import chain

from django.db.models import Count
import math
import os

from django.db.models import Q
from django.views.generic import ListView

from .models import Project, Post
from .forms import ProjectForm, PostForm

class SearchResultsView(ListView):
    model = Post
    template_name = 'geography/search_results.html'

    def get_queryset(self):
        #searches for query
        query = self.request.GET.get('q')

        #navbar styling. default public.
        nbar='public'

        #future implementation of sorting
        sort='-date_edited'
        #if not logged in. and not an empty query.
        if self.request.user.is_authenticated and query not in ['', None]:
            #navbar styling
            nbar = 'private'
            #Post filter: query in test,username, project title, project text, public and public project or owned
            object_list = Post.objects.filter(Q(text__icontains=query) | Q(project__owner__username__icontains=query) | Q(project__title__icontains=query) | Q(project__text__icontains=query), Q(public=True) & Q(project__public=True) | Q(project__owner=self.request.user)).order_by(sort)            
            #project filter
            projects = Project.objects.filter(Q(title__icontains=query) | Q(owner__username__icontains=query) | Q(text__icontains=query), Q(public=True) | Q(owner=self.request.user)).order_by(sort)
        elif query not in ['',None]:
            #see above minus owned
            object_list = Post.objects.filter(Q(text__icontains=query) | Q(project__title__icontains=query) | Q(project__text__icontains=query) | Q(project__owner__username__icontains=query), Q(public=True) & Q(project__public=True)).order_by(sort)
            projects = Project.objects.filter(Q(title__icontains=query) | Q(owner__username__icontains=query) | Q(text__icontains=query), Q(public=True)).order_by(sort)
        else:
            #if query is '' or none
            object_list={}
            projects={}
        #assumes a single page to be changed if tested otherwise
        paginator = Paginator(object_list, 10)
        page_num = self.request.GET.get('page')
        if not page_num:
            page_num = 1
        page_o = paginator.get_page(page_num)
        object_list = {'object_list': page_o, 'projects' :projects, 'q': query, 'nbar':nbar}
        return object_list

#I dont like it
def projects(request, user_id='public'):
    sort = request.GET.get('sort')
    sort_options = ['title','post_num', 'date_edited','date_added']
    nbar= 'public'
    if sort and sort.replace('-','') in sort_options:
        p_sort = sort
    else:
        p_sort = 'date_edited'
    if user_id != 'public':
        try:
            user_id = int(user_id)
        except ValueError:
            pass
        if isinstance(user_id, int):
            public = get_object_or_404(User, id=user_id)
        else:
            public = get_object_or_404(User, username=user_id)
        if request.user.is_authenticated and public == request.user:
            nbar='private'
            projects = Project.objects.filter(owner=public.id)
        else:
            try:
                projects = Project.objects.filter(owner=public.id, public=True)
            except NameError:
                print(4)
                raise Http404   
    else:
        projects = Project.objects.filter(public=True)
        public = 'public'
    if sort == 'post_num':
        projects = projects.annotate(count=Count('post')).order_by('count')
    elif sort == '-post_num':
        projects = projects.annotate(count=Count('post')).order_by('-count')
    else:
        try:
            projects = projects.order_by(p_sort)
        except FieldDoesNotExist:
            print(5)
            raise Http404     
    paginator = Paginator(projects, 10)
    page_num = request.GET.get('page')
    if not page_num:
        page_num = 1
    page_o = paginator.get_page(page_num)
    context = {'projects':page_o, 'public': public, 'nbar': nbar, 'sort': p_sort, 'sort_options':sort_options}
    return render(request, 'geography/projects.html', context)

def project(request, project_id):
    sort = request.GET.get('sort')
    sort_options = ['public','image','pdf', 'date_edited','date_added']
    if sort and sort.replace('-','') in sort_options:
        p_sort = sort
    else:
        p_sort = '-date_edited'
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user and not project.public:
        raise Http404
    if request.user.is_authenticated and request.user == project.owner:
        posts = project.post_set.order_by(p_sort)
    else:
        try:
            posts = project.post_set.filter(public=True).order_by(p_sort)
        except FieldDoesNotExist:
            raise Http404
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    if not page_num:
        page_num = 1
    page_o = paginator.get_page(page_num)
    context = {'project': project, 'posts': page_o, 'nbar': 'project', 'sort': p_sort,'sort_options': sort_options}
    return render(request, 'geography/project.html', context)

@login_required
def new_project(request):
    if not request.user.projector.admin:
        raise Http404
    if request.method != 'POST':
        form = ProjectForm()
    else:
        form = ProjectForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_p = form.save(commit=False)
            new_p.owner = request.user
            new_p.save()
            return HttpResponseRedirect(reverse('projects', args=[request.user.id]))
    context = {'form': form, 'nbar': 'new_project'}
    return render(request, 'geography/new_project.html', context)

@login_required
def new_post(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method != 'POST':
        data={'project':project}
        form = PostForm(initial=data)
    else:
        form = PostForm(data=request.POST, files=request.FILES)
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
        i = request.POST.get('image-clear',0)
        p = request.POST.get('pdf-clear',0)
        if i != 0:
            img = post.image
        if p != 0:
            pdf = post.pdf
        form = PostForm(instance=post, files=request.FILES, data=request.POST)
        if form.is_valid():
            if i == 'on':
                img.delete()
            if p == 'on':
                pdf.delete()
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
        f = request.POST.get('banner-clear',0)
        if f != 0:
            b = project.banner
        form = ProjectForm(instance=project, files=request.FILES, data=request.POST)
        if form.is_valid():
            if f == 'on':
                b.delete()
            form.save()
            return HttpResponseRedirect(reverse('projects', args=[project.owner]))
    context = {'project':project, 'form':form, 'nbar': 'project'}
    return render(request, 'geography/edit_project.html', context)

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    project = post.project.id
    if post.project.owner != request.user:
        raise Http404
    else:
        if post.image:
            post.image.delete()
        if post.pdf:
            post.pdf.delete()
        post.delete()
        return HttpResponseRedirect(reverse('project', args=[project]))

@login_required
def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    posts_w_img = Post.objects.filter(project=project, image__isnull=False)
    posts_w_pdf = Post.objects.filter(project=project, pdf__isnull=False)
    owner = project.owner.id
    if not request.user.is_authenticated or project.owner != request.user:
        raise Http404
    else:
        if project.banner:
            project.banner.delete()
        if len(posts_w_img)> 1:
            for post in posts_w_img:
                post.image.delete()
        if len(posts_w_pdf)> 1:
            for post in posts_w_pdf:
                post.pdf.delete()
        project.delete()
        return HttpResponseRedirect(reverse('projects', args=[owner]))
