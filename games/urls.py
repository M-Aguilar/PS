from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name="games"),
	path('<path>', views.game, name="game"),
	path('edit/<path>', views.edit_game, name="edit_game"),
]