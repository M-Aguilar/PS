from django.shortcuts import render, redirect
from .models import Project, Post
from .forms import ProjectForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist

from itertools import chain

from django.db.models import Count
import math
import os

from django.db.models import Q
from django.views.generic import ListView

'''
TODO: This could definitely be fleshed out more. It could allow for arguments
for example user=username and listing the publuc posts of that user. Could also provide user
page.
-keyword to exclude word in serach
There needs to be priorty in the search results. I want the most relevant searches at the top.
For example posts that contain multiple keywords should be higher up the search result list

'''
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

        #Debug printer
        #print('query: ' + query + ' -  Type: ' + str(type(query)))

        #Checks for page num otherwise sets it
        page_num = self.request.GET.get('page_num')
        if not page_num:
            page_num = 0

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
        '''
        Now that I have potentially two lists I need to adjust the function below to account for projects as a product of results ideally at the top
        I want the total to still be 10.
        '''
        #to be or not to be. Concatinate total length.
        total = len(object_list) #+ len(projects)
        #assumes a single page to be changed if tested otherwise
        next_p = False
        if total > 10:
            #sets page to 1 if 0 or sets to passed page_num or raises 404 if out of bounds
            if page_num == 0 or page_num == '0':
                page_num = 1
            else:
                try:
                    page_num = int(page_num)
                except ValueError:
                    raise Http404
                if page_num < 0 or page_num > math.ceil((len(object_list)/10)):
                    print(7)
                    raise Http404

            #pagination checks if page_num is last page
            if page_num == math.ceil(total/10):
                #what am i doing here??? I dont know but it works
                if (math.floor(total/10)) == page_num:
                    object_list = object_list[(page_num-1)*10:]
                else:
                    object_list = object_list[(math.floor(len(object_list)/10))*10:]
            else:
                object_list = object_list[(page_num-1)*10:10 * page_num]
                next_p = True
        object_list = {'object_list': object_list, 'projects' :projects, 'q': query, 'total': total, 'page_num': page_num, 'next':next_p, 'nbar':nbar}
        return object_list

def pagination(q_list, page_num):
    total=len(q_list)
    return object_list

def projects(request, user_id='public', sort='', page_num=0):
    sort_options = ['public','title','post_num', 'date_edited','date_added']
    if sort.replace('-','') not in sort_options and sort != '':
        raise Http404
    nbar='public'
    if sort is '':
        p_sort = '-date_edited'
    else:
        p_sort = sort
    if user_id != 'public':
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
        if request.user.is_authenticated and public == request.user:
            nbar='private'
            projects = Project.objects.filter(owner=public.id)
            if sort == 'post_num':
                projects = projects.annotate(count=Count('post')).order_by('count')
            elif sort == '-post_num':
                projects = projects.annotate(count=Count('post')).order_by('-count')
            else: 
                try:#*
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
                try:#*
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
            try:#*
                projects = projects.order_by(p_sort)
            except FieldDoesNotExist:
                print(6)
                raise Http404
        public = 'public'
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
            if page_num < 0:
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
    sort_options = ['public','image','pdf', 'date_edited','date_added']
    if sort.replace('-','') not in sort_options and sort != '':
        raise Http404
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
        try:#*
            posts = project.post_set.order_by(p_sort)
        except FieldDoesNotExist:
            raise Http404
    else:
        try:#*
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
    if project.owner != request.user:
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

'''
interesting command worth understanding further
Project._meta.get_field(p_sort.replace('-',''))
found at *

'''