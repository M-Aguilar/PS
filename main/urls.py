from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('pages/new_page', views.new_page, name='new_page'),
    path('pages/edit_page/<page_id>', views.edit_page, name='edit_page'),
    path('<slug_url>', views.page, name='page'),
    path('pages/delete_page/<page_id>', views.delete_page, name='delete_page'),
]
