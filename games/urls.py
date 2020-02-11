from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name="games"),
	path('<game_id>', views.game, name="game"),
]
