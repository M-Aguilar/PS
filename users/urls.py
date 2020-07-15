from django.urls import path
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView

from . import views

urlpatterns = [
    path('login', LoginView.as_view(template_name='users/login.html'), name='login'),
    #logout page
    path('logout', views.logout_view, name='logout'),

    #registration page
    path('register', views.register, name='register'),

    path('password_change_done', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),name='password_change_done'),

    path('password_change', PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),

    #edit account page
    path('<username>/edit_account', views.edit_account, name='edit_account'),
    #account page
    path('<username>', views.account, name='account'),
]
