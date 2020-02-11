from django.shortcuts import render

# Create your views here.
def index(request):
	context = {'nbar': 'index'}
	return render(request, 'main/index.html', context)

def about(request):
	context = {'nbar': 'about'}
	return render(request, 'main/about.html', context)
