from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<project_id>', views.project, name='project'),
    path('new_project', views.new_project, name='new_project'),
    path('new_post/<project_id>', views.new_post, name='new_post'),
    path('edit_post/<post_id>', views.edit_post, name='edit_post'),
    path('edit_project/<project_id>', views.edit_project, name='edit_project'),
]