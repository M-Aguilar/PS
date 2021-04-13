from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('get_order',views.get_order, name='get_order'),
    path('<user_id>/projects', views.projects, name='projects'),
    
    #path('search/<page_num>/',views.SearchResultsView.as_view(), name='search_page'),
    #path('search', views.search, name='search'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),

    path('project/<project_id>', views.project, name='project'),

    path('new_project', views.new_project, name='new_project'),
    path('new_post/<project_id>', views.new_post, name='new_post'),
    path('edit_post/<post_id>', views.edit_post, name='edit_post'),
    path('edit_project/<project_id>', views.edit_project, name='edit_project'),
    path('delete_post/<post_id>', views.delete_post, name='delete_post'),
    path('delete_project/<project_id>', views.delete_project, name='delete_project'),
]
