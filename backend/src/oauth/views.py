from django.shortcuts import render
import social.apps.django_app.default.models as sm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User


def home(request):
	#logout(request)
	uname=""
	if request.method == 'POST' and 'submit' in request.POST:
		submit = request.POST['submit']
		if submit=="sign-out":
			logout(request)
	if '_auth_user_id' in request.session:
		user = User.objects.get(pk = request.session['_auth_user_id'])
		
		data = {
			'uname': user.username,
			'name': (user.first_name + ' ' + user.last_name),
			'email': user.email
		}
		return render(request,'home.html',data)
	return render(request,'home.html',{'uname': uname})

def show(request):
	return HttpResponse("Hello %s"%request.session['uname'])

def log_out(request):
	if '_auth_user_id' in request.session:
		logout(request)
	return render(request,'home.html',{})

