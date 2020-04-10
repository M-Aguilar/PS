from django.shortcuts import render
from .models import Project, Post
from .forms import ProjectForm, PostForm
from django.contrib.auth.decorators import login_required
#from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist

from django.db.models import Count
#unused currently
import math
import os
from django.conf import settings
# Create your views here.
'''
possible inputs
as registered user and projector
    public -- other user -- own projects

as registered non owner
    public other - other user 

as non registered
    public -- specific user's public
'''

def projects(request, user_id='public', sort='', page_num=0):
    if sort is '':
        p_sort = '-date_edited'
    else:
        p_sort = sort
    if user_id != 'public':
        nbar='private'
        try:
            user_id = int(user_id)
        except ValueError:
            pass
        if isinstance(user_id, int):
            try:
                public = User.objects.get(id=user_id)
            except (ObjectDoesNotExist, ValueError) as e:
                print(1)
                raise Http404
        else:
            try:
                public = User.objects.get(username=user_id)
            except (ObjectDoesNotExist, ValueError) as e:
                print(2)
                raise Http404
        if request.user.is_authenticated:
            projects = Project.objects.filter(owner=public.id)
            if sort == 'post_num':
                projects = projects.annotate(count=Count('post')).order_by('count')
            elif sort == '-post_num':
                projects = projects.annotate(count=Count('post')).order_by('-count')
            else: 
                try:
                    Project._meta.get_field(p_sort.replace('-',''))
                    projects = projects.order_by(p_sort)
                except FieldDoesNotExist:
                    print(3)
                    raise Http404
        else: #for all other viewing of no owners projects 
            try:
                projects = Project.objects.filter(owner=public.id, public=True)
            except NameError:
                print(4)
                raise Http404
            if sort == 'post_num' or sort == '-post_num':
                projects = projects.annotate(Count('posts'))
            else:
                try:
                    Project._meta.get_field(p_sort.replace('-',''))
                    projects = projects.order_by(p_sort)
                except FieldDoesNotExist:
                    print(5)
                    raise Http404        
    else:
        #All Public
        projects = Project.objects.filter(public=True)
        if sort == 'post_num':
                projects = projects.annotate(count=Count('post')).order_by('count')
        elif sort == '-post_num':
                projects = projects.annotate(count=Count('post')).order_by('-count')
        else:
            try:
                Project._meta.get_field(p_sort.replace('-',''))
                projects = projects.order_by(p_sort)
            except FieldDoesNotExist:
                print(6)
                raise Http404
        public = 'public'
        nbar='public'
    next_p = False
    total = len(projects)
    if len(projects) > 10:
        if page_num == 0 or page_num == '0':
            page_num = 1
        else:
            try:
                page_num = int(page_num)
            except ValueError:
                raise Http404
            if page_num < -1:
                print(7)
                raise Http404
        if page_num == math.ceil(len(projects)/10):
            if (math.floor(len(projects)/10)) == page_num:
                projects = projects[(page_num-1)*10:]
            else:
                projects = projects[(math.floor(len(projects)/10))*10:]
        else:
            projects = projects[(page_num-1)*10:10 * page_num]
            next_p = True
    context = {'projects':projects, 'public': public, 'nbar': nbar, 'sort': p_sort, 'page_num':page_num,'next': next_p, 'total': total}
    #For another day
    #if request.is_ajax():
    #    print(locals())
    #    return render(request, 'geography/projects_inject.html', locals())
    return render(request, 'geography/projects.html', context)

def project(request, project_id, sort='', page_num=0):
    if sort is '':
        p_sort = '-date_edited'
    else:
        p_sort = sort
    try:
        project = Project.objects.get(id=project_id)
    except (ObjectDoesNotExist, ValueError) as e:
        raise Http404
    p_tot = 0
    if project.owner != request.user and not project.public:
        raise Http404
    if request.user.is_authenticated and request.user == project.owner:
        try:
            Post._meta.get_field(p_sort.replace('-',''))
            posts = project.post_set.order_by(p_sort)
        except FieldDoesNotExist:
            raise Http404
    else:
        try:
            Post._meta.get_field(p_sort.replace('-',''))
            posts = project.post_set.filter(public=True).order_by(p_sort)
        except FieldDoesNotExist:
            raise Http404
    next_p = False
    total = len(posts)
    if len(posts) > 10:
        if page_num == 0 or page_num == '0':
            page_num = 1
        else:
            try:
                page_num = int(page_num)
            except ValueError:
                raise Http404
            if page_num < -1:
                print(8)
                raise Http404
        if page_num == math.ceil(len(posts)/10):
            if (math.floor(len(posts)/10)) == page_num:
                posts = posts[(page_num-1)*10:10 * page_num]
            else:
                posts = posts[(math.floor(len(posts)/10))*10:]
        else:
            posts = posts[(page_num-1)*10:10 * page_num]
            next_p = True
    context = {'project': project, 'posts': posts, 'nbar': 'project', 'sort': p_sort, 'page_num': page_num, 'next': next_p,'total':total}
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

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    project = post.project.id
    if post.project.owner != request.user:
        raise Http404
    else:
        post.delete()
        return HttpResponseRedirect(reverse('project', args=[project]))

@login_required
def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    owner = project.owner.id
    if project.owner != request.user:
        raise Http404
    else:
        project.delete()
        return HttpResponseRedirect(reverse('projects', args=[owner]))