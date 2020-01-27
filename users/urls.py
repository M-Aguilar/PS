from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    #logout page
    path('logout/', views.logout_view, name='logout'),

    #registration page
    path('register/', views.register, name='register'),

    #path('accounts/', include('django.contrib.auth.urls')),
    #edit account page
    path('edit_account/', views.edit_account, name='edit_account'),
    #account page
    path('<username>/', views.account, name='account'),
]
