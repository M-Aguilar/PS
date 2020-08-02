from django.urls import path

from . import views

urlpatterns = [
	#URLS is strange. there cannot e 2 single slug urls as they will conflict.
	#Django will choose the highest single url input to resolve it. 
	#strane behavior I'm telling yuh. 
	path('', views.index, name='games'),
	path('play/<path>', views.game, name='game'),
	path('edit/<path>', views.edit_game, name='edit_game'),
	path('new_game', views.new_game, name='new_game'),
	path('<path>/rating', views.rating, name='rating'),
]