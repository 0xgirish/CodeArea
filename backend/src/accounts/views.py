from django.shortcuts import render

# Create your views here.

def isworking(request):
	return render(request, "home.html")
